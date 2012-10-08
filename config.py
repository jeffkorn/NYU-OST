import verify
import math

ADMINS = {
  'N00000000' : 'Prof. Korn',
  'N11887225' : 'Praveen Thirukonda',
  'N19223762' : 'Deniz Ulema',
}

HWS = [
  {
    'id' : 'hw0',
    'due': '9/17/12 before class',
    'asgn': 'Assignment 0',
    'url': 'http://www.cs.nyu.edu/courses/fall12/CSCI-GA.3033-004/asgn/as0.html',
    'submit_url' : 0,
    'grades_released' : 0,
    'verify' : verify.hw1
  },
  {
    'id' : 'hw1',
    'due': '10/3/12 11:59PM',
    'asgn': 'Assignment 1',
    'url': 'https://docs.google.com/document/pub?id=1-sYCpnhCW2cJLglLfoVB4ieERkY3Btsw7XqppwSz5KY',
    'submit_url' : 0,
    'grades_released' : 0,
  },
]

UNASSIGNED_HWS = [
  {
    'id' : 'hw1',
    'due': '9/29/11 before class',
    'asgn': 'Assignment 1',
    'url': 'https://docs.google.com/document/pub?id=1C6lb1j3SZ7kc6OWzdXer1zUJSLMwz3bxQI2G-7Tw29g',
    'submit_url' : 0,
    'grades_released' : 1,
  },
  {
    'id' : 'hw2',
    'due': '10/20/11 before class',
    'asgn': 'Assignment 2',
    'url': 'https://docs.google.com/document/pub?id=15NUnbu360hGM7-_qiLdmnGaASVcSRzXgvGFcfjjMOhw',
    'submit_url' : 0,
    'grades_released' : 1,
  },
  {
    'id' : 'hw3',
    'due': '11/10/11 before class',
    'asgn': 'Assignment 3',
    'url': 'https://docs.google.com/document/pub?id=1Q5OsJR5weGJaHIgSXVvr0AOFxGLG-1v0ZBTQT8ztBa0',
    'submit_url' : 0,
    'grades_released' : 1,
  },
  {
    'id' : 'hw4',
    'due': '12/1/11 before class',
    'asgn': 'Assignment 4',
    'url': 'https://docs.google.com/document/pub?id=1b1AIcL8Sn5vN0zh5mkw5kDaSl8AAaWp0ysYlH9IjW44',
    'submit_url' : 1,
    'grades_released' : 1,
  },
  {
    'id' : 'prj',
    'due': 'Due 12/l8, 2011 11:59',
    'asgn': 'Final Project',
    'url': 'https://docs.google.com/document/pub?id=1kEIuoHjGbZ54pbJ0Xiv4N0NQGf1kzQqLMTqUNkGKXMg',
    'submit_url' : 1,
    'grades_released' : 0,
    'hide' : 1,
  },
]

def projectGrade(points):
  if points == 100:
    grade = 'A+'
  elif points >= 95:
    grade = 'A'
  elif points >= 90:
    grade = 'A-'
  elif points >= 85:
    grade = 'B+'
  elif points >= 80:
    grade = 'B'
  elif points >= 75:
    grade = 'B-'
  elif points >= 70:
    grade = 'C+'
  elif points >= 60:
    grade = 'C'
  else:
    grade = 'F'
  return grade

#def projectGrade(points):
#  if points >= 90:
#    grade = 'A+'
#  elif points >= 85:
#    grade = 'A'
#  elif points > 75:
#    grade = 'A-'
#  elif points >= 75:
#    grade = 'B+'
#  elif points > 65:
#    grade = 'B'
#  elif points >= 65:
#    grade = 'B-'
#  elif points > 50:
#    grade = 'C+'
#  elif points >= 40:
#    grade = 'C'
#  else:
#    grade = 'F'
#  return grade

EXAMS = [
  {
    'id' : 'test1',
    'name': 'Midterm',
    'file': '/home/unixtool/private/2010/midterm.csv',
    'grades_released' : 1,
#    'adjust' : lambda x: pow(x,.75) * pow(100,.25) + 12,
#     'adjust' : lambda x: pow(x,.75) * pow(100,.25),
#    'adjust' : lambda x: math.sqrt(x)*10,
   'adjust' : lambda x: 50.5 + (x/2),
    'letter' : 0,
  },
  {
    'id' : 'test2',
    'name': 'Final',
    'file': '/home/unixtool/private/2010/final.csv', 
    'grades_released' : 0,
#    'adjust' : lambda x: math.sqrt(x+7)*10-1.5,
    'adjust' : lambda x: 50 + (x/2),
    'letter' : 0,
  },
  {
    'id' : 'project',
    'name': 'Final Project',
    'grades_released' : 0,
    'letter' : 1,
  },
]
 
UNASSIGNED_EXAMS = {
  'test3': {
    'name': 'Project',
    'file': '/home/unixtool/private/2009/proj.csv', 
    'grades_released' : 1,
    'adjust' : lambda x: x + 10,
    'letter' : 1,
    'letter_convert' : lambda x : projectGrade(int(x)),
  },
}

######

HW_MAP = {}
for hw in HWS:
  HW_MAP[hw['id']] = hw
EXAM_MAP = {}
for exam in EXAMS:
  EXAM_MAP[exam['id']] = exam

def admins():
  return ADMINS

def hws():
  return HW_MAP

def exams():
  return EXAM_MAP
