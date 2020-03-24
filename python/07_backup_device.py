#!/usr/bin/env python3
"""Backup a device configuration using Cisco Business Dashboard.

Trigger a backup device config action for the specified device or network
using the Cisco Business Dashboard API.  The device/network(s) to be
backed up are passed as command line options.  The details of the Dashboard
are contained in the environment.py file.

Command line arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -d DEVICE, --device DEVICE
                        The nodeId for the device to back up. Multiple IDs may
                        be specified.
  -n NETWORK, --network NETWORK
                        The networkId for the network to back up. Multiple IDs
                        may be specified.
  -c COMMENT, --comment COMMENT
                        A note to be applied to the backup.


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

import requests
import json
import argparse

import environment
import cbdauth

# Get details of device(s) and/or network(s) to back up from command line
# arguments
parser = argparse.ArgumentParser(description='Perform a backup configuration '
                                 'action for the specified device or network.')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('-d','--device',default=None,action='append',
                    help='The nodeId for the device to back up.  Multiple '
                    'IDs may be specified.')
parser.add_argument('-n','--network',default=None,action='append',
                    help='The networkId for the network to back up.  Multiple '
                    'IDs may be specified.')
parser.add_argument('-c','--comment',default=None,
                    help='A note to be applied to the backup.')
args = parser.parse_args()

if (args.device is None) and (args.network is None):
  print("At least one device or network must be specified.")

else:
  # Create a dictionary of the request details, ready for conversion to
  # a JSON payload later
  action = {}
  if args.comment is not None:
    action['comment'] = args.comment
  if args.network is not None:
    action['network-ids'] = args.network
  if args.device is not None:
    action['node-ids'] = args.device

  # Create a properly formatted JWT using environment data
  token = cbdauth.getToken(keyid=environment.keyid,
                           secret=environment.secret,
                           clientid=environment.clientid,
                           appname=environment.appname)

  try:
    # Build and send the API request.  The backup operation API path is
    # /api/v2/nodes/operations/backup-config.  Include the action details
    # dictionary as a JSON payload
    response=requests.post('https://%s:%s/api/v2/nodes/operations/backup-config' % 
                         (environment.dashboard, environment.port),
                         headers={'Authorization':"Bearer %s" % token},
                         json=action,verify=environment.verify_cbd_cert)

  except requests.exceptions.RequestException as e:
    # Generally this will be a connection error or timeout.  HTTP errors are
    # handled in the else section below
    print("Failed with exception:",e)
    sys.exit(1)

  else:
    if response.status_code == 200:
      # Request succeeded
      # The API response payload is a JSON object
      print('Successfully created backup request(s) with job '
            'ID(s): {}'.format(', '.join(response.json()['job-ids'])))
    else:
      # Some other error occurred.
      print('HTTPError:',response.status_code,response.headers)
      
      # Most errors return additional information as a json payload
      if 'application/json' in response.headers['Content-Type']:
        print('Error payload:')
        print(json.dumps(response.json(),indent=2))  
