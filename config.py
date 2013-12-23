import verify
import math

ADMINS = {
  'N00000000' : 'Prof. Korn',
  'N16823985' : 'Libin Lu',
  'N18098909' : 'Shancong Fu',
  'N18962557' : 'Zicong Pan',
  'N19303071' : 'Xu He',
}

HWS = [
  {
    'id' : 'hw0',
    'due': '9/10/13 before class',
    'asgn': 'Assignment 0',
    'url': 'http://www.cs.nyu.edu/courses/fall13/CSCI-GA.3033-004/asgn/as0.html',
    'submit_url' : 0,
    'grades_released' : 0,
    'verify' : verify.hw1
  },
  {
    'id' : 'hw1',
    'due': '9/25/13 11:59PM',
    'asgn': 'Assignment 1',
    'url': 'https://docs.google.com/document/d/1TABTNyDubqUCNR1QNhQsfcOrH0TwY4WL-KuIMi58ZyI/pub',
    'submit_url' : 0,
    'grades_released' : 1,
  },
  {
    'id' : 'hw2',
    'due': '10/10/13 11:59PM',
    'asgn': 'Assignment 2',
    'url': 'https://docs.google.com/document/d/16yr1pHHu-4Sz-MlhlqfmlTIQNdZrtrWFYvXJmwpqY6A/preview',
    'submit_url' : 0,
    'grades_released' : 1,
  },
  {
    'id' : 'hw3',
    'due': '11/4/l3 11:59PM',
    'asgn': 'Assignment 3',
    'url': 'https://docs.google.com/document/d/11JY8QlcvsAE2PDcg7VYMKlUwhJ8GejP1gjkt5wfNdZs/preview',
    'submit_url' : 0,
    'grades_released' : 1,
  },
  {
    'id' : 'hw4',
    'due': '11/27/12 11:59pm',
    'asgn': 'Assignment 4',
    'url': 'https://docs.google.com/document/d/1B7WtrJfTqlfBS6kUuJNvRr5vqkhCZwAnejFPmZEnk2w/preview',
    'submit_url' : 1,
    'grades_released' : 1,
  },
  {
    'id' : 'prj',
    'due': 'Due 12/l6/13 11:59pm',
    'asgn': 'Final Project',
    'url': 'https://docs.google.com/document/d/1UBr8vtkSo0TLfh32ovx8Av0JBXURWMNBo-Fn4ZDoaNM/preview',
    'submit_url' : 1,
    'grades_released' : 1,
    'hide' : 0,
  },
]

UNASSIGNED_HWS = [
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
    'grades_released' : 1,
#    'adjust' : lambda x: math.sqrt(x+7)*10-1.5,
    'adjust' : lambda x: 50 + (x/2),
    'letter' : 0,
  },
  {
    'id' : 'project',
    'name': 'Final Project',
    'grades_released' : 1,
    'letter' : 1,
  },
]
 
UNASSIGNED_EXAMS = [
]

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
