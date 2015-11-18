#!/usr/bin/python

"""
Grader for AppEngine.
"""

import cgitb; cgitb.enable()
import cgi
import csv
import config
import datetime
import hashlib
import logging
import os
import tarfile
import urlparse
import zipfile
import StringIO

from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.ext import ndb
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
  course_id = db.StringProperty()
  date = db.DateTimeProperty(auto_now=True)
  blob_key = blobstore.BlobReferenceProperty()

class UploadLog(db.Model):
  sid = db.StringProperty()
  filename = db.StringProperty()
  assignment = db.StringProperty()
  course_id = db.StringProperty()
  date = db.DateTimeProperty(auto_now=True)
  blob_key = blobstore.BlobReferenceProperty()
  user = db.StringProperty()
  action = db.StringProperty()

class UserInfo(db.Model):
  name = db.StringProperty()
  email = db.StringProperty()
  sid = db.StringProperty()
  course_id = db.StringProperty()
  last_action = db.DateTimeProperty()

class Grade(db.Model):
  sid = db.StringProperty()
  asgn = db.StringProperty()
  course_id = db.StringProperty()
  original_score = db.StringProperty()
  penalty = db.StringProperty()
  extra_points = db.StringProperty()
  final_score = db.StringProperty()
  comments = db.TextProperty()
  private_comments = db.TextProperty()
  grader = db.StringProperty()

class Exam(db.Model):
  exam_id = db.StringProperty()
  course_id = db.StringProperty()
  sid = db.StringProperty()
  name = db.StringProperty()
  score = db.FloatProperty()

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
                             email=aeu.email(),
                             course_id=config.COURSE_ID,
                             name=aeu.nickname()) 
  s.last_action = datetime.datetime.now()
  s.put()
  config.load_config(s.course_id)
  return s

def userinfo_fromhash(sid, sid_hash):
  query = db.Query(UserInfo)
  query.filter('sid =', sid)
  for r in query:
    if r.sid == sid and sidHash(r) == sid_hash:
      config.load_config(r.course_id)
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

class UtcTzinfo(datetime.tzinfo):
  def utcoffset(self, dt): return datetime.timedelta(0)
  def dst(self, dt): return datetime.timedelta(0)
  def tzname(self, dt): return 'UTC'
  def olsen_name(self): return 'UTC'

class EdtTzinfo(datetime.tzinfo):
  def utcoffset(self, dt): return datetime.timedelta(hours=-5)
  def dst(self, dt): return datetime.timedelta(0)
  def tzname(self, dt): return 'EST+05EDT'
  def olsen_name(self): return 'US/Eastern'

class EstTzinfo(datetime.tzinfo):
  def utcoffset(self, dt): return datetime.timedelta(hours=-4)
  def dst(self, dt): return datetime.timedelta(0)
  def tzname(self, dt): return 'EST+05EDT'
  def olsen_name(self): return 'US/Eastern'

TZINFOS = {
  'utc': UtcTzinfo(),
  'est': EstTzinfo(),
  'edt': EdtTzinfo(),
}

def fileinfo(content):
  result = []
  t = content.date
  t = t.replace(tzinfo=TZINFOS['utc'])
  date = t.astimezone(TZINFOS['edt']).strftime('%D %H:%M:%S EDT')

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
  result.append({
    'name' : content.filename,
    'size' : content.content_len,
    'date' : date,
  })
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
    i += 1
  logging.info(str(result))
  logging.info(str(idx))
  return (result, idx)

def is_admin(sid):
  return sid in config.admins()

##############
# CGI Commands
##############

