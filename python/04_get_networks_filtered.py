#!/usr/bin/env python3
"""Retrieve a filtered list of networks from Cisco Business Dashboard.

Query the Cisco Business Dashboard API for a list of networks that match
the supplied search string.  Only the network name and ID are returned.  The
details of the Dashboard to query are contained in the environment.py file.

Command line arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -s SEARCH, --search SEARCH
                        Display only networks that contain the search string.


Copyright (c) 2020 Cisco and/or its affiliates.

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
import urllib.parse
import json
import argparse

import environment
import cbdauth

# Get details of network(s) to display from command line arguments
#
# In this example, the only parameter is a simple search string.
parser = argparse.ArgumentParser(description='Get a list of networks filtered '
                                 'by the specified search string.  Returns only'
                                 ' the network name and network ID.')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('-s','--search',default=None,help='Display only networks '
                    'that contain the search string.')
args = parser.parse_args()

# Create a properly formatted JWT using environment data
token = cbdauth.getToken(keyid=environment.keyid,
                    	 secret=environment.secret,
                         clientid=environment.clientid,
                         appname=environment.appname)

# Build the API request URL.  The getNetworks API path is /api/v2/networks
url = 'https://%s:%s/api/v2/networks' % (environment.dashboard, environment.port)

# Specify the fields to be returned as query parameters
url = url + '?fields=name,network-id'

# Append the search string as a query parameter
if args.search:
  url = url + '&search=' + urllib.parse.quote(args.search)

try:
  # Build and send the API request.
  response=requests.get(url,headers={'Authorization':"Bearer %s" % token},
                        verify=environment.verify_cbd_cert)

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
