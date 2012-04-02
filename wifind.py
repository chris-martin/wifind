from IWList import IWList

import sys, re
from os import path
import subprocess
from time import sleep

def is_match(x):
  if ignore(x): return False
  return ssid(x) or mac(x)

def ssid(x):
  regex = get_file_line('ssid')
  return re.match(regex, x['ESSID'], re.I)

def mac(x):
  regex = get_file_line('mac')
  return re.match(regex, x['MAC'], re.I)

def ignore(x):
  return path.exists('ignore') and x['ESSID'] in get_file_lines('ignore')

def get_file_line(x):
  lines = list(get_file_lines(x))
  return lines[0] if len(lines) else None

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
      print(set(map(lambda x: x['ESSID'], candidates)))
      found = search(candidates)
      print(found)
      sys.stdout.flush()

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
 