def cgi_upload(asgn=None):
  s = get_user_info()
  if not s.sid:
    return cgi_home()
  sid = s.sid
  hws = config.hws()
  if not asgn: asgn = config.HWS[-1]['id']
  files = []
  query = db.Query(UploadContent)
  query.filter('course_id =', s.course_id)
  query.filter('assignment =', asgn)
  query.filter('sid =', sid)
  submitted_url = ''
  for r in query:
    finfo = fileinfo(r)
    if len(finfo) == 1 and finfo[0]['size'] == None:
      submitted_url = finfo[0]['name']
    elif finfo:
      files.extend(finfo)
  upload_url = blobstore.create_upload_url('/upload')
  upload_url_parse = urlparse.urlparse(upload_url)
  upload_key = upload_url_parse.path.split('/')[-1]

  template_values = {
    'sid' : sid,
    'sid_hash' : sidHash(s),
    'hw' : hws[asgn],
    'upload_url' : upload_url,
    'upload_key' : upload_key,
    'submitted_url' : submitted_url,
    'files' : files,
  }
  template_values['hws'] = config.HWS
  return output_template('upload.tpl', template_values)

def cgi_uploadurl(asgn=None, upload_url='', uploadbtn=None):
  s = get_user_info()
  if not s.sid or not asgn or upload_url == '':
    alert('Cannot upload URL')
    back()
    return
  ul = UploadLog()
  ul.filename = upload_url
  ul.assignment = asgn
  ul.sid = s.sid
  ul.action = 'upload_url'
  ul.course_id = s.course_id
  ul.put()
  f = UploadContent(key_name='%s:%s:__url__' % (s.key().name(), asgn))
  f.filename = upload_url
  f.assignment = asgn
  f.sid = s.sid
  f.course_id = s.course_id
  f.put()
  alert('URL uploaded')
  back()

def cgi_rm(asgn=None, filename=None):
  s = get_user_info()
  if not s.sid:
    return cgi_home()
  sid = s.sid
  query = db.Query(UploadContent)
  query.filter('course_id =', s.course_id)
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
  ul.course_id = s.course_id
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
  elif register(sid=sid, name=name, email=email):
    return cgi_home(sid=sid)
  else:
    return cgi_register()

def cgi_admin(sid=None, hw=None, csv=None):
  s = get_user_info()
  admin_sid = s.sid
  if not is_admin(admin_sid):
    return cgi_home()
  if hw != None:
    return cgi_scores(asgn=hw, student_sid=sid)
  course_id = s.course_id  # was config.COURSE_ID
  grade_query = db.Query(Grade)
  grade_query.filter('course_id =', course_id)
  user_query = db.Query(UserInfo)
  user_query.filter('course_id =', course_id)
  user_query.filter('sid !=', None)
  upload_query = db.Query(UploadContent)
  upload_query.filter('course_id =', course_id)
  exam_query = db.Query(Exam)
  exam_query.filter('course_id =', course_id)
  grades = {}
  submitted = {}
  for r in grade_query:
    grade = r.final_score or ""
    pos = grade.find('/') or -1
    if pos != -1: grade = grade[0:pos]
    grades[(r.sid,r.asgn)] = grade.strip()
  for r in upload_query:
    submitted[(r.sid,r.assignment)] = True
  for r in exam_query:
    grades[(r.sid,r.exam_id)] = r.score
  students = []
  for r in user_query:
    info = { 'name' : r.name, 'sid' : r.sid or r.email, 'grades' : [] }
    for hw in config.hws().keys() + config.exams().keys():
      grade = {'asgn' : hw}
      grade['show_link'] = config.exams().has_key(hw) and '0' or '1'
      if grades.has_key((r.sid, hw)):
        grade['score'] = grades[(r.sid, hw)]
      else:
        grade['score'] = ''
      if submitted.has_key((r.sid, hw)):
        grade['submitted'] = '1'
      else:
        grade['submitted'] = '0'
      info['grades'].append(grade)
    info['grades'].sort(key=lambda x: x['asgn'])
    students.append(info)
  students.sort(key=lambda x: x['sid'])
  template_values = {
    'students' : students,
  }
  logging.info(str(template_values))
  if csv:
    headers = {
        'Content-Type' : 'applicaton/csv',
        'Content-Disposition' : 'attachment; filename="grades.csv"',
    }
    return (headers, output_template('tally.tpl', template_values))
  else:
    return output_template('admin.tpl', template_values)

