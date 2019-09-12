#!/usr/bin/env python3
"""Receive a stream of events from Cisco FindIT Network Manager.

Use the Cisco FindIT Network Manager API to subscribe to the event stream.
Display a message for each event as it is received.  The details of the
Manager to receive events from are contained in the environment.py file.

Command line arguments:
  optional arguments:
    -h, --help  show this help message and exit
    --version   show program's version number and exit


Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import json
import requests
import argparse

# SSE Client library (https://github.com/btubbs/sseclient)
#
# Use v0.0.22 as 0.0.23-0.0.24 have a bug handling large events
import sseclient

import environment
import finditauth

# Simple command line arguments for help and version
parser = argparse.ArgumentParser(description='Receive an event stream from '
                                 'FindIT Network Manager.')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
args = parser.parse_args()

try:
  token = None
  while True:
    if not token:
      # Create a properly formatted JWT using 
      token = finditauth.getToken(keyid=environment.keyid,
                                  secret=environment.secret,
                                  clientid=environment.clientid,
                                  appname=environment.appname,
                                  lifetime=14400)


    events = sseclient.SSEClient('https://%s:%s/api/v2/event-source?types=action,config_change,event,state_change&monitored-networks=all' % 
                               (environment.manager, environment.port),
                               headers={'Authorization':"Bearer %s" % token},
                               verify=environment.verify_mgr_cert)
    try:
      for ev in events:
        event = json.loads(ev.data)
        if event['type'] == '/heart_beat':
          print("Received heartbeat from Manager.")
        else:
          # Use the event content to generate a human readable english string
          print("Received event: ",event['english-string'].format(**event['parameters']))
    except requests.exceptions.HTTPError as e:
      # HTTP error from the server
      print('HTTPError: {}'.format(e.response.status_code))
      if e.response.status_code == 401:
        print("JWT Expired.  Create a new one.")
        token = None
      else:
        print(vars(e.response))
    except KeyboardInterrupt:
      raise

except KeyboardInterrupt:
  print("Exiting.  Goodbye!")  
