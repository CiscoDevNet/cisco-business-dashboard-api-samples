#!/usr/bin/env python3
"""Retrieve networks from FindIT Network Manager belonging to an organization.

Query the Cisco FindIT Network Manager API for a list of networks that belong
to the specified organization ID.  The details of the Manager to query are
contained in the environment.py file.

Command line arguments:
  positional arguments:
    orgid       The ID of the organization

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

import requests
import json
import argparse

import environment
import finditauth

# Get desired organization ID from command line argument
parser = argparse.ArgumentParser(description='List all networks belong to the '
                                 'specified organization.')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('orgid',help='The ID of the organization')
args = parser.parse_args()

# Create a properly formatted JWT using environment data
token = finditauth.getToken(keyid=environment.keyid,
                            secret=environment.secret,
                            clientid=environment.clientid,
                            appname=environment.appname)

try:
  # Build and send the API request.  The getNetworks API path is
  # /api/v2/networks.  The x-ctx-org-id header is used to restrict the
  # results to the specified org.
  response=requests.get('https://%s:%s/api/v2/networks' % 
                       (environment.manager, environment.port),
                       headers={'Authorization':"Bearer %s" % token,
                                'x-ctx-org-id':args.orgid },
                       verify=environment.verify_mgr_cert)

except requests.exceptions.RequestException as e:
  # Generally this will be a connection error or timeout.  HTTP errors are
  # handled in the else section below
  print("Failed with exception:",e)
  sys.exit(1)

else:
  if response.status_code == 200:
    # Request succeeded
    # The API response payload is a JSON object
    print(json.dumps(response.json(),indent=2))
  else:
    # Some other error occurred.
    print('HTTPError:',response.status_code,response.headers)
    
    # Most errors return additional information as a json payload
    if 'application/json' in response.headers['Content-Type']:
      print('Error payload:')
      print(json.dumps(response.json(),indent=2))
