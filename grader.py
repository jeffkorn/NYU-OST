#!/usr/bin/python
import cgitb; cgitb.enable()
import cgi
import config
import datetime
import hashlib
import logging
import os
import tarfile
import urlparse
import zipfile

from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class UploadContent(db.Model):
  sid = db.StringProperty()
  filename = db.StringProperty()
  contents = db.Blob()
  content_len = db.StringProperty()
  assignment = db.StringProperty()
  date = db.DateTimeProperty(auto_now=True)
  blob_key = blobstore.BlobReferenceProperty()

class UploadLog(db.Model):
  sid = db.StringProperty()
  filename = db.StringProperty()
  assignment = db.StringProperty()
  date = db.DateTimeProperty(auto_now=True)
  blob_key = blobstore.BlobReferenceProperty()
  user = db.StringProperty()
  action = db.StringProperty()

class UserInfo(db.Model):
  name = db.StringProperty()
  email = db.StringProperty()
  sid = db.StringProperty()
  last_action = db.DateTimeProperty()

class Grader(db.Model):
  name = db.StringProperty()
  sid = db.StringProperty()
  assignments = db.StringListProperty()
  is_admin = db.BooleanProperty()

class Assignment(db.Model):
  due_date = db.DateTimeProperty()
  title = db.StringProperty()
  url = db.StringProperty()
  grade_released = db.BooleanProperty()
  is_assigned = db.BooleanProperty()
  submit_url = db.BooleanProperty()

class Grade(db.Model):
  sid = db.StringProperty()
  asgn = db.StringProperty()
  original_score = db.StringProperty()
  penalty = db.StringProperty()
  extra_points = db.StringProperty()
  final_score = db.StringProperty()
  comments = db.StringProperty()
  private_comments = db.StringProperty()
  grader = db.StringProperty()

##################################

def alert(msg):
  print
  print
  print '''<SCRIPT language="JavaScript">
           alert("%s");
           </SCRIPT>
        ''' % msg

def back():
  print '''<SCRIPT language="JavaScript">
           history.back();
           </SCRIPT>
        '''
def get_user_info():
  aeu = users.get_current_user()
  s = UserInfo.get_or_insert(aeu.user_id(),
                             email=aeu.email(), name=aeu.nickname()) 
  s.last_action = datetime.datetime.now()
  s.put()
  return s

def userinfo_fromhash(sid, sid_hash):
  query = db.Query(UserInfo)
  query.filter('sid =', sid)
  for r in query:
    if r.sid == sid and sidHash(r) == sid_hash:
      return r
  return None

def output_template(name, template_values):
  path = os.path.join(os.path.dirname(__file__), name)
  return template.render(path, template_values)

def sidHash(s):
  return hashlib.md5('%s:%s' % (s.sid, str(s.last_action))).hexdigest()[0:16]

def sid_registered(sid):
  query = db.Query(UserInfo)
  query.filter('sid =', sid)
  for r in query:
    return True
  return False

def saveuser(sid, name, email):
 usr = users.get_current_user()
 s = UserInfo.get_or_insert(usr.user_id(), email=email, name=name)
 query = db.Query(UserInfo)
 query.filter('sid =', sid)
 for r in query:
   if s.key() != r.key(): return False
 s.sid = sid
 s.email = email
 s.name = name
 s.put()
 return True

def register(sid=None, name='', email=''):
  if not sid or not name or not email:
    alert('Missing info.  Fill out all fields.')
    back()
    return 0
  if not saveuser(sid, name, email):
    alert('Student ID exists.')
    back()
    return 0
  alert('You have successfully registered.')
  return 1

def basename(f):
  return os.path.basename(f)

def fileinfo(content):
  result = []
  date = content.date.strftime('%D %H:%M:%S')
  if not content.blob_key:
    return
  try:
    zip = zipfile.ZipFile(blobstore.BlobReader(content.blob_key))
    for zipinfo in zip.infolist():
      result.append({'name' : basename(zipinfo.filename),
                     'size' : zipinfo.file_size,
                     'date' : date})
    zip.close()
    return result
  except:
    pass
  try:
    tar = tarfile.open(fileobj=blobstore.BlobReader(content.blob_key))
    for tarinfo in tar:
      result.append({'name': basename(tarinfo.name),
                     'size': tarinfo.size,
                     'date': date})
    tar.close()
    return result
  except:
    pass
  result.append({'name' : content.filename, 'size' : content.content_len,
    'date' : date})
  return result