def cgi_home(sid=None):
  s = get_user_info()
  sid = s.sid
  if not sid:
    return cgi_register()
  elif is_admin(sid):
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
  if is_admin(sid):
    student_sid = student_sid or sid
  else:
    student_sid = sid
  course_id = s.course_id

  template_values = {
    'sid' : sid,
    'graders' : config.admins().values(),
    'student_sid' : student_sid,
  }
  if asgn and is_admin(sid):
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
      g.course_id = course_id
      logging.info(g)
      g.put()
  query = db.Query(Grade)
  query.filter('course_id =', course_id)
  query.filter('sid =', student_sid)
  query2 = db.Query(UploadContent)
  query2.filter('course_id =', course_id)
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
  else:
    (hws, idx) = get_hws()
    for r in query:
      logging.info(r.asgn)
      hws[idx[r.asgn]]['final_score'] = r.final_score
      hws[idx[r.asgn]]['has_record'] = 1
    for r in query2:
      hws[idx[r.assignment]]['has_file'] = 1
    for hw in config.HWS:
      if hw.get('hide', 0): del hws[idx[hw['id']]]
    query3 = db.Query(Exam)
    query3.filter('course_id =', course_id)
    query3.filter('sid =', student_sid)
    exams = []
    for r in query3:
      exam_info = { }
      exam_info.update(config.exams()[r.exam_id])
      exam_info['score'] = exam_info.get('letter', 0) and \
          config.projectGrade(r.score) or r.score
      exams.append(exam_info)
    template_values['hws'] = hws
    template_values['exams'] = exams
    logging.info(str(template_values['hws'][0]))
    return output_template('scores.tpl', template_values)

class DownloadHandler(webapp.RequestHandler):
  def get(self):
    s = get_user_info()
    if not is_admin(s.sid) or not self.request.params.has_key('asgn'):
      template_values = { 'hws' : config.HWS, 'exams' : config.EXAMS }
      self.response.out.write(output_template('admin_download.tpl',
                                              template_values))
      return
    zipstream = StringIO.StringIO()
    file = zipfile.ZipFile(zipstream, "w")
    asgn = self.request.params['asgn']
    course = self.request.params.get('course', s.course_id)
    query = db.Query(UploadContent)
    query.filter('course_id =', s.course_id)
    query.filter('assignment =', asgn)
    suffix = self.request.params.has_key('suffix') and \
        str(self.request.params['suffix']) or ""
    for r in query:
      if suffix and not r.sid.endswith(suffix): continue
      if not r.blob_key:
        fn = 'ost_%s/%s.__url__' % (str(r.assignment), str(r.sid or r.email))
        file.writestr(fn, str(r.filename))
      else:
        b = blobstore.BlobReader(r.blob_key)
        fn = 'ost_%s/%s.%s' % (str(r.assignment), str(r.sid or r.email),
                               str(r.filename))
        file.writestr(fn, b.read())
      logging.debug('Wrote file %s' % fn)
    file.close()
    zipstream.seek(0)
    self.response.headers['Content-Type'] = 'applicaton/zip'
    self.response.headers['Content-Disposition'] = \
        'attachment; filename="bundle.zip"'
    self.response.out.write(zipstream.getvalue())

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
      f = UploadContent(key_name='%s:%s:%s' % (s.key().name(), asgn, fn))
      f.filename = fn
      f.assignment = asgn
      f.content_len = str(upload.size)
      f.blob_key = upload.key()
      f.sid = s.sid
      f.course_id = s.course_id
      f.put()

      ul = UploadLog()
      ul.filename = fn
      ul.assignment = asgn
      ul.sid = s.sid
      ul.blob_key = upload.key()
      ul.action = 'upload'
      ul.course_id = s.course_id
      ul.put()

      self.redirect('/grader.cgi?command=upload&asgn=%s' % f.assignment)

