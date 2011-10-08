import cgi
import os

# Verify homework 1: Make sure file has correct fields
def hw1(path):
  fields = [
     'first name',
     'last name',
     'nyu email',
     'preferred email',
     'phone',
     'zip code',
     'favorite url',
     'department',
     'graduation year',
  ]
  msg = ""
  status = 1
  lineno = 0
  for line in open(path, "r"):
    lineno = lineno + 1
    line_orig = line.strip()
    line = line.strip().lower()
    if not line:
      continue
    words = line.split(":")
    if len(words) < 2:
      os.remove(path)
      return (1, "<font size=+3><font color=red><center>ERROR</center></font></font>" \
                 "<b><font size=+2><font color=red>File is in valid:</font>" \
                 " Lines %d is not of format <i>field</i>:" \
                 "<i>value</i></font></b><p>" % lineno)
    if words[0] in fields:
      msg += "<font color=green><tt>%s</tt></font><br>" % cgi.escape(line_orig)
      fields.remove(words[0])
    else:
      msg += "<font color=red><tt>%s</tt></font><br>" % cgi.escape(line_orig)
      status = 0
  if status == 0:
    os.remove(path)
    return (1, "<font size=+3><font color=red><center>ERROR</center></font></font>" \
                 "<br><b><font size=+2><font color=red>Invalid lines (shown in red)" \
                 "</font></font></b><p>" + msg)
  elif len(fields) > 0:
    os.remove(path)
    return (1, "<font size=+3><font color=red><center>ERROR</center></font></font>" \
                 "<br><b><font size=+2><font color=red>Missing field(s):</font><br>" \
                 "<tt>%s</tt></font></b><p>" % ', '.join(fields))
  else:
    return (status, 'Upload successful!<br>' + msg)
