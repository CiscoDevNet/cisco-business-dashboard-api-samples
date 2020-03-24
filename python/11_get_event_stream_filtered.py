#!/usr/bin/env python3
"""Receive a filtered stream of events from Cisco Business Dashboard.

Use the Cisco Business Dashboard API to subscribe to the event stream.
Display a message for each event as it is received.  The stream may be
restricted using command line arguments to only events from specific networks
and events of the specified types.  The details of the Dashboard to receive
events from are contained in the environment.py file.

Command line arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -n NETID, --netid NETID
                        Network ID to monitor. May be used multiple times.
                        Default is all networks.
  -t {action,config_change,event,state_change}, --type {action,config_change,event,state_change}
                        Event type to monitor. Valid options are action,
                        config_change, event and state_change. May be used
                        multiple times. Default is all.


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
import cbdauth

# Get details of event(s) to display from command line arguments
#
# In this example, the only parameter is a simple search string.
parser = argparse.ArgumentParser(description='Get an event stream filtered '
                                 'by network ID, severity, or devices that '
                                 'match the specified search string.')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('-n','--netid',default=None,action='append',
                    help='Network ID to monitor.  May be used multiple times.'
                    '  Default is all networks.')
parser.add_argument('-t','--type',
                    choices=['action','config_change','event','state_change'],
                    default=None,action='append',
                    help='Event type to monitor.  Valid options are '
                    'action, config_change, event and state_change.  May be '
                    'used multiple times.  Default is all.')
args = parser.parse_args()

# Create a properly formatted JWT using environment data
token = cbdauth.getToken(keyid=environment.keyid,
                         secret=environment.secret,
                         clientid=environment.clientid,
                         appname=environment.appname,
                         lifetime=3600)

# First is to subscribe to the networks specified on the command line
if args.netid is not None:
  # Create a dictionary listing the desired networks, ready for conversion to
  # a JSON payload later
  netids = {
    'network-ids':args.netid
  }

  try:
    # Build and send the API request.  The event subscription API path is
    # /api/v2/subscription.  Include the netids dictionary as a JSON
    # payload
    response=requests.post('https://%s:%s/api/v2/subscription' % 
                         (environment.dashboard, environment.port),
                         headers={'Authorization':"Bearer %s" % token},
                         json=netids,verify=environment.verify_cbd_cert)

  except requests.exceptions.RequestException as e:
    # Generally this will be a connection error or timeout.  HTTP errors are
    # handled in the else section below
    print("Failed with exception:",e)
    sys.exit(1)

  else:
    if response.status_code == 204:
      # Request succeeded.  Note that success is a 204 staus with no payload.
      print('Successfully subscribed to networks with ID(s) {}'.format(", ".join(args.netid)))
    else:
      # Some other error occurred.
      print('HTTPError:',response.status_code,response.headers)
      
      # Most errors return additional information as a json payload
      if 'application/json' in response.headers['Content-Type']:
        print('Error payload:')
        print(json.dumps(response.json(),indent=2))
      sys.exit(1)


# Now that we have created our network subscription, 
try:
  while True:
    url = 'https://%s:%s/api/v2/event-source' % (environment.dashboard,
                                                 environment.port)
    if args.type is not None:
      url += "?types=" + ",".join(args.type)
    else:
      url += "?types=action,config_change,event,state_change"
    if args.netid is not None:
      url += "&monitored-networks=subscribed"
    else:
      url += "&monitored-networks=all"

    events = sseclient.SSEClient(url,
                                 headers={'Authorization':"Bearer %s" % token},
                                 verify=environment.verify_cbd_cert)
    try:
      for ev in events:
        event = json.loads(ev.data)
        if event['type'] == '/heart_beat':
          print("Received heartbeat from Dashboard.")
        else:
          # Use the event content to generate a human readable english string
          print("Received event: ",event['english-string'].format(**event['parameters']))
    except requests.exceptions.HTTPError as e:
      # HTTP error from the server
      print('HTTPError: {}'.format(e.response.status_code))
      if e.response.status_code == 401:
        print("JWT Expired.  Create a new one.")
        token = cbdauth.getToken(keyid=environment.keyid,
                                 secret=environment.secret,
                                 clientid=environment.clientid,
                                 appname=environment.appname,
                                 lifetime=3600)
      else:
        print(vars(e.response))
    except KeyboardInterrupt:
      raise

except KeyboardInterrupt:
  print("Exiting.  Goodbye!")  
