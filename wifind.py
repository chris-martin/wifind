from IWList import IWList

import sys, re
from os import path
import subprocess
from time import sleep

def is_match(x):
  return regex(x) and not ignore(x)

def regex(x):
  return re.match(sys.argv[2], x['ESSID'], re.I)

def ignore(x):
  return path.exists('ignore') and x['ESSID'] in get_file_lines('ignore')

def get_file_lines(x):
  if not path.exists(x): return []
  return map(lambda s: s.strip(), open(x, 'r').readlines())

def all():
  iwl = IWList(sys.argv[1])
  return list(iwl.getData().values())

def search(candidates):
  return list(filter(is_match, candidates))

if __name__  ==  '__main__':
  while True:
    try:
      candidates = all()
      found = search(candidates)
      print(found)

      if len(found): 
        subprocess.call('beep -f 1200 -l 200 -r 3', shell=True)
      elif len(candidates):
        subprocess.call('beep -f 500 -l 80', shell=True)
      else: 
        sleep(1)
    except KeyboardInterrupt:
      sys.exit()
    except:
      pass
 
