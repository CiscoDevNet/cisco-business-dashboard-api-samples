#!/usr/bin/env python3
"""Add a new network to Cisco FindIT Network Manager.

Create a new network record using the Cisco FindIT Network Manager API.
Only the network name and description are set.  The network name and the ID of
the owning organization must be specified.  The details of the Manager to
update are contained in the environment.py file.

Command line arguments:
  positional arguments:
    name                  The name of the new network
    orgid                 The ID of the organization the network should belong
                          to

  optional arguments:
    -h, --help            show this help message and exit
    --version             show program's version number and exit
    -d DESCRIPTION, --description DESCRIPTION
                          The network description


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
import finditauth

# Get details of network to create from command line arguments
#
# For this example, we will keep it simple and only collect the mandatory
# parameters - network name and organization ID - plus the description.
parser = argparse.ArgumentParser(description='Create a new network with the '
                                 'specified characteristics.')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('name',help='The name of the new network')
parser.add_argument('orgid',help='The ID of the organization the network '
                    'should belong to')
parser.add_argument('-d','--description',default=None,help='The network '
                    'description')
args = parser.parse_args()

# Create a dictionary of the new network's details, ready for conversion to
# a JSON payload later
network = {
  'name':args.name,
  'org-id':args.orgid,
}
if args.description is not None:
  network['description'] = args.description

# Create a properly formatted JWT using environment data
token = finditauth.getToken(keyid=environment.keyid,
                            secret=environment.secret,
                            clientid=environment.clientid,
                            appname=environment.appname)

try:
  # Build and send the API request.  The createNetworks API path is
  # /api/v2/networks
  response=requests.post('https://%s:%s/api/v2/networks' % 
                       (environment.manager, environment.port),
                       headers={'Authorization':"Bearer %s" % token},
                       json=network,verify=environment.verify_mgr_cert)

except requests.exceptions.RequestException as e:
  # Generally this will be a connection error or timeout.  HTTP errors are
  # handled in the else section below
  print("Failed with exception:",e)
  sys.exit(1)

else:
  if response.status_code == 200:
    # Request succeeded
    # The API response payload is a JSON object
    print('Successfully created network with ID {}'.format(response.json()['id']))
  else:
    # Some other error occurred.
    print('HTTPError:',response.status_code,response.headers)
    
    # Most errors return additional information as a json payload
    if 'application/json' in response.headers['Content-Type']:
      print('Error payload:')
      print(json.dumps(response.json(),indent=2))