def get_hws():
  result = []
  i = 0
  idx = {}
  hws = config.hws()
  hw_names = hws.keys()
  hw_names.sort()
  for n in hw_names:
    hws[n]['name'] = n
    result.append(hws[n])
    idx[n] = i
    i = i + 1
  return (result, idx)

#################

def cgi_upload(asgn=None):
  s = get_user_info()
  if not s.sid:
    return cgi_home()
  sid = s.sid
  hws = config.hws()
  hw_names = hws.keys()
  hw_names.sort()
  if not asgn: asgn = hw_names[-1]
  files = []
  query = db.Query(UploadContent)
  query.filter('assignment =', asgn)
  query.filter('sid =', sid)
  for r in query:
    files.extend(fileinfo(r))
  upload_url = blobstore.create_upload_url('/upload')
  upload_url_parse = urlparse.urlparse(upload_url)
  upload_key = upload_url_parse.path.split('/')[-1]

  template_values = {
    'sid' : sid,
    'sid_hash' : sidHash(s),
    'hw' : hws[asgn],
    'upload_url' : upload_url,
    'upload_key' : upload_key,
    'files' : files,
  }
  template_values['hws'] = []
  for n in hw_names:
    hws[n]['name'] = n
    template_values['hws'].append(hws[n])
  return output_template('upload.tpl', template_values)

def cgi_rm(asgn=None, filename=None):
  s = get_user_info()
  if not s.sid:
    return cgi_home()
  sid = s.sid
  query = db.Query(UploadContent)
  query.filter('assignment =', asgn)
  query.filter('sid =', sid)
  query.filter('filename =', filename)
  for r in query:
    logging.debug('Remove %s' % str(r))
    r.delete()
  ul = UploadLog()
  ul.filename = filename
  ul.assignment = asgn
  ul.sid = sid
  ul.action = 'delete'
  ul.put()
  return cgi_upload()

def cgi_register(sid=None, name='', email=''):
  if not sid:
    s = get_user_info()
    default_name = s.name
    if s.name == s.email:
      default_name = ''
    template_values = {
      'class_year'    : 2012,
      'default_email' : s.email,
      'default_name'  : default_name,
      'default_sid'   : s.sid or '',
    }
    return output_template('register.tpl', template_values)
  else:
    if register(sid=sid, name=name, email=email):
      return cgi_home(sid=sid)
    else:
      return cgi_register()

def cgi_admin(sid=None, hw=None):
  s = get_user_info()
  admin_sid = s.sid
  if admin_sid not in config.admins():
    return cgi_home()
  if hw != None:
    return cgi_scores(asgn=hw, student_sid=sid)
    #query = db.Query(Grade)
    #query.filter('sid =', sid)
    #query.filter('asgn =', hw)
    #results = []
    #for r in query:
    #  result = {'final_score' : r.final_score }
    #  results.append(result)
    #if len(results) == 1:
    #  template_values = results[0]
    #  logging.info(str(template_values))
    #return output_template('admin_grade.tpl', template_values)
  grade_query = db.Query(Grade)
  user_query = db.Query(UserInfo)
  grades = {}
  for r in grade_query:
    grades[(r.sid,r.asgn)] = r.final_score
  students = []
  for r in user_query:
    info = { 'name' : r.name, 'sid' : r.sid, 'grades' : [] }
    for hw in config.hws():
      grade = {'asgn' : hw}
      if grades.has_key((r.sid, hw)):
        grade['score'] = grades[(r.sid, hw)]
      else:
        grade['score'] = ''
      info['grades'].append(grade)
    students.append(info)
  students.sort()
  template_values = {
    'students' : students,
  }
  logging.info(str(template_values))
  return output_template('admin.tpl', template_values)

def cgi_home(sid=None):
  s = get_user_info()
  sid = s.sid
  if not sid:
    return cgi_register()
  else:
    if sid in config.admins():
      return cgi_admin()
    else:
      return cgi_upload()

