import verify
import math

# Directory where submisions will be stored
ROOT = '/home/unixtool/public_html/hw_fall10/hw'

ADMINS = [
  'N00000000',
]

GRADERS = [
  'Prof. Korn',
  'Royston Monteiro',
  'Deniz Ulema',
]

HWS = {
  'hw0': {
    'due': '9/15/11 before class',
    'asgn': 'Assignment 0',
    'url': 'http://www.cs.nyu.edu/courses/fall11/CSCI-GA.3033-005/asgn/as0.html',
    'submit_url' : 0,
    'grades_released' : 0,
    'verify' : verify.hw1
  },
  'hw1': {
    'due': '9/29/11 before class',
    'asgn': 'Assignment 1',
    'url': 'https://docs.google.com/document/pub?id=1C6lb1j3SZ7kc6OWzdXer1zUJSLMwz3bxQI2G-7Tw29g',
    'submit_url' : 0,
    'grades_released' : 0,
  },
  'hw2': {
    'due': '10/20/11 before class',
    'asgn': 'Assignment 2',
    'url': 'https://docs.google.com/document/pub?id=15NUnbu360hGM7-_qiLdmnGaASVcSRzXgvGFcfjjMOhw',
    'submit_url' : 0,
    'grades_released' : 0,
  },
}

UNASSIGNED_HWS = {
  'hw3': {
    'due': '11/16/10 9PM',
    'asgn': 'Assignment 3',
    'url': 'https://docs.google.com/View?id=d45v4sz_28hqhhndkf',
    'submit_url' : 0,
    'grades_released' : 1,
  },
  'hw4': {
    'due': '11/30/10 9PM',
    'asgn': 'Assignment 4',
    'url': 'https://docs.google.com/document/pub?id=10a_BTjfpZASDLcViNz6kovB9GaShjfNc-2ustRd46Jg&pli=1',
    'submit_url' : 1,
    'grades_released' : 1,
  },
 'prj': {
    'due': 'Due 12/l7, 2010 5:00PM',
    'asgn': 'Final Project',
    'url': 'https://docs.google.com/View?docID=0AZzWs1b91j6dZDQ1djRzel81MmZnNHZwOWRt',
    'submit_url' : 1,
    'grades_released' : 1,
    'default' : 1,
  },
}

def projectGrade(points):
  if points >= 90:
    grade = 'A+'
  elif points >= 85:
    grade = 'A'
  elif points > 75:
    grade = 'A-'
  elif points >= 75:
    grade = 'B+'
  elif points > 65:
    grade = 'B'
  elif points >= 65:
    grade = 'B-'
  elif points > 50:
    grade = 'C+'
  elif points >= 40:
    grade = 'C'
  else:
    grade = 'F'
  return grade

EXAMS = { 
  'test1': {
    'name': 'Midterm',
    'file': '/home/unixtool/private/2010/midterm.csv',
    'grades_released' : 1,
#    'adjust' : lambda x: pow(x,.75) * pow(100,.25) + 12,
#     'adjust' : lambda x: pow(x,.75) * pow(100,.25),
#    'adjust' : lambda x: math.sqrt(x)*10,
   'adjust' : lambda x: 50.5 + (x/2),
    'letter' : 0,
  },
  'test2': {
    'name': 'Final',
    'file': '/home/unixtool/private/2010/final.csv', 
    'grades_released' : 1,
#    'adjust' : lambda x: math.sqrt(x+7)*10-1.5,
    'adjust' : lambda x: 50 + (x/2),
    'letter' : 0,
  },
}
 
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

FINAL_GRADES = '/home/unixtool/private/2010/grades.csv'
 
######

def admins():
  return ADMINS

def hws():
  return HWS

def exams():
  return EXAMS

def final_grades():
  return FINAL_GRADES

def graders():
  return GRADERS

def root():
  return ROOT