class UploadHwHandler(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write(blobstore.create_upload_url('/upload'))

class UploadExamHandler(webapp.RequestHandler):
  def get(self):
    template_values = {
      'hws' : config.HWS,
      'exams' : config.EXAMS,
      'action' : 'upload_exam',
    }
    self.response.out.write(output_template('admin_upload.tpl',
                                            template_values))

  def post(self):
    s = get_user_info()
    if not is_admin(s.sid):
      return
    exam_id = self.request.params.get('exam_id', '')
    if not config.exams().has_key(exam_id):
      return
    csv_file = self.request.get('csv_import')
    fileReader = csv.reader(csv_file.split('\n'))
    self.response.out.write('<h1>%s</h1>\n<pre>' % exam_id)
    count = 0
    for row in fileReader:
      if len(row) == 0: continue
      if len(row) != 3:
        self.response.out.write('skip record: %s\n' % ','.join(row))
        continue
      (sid, name, score) = row
      exam = Exam(key_name='%s:%s' % (sid, exam_id))
      exam.exam_id = exam_id
      exam.sid = sid
      exam.name = name
      exam.score = float(score)
      exam.course_id = s.course_id
      exam.put()
      count += 1
    self.response.out.write('</pre>')
    self.response.out.write('Uploaded %d records' % count)

class UploadCommentsHandler(webapp.RequestHandler):
  def get(self):
    template_values = {
      'hws' : config.HWS,
      'exams' : config.EXAMS,
      'action' : 'upload_comments',
    }
    self.response.out.write(output_template('admin_upload.tpl',
                                            template_values))

  def post(self):
    s = get_user_info()
    logging.debug('here')
    if not is_admin(s.sid):
      return
    exam_id = self.request.params.get('exam_id', '')
    hw_id = ''
    if exam_id:
      if not config.exams().has_key(exam_id): return
    else:
      hw_id = self.request.params.get('hw_id', '')
      if not config.hws().has_key(hw_id): return
    csv_file = self.request.get('csv_import')
    fileReader = csv.reader(csv_file.split('\n'))
    self.response.out.write('<h1>%s</h1>\n<pre>' % exam_id)
    count = 0
    self.response.out.write('</pre>')
    for row in fileReader:
      if len(row) == 0: continue
      if len(row) != 3:
        self.response.out.write('skip record: %s\n' % ','.join(row))
        continue
      (sid, name, comment) = row
      self.response.out.write('Would upload this comment for %s:<br>' % sid)
      self.response.out.write('<pre>\n')
      self.response.out.write(comment.replace('|', '\n'))
      self.response.out.write('</pre>\n')
      if hw_id:
        logging.debug('Lookup grade')
        g = Grade(key_name='%s:%s' % (sid, hw_id))
        g.sid = sid
        g.asgn = hw_id
        g.comments = comment.replace('|', '\n')
        g.course_id = s.course_id
        g.put()
      count += 1
    self.response.out.write('Uploaded %d records' % count)

class SetupHandler(webapp.RequestHandler):
  def get(self):
    config.create_sample_entries()
    self.response.out.write('Done')

class ReqHandler(webapp.RequestHandler):
  def get(self):
    self.post()
  def post(self):
    logging.debug('LOADING')
    args = {}
    params = self.request.params
    for key in params:
      args[str(key)] = params.get(key)
    logging.debug('Got args: %s' % str(args))
    if args.has_key('command') and handlers.has_key('cgi_' + args['command']):
      handler = handlers['cgi_' + args['command']]
      del args['command']
      response = handler(**args)
    else:
      response = cgi_home()
    if type(response) == type(()):
      for k in response[0]:
        self.response.headers[k] = response[0][k]
      response = response[1]
    self.response.out.write(response)

handlers = vars()

def main():
  app = webapp.WSGIApplication([
    ('/',                 ReqHandler),
    ('/grader.cgi',       ReqHandler),
    ('/upload_hw',        UploadHwHandler),
    ('/upload',           UploadHandler),
    ('/upload_exam',      UploadExamHandler),
    ('/upload_comments',  UploadCommentsHandler),
    ('/download',         DownloadHandler),
    ('/setup',            SetupHandler),
  ], debug=True)
  run_wsgi_app(app)

if __name__ == "__main__":
  main()
