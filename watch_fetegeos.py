#!/usr/bin/env python
# Simple script to watch fetegeo and restart fetegeos whenever a file changes
# Just because I'm too lazy to restart things manually

import os, time, subprocess
from sys import exit

cwd = os.getcwd()

SLEEP_INTERVAL = 5

watch_list = {'files': ['fetegeos'],
              'dirs' : ['Geo']}

modtimes = {}

SERVER_PATH = '%s/fetegeos' % cwd

fetegeos_handle = None

try:
    while True:
        restarted = False
        
        if fetegeos_handle == None:
            fetegeos_handle = subprocess.Popen(SERVER_PATH)
    
        for root, dirs, files in os.walk(cwd):
            for this_file in files:
                # Strip the first len(cwd) + 1 characters off the root to give us only the local part of the dir path
                if (this_file in watch_list['files'] or root[len(cwd)+1:] in watch_list['dirs']) and not this_file.endswith('.pyc'):
                    key = "%s/%s" % (root, this_file)
                
                    modified = os.stat(key).st_mtime
                    try:
                        if modtimes[key] != modified:
                            modtimes[key] = modified
                            # Dont restart the server again if it's already been done this run
                            if not restarted:
                                print '%s has changed - restarting fetegeos\n%s\n' % (key, '='*80)
                                fetegeos_handle.terminate()
                                fetegeos_handle = subprocess.Popen(SERVER_PATH)
                                restarted = True
                                
                    except KeyError:
                        modtimes[key] = modified
    
        time.sleep(SLEEP_INTERVAL)
except KeyboardInterrupt:
    fetegeos_handle.terminate()
    exit(0)