def cgi_scores(asgn=None, store=None, basic=None, extra=None, penalty=None,
               final=None, comments=None, private_comments=None, grader=None,
               student_sid=None):
  s = get_user_info()
  sid = s.sid
  if not sid:
    return cgi_home()
  student_sid = student_sid or sid
  if sid not in config.admins():
    student_sid = sid

  template_values = {
    'sid' : sid,
    'graders' : config.graders(),
    'student_sid' : student_sid,
  }
  if asgn and sid in config.admins():
    template_values['admin'] = 1
    if store:
      g = Grade(key_name='%s:%s' % (student_sid, asgn))
      g.sid = student_sid
      g.asgn = asgn
      g.original_score = basic
      g.penalty = penalty
      g.extra_points = extra
      g.final_score = final
      g.grader = grader
      g.comments = comments
      g.private_comments = private_comments
      logging.info(g)
      g.put()
  query = db.Query(Grade)
  query.filter('sid =', student_sid)
  query2 = db.Query(UploadContent)
  query2.filter('sid =', student_sid)
  if asgn:
    query.filter('asgn =', asgn)
    query2.filter('assignment =', asgn)
    template_values.update(config.hws()[asgn])
    for r in query:
      template_values['basic'] = r.original_score
      template_values['extra'] = r.extra_points
      template_values['penalty'] = r.penalty
      template_values['final'] = r.final_score
      template_values['grader'] = r.grader
      template_values['comments'] = r.comments
      template_values['private_comments'] = r.private_comments
    return output_template('grade.tpl', template_values)
    # grader.showGrade(sid, hw)
  else:
    (hws, idx) = get_hws()
    for r in query:
      # config.hws()[r.asgn].update(r.__dict__)
      logging.info(r.asgn)
      # hws[idx[r.asgn]].update(r.__dict__)
      hws[idx[r.asgn]]['final_score'] = r.final_score
    for r in query2:
      # config.hws()[r.assignment]['has_file'] = 1
      hws[idx[r.assignment]]['has_file'] = 1
    template_values['hws'] = hws
    logging.info(str(template_values['hws'][0]))
    return output_template('scores.tpl', template_values)
    # grader.showAllGrades(sid)


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    if self.request.params.has_key('sid') and \
       self.request.params.has_key('sid_hash'):
      s = userinfo_fromhash(self.request.params['sid'],
                            self.request.params['sid_hash'])
    else:
      s = get_user_info()
    asgn = self.request.params['asgn']
    if not config.hws().has_key(asgn):
      self.error(500)
      return
    for upload in self.get_uploads():
      fn = os.path.basename(upload.filename)
      f = UploadContent(key_name='%s:%s' % (s.key().name(), fn))
      f.filename = fn
      f.assignment = asgn
      f.content_len = str(upload.size)
      f.blob_key = upload.key()
      f.sid = s.sid
      f.put()

      ul = UploadLog()
      ul.filename = fn
      ul.assignment = asgn
      ul.sid = s.sid
      ul.blob_key = upload.key()
      # ul.user = self.request.params['user']
      ul.action = 'upload'
      ul.put()

      self.redirect('/grader.cgi?command=upload&asgn=%s' % f.assignment)

class UploadHwHandler(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write(blobstore.create_upload_url('/upload'))

class ReqHandler(webapp.RequestHandler):
  def get(self):
    self.post()
  def post(self):
    args = {}
    params = self.request.params
    for key in params:
      logging.debug('Check %s' % key)
      args[str(key)] = params.get(key)
    logging.debug('Got args: %s' % str(args))
    if args.has_key('command') and handlers.has_key('cgi_'+args['command']):
      handler = handlers['cgi_' + args['command']]
      del args['command']
      # response = apply(handler, (), args)
      response = handler(**args)
    else:
      response = cgi_home()
    # self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write(response)

handlers = vars()

def main():
  app = webapp.WSGIApplication([
    ('/grader.cgi', ReqHandler),
    ('/upload_hw', UploadHwHandler),
    ('/upload', UploadHandler),
  ], debug=True)
  run_wsgi_app(app)

if __name__ == "__main__":
  main()

