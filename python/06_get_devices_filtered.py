#!/usr/bin/env python3
"""Retrieve a filtered list of devices from Cisco Business Dashboard.

Query the Cisco Business Dashboard API for a list of devices that match
the supplied search string and device type(s).  Outputs a JSON object
containing the hostname, device type, IP address and serial number.  The
details of the Dashboard to query are contained in the environment.py file.

Command line arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -s SEARCH, --search SEARCH
                        Display only devices that contain the search string.
  -t TYPE, --type TYPE  Display only devices of the specified type(s). Should
                        be one of the following: All, Device, Others, Router,
                        Switch, WAP, IpPhone, IpCamera, NAS, VirtualDevice, or
                        WLC. Defaults to Device. May be specified multiple
                        times.


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

# Get details of network to create from command line arguments
#
# For this example, we allow the user to specify the type(s) of devices
# to return, plus a search string to further restrict the output
parser = argparse.ArgumentParser(description='Get a list of devices filtered '
                                 'by the specified search string and device '
                                 'type.  Returns only the device hostname, '
                                 'type, IP address and serial number.')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('-s','--search',default=None,help='Display only devices '
                    'that contain the search string.')
parser.add_argument('-t','--type',action='append',help='Display only devices '
                    'of the specified type(s).  Should be one of the following:'
                    ' All, Device, Others, Router, Switch, WAP, IpPhone, '
                    'IpCamera, NAS, VirtualDevice, or WLC.  Defaults to Device.'
                    '  May be specified multiple times.')
args = parser.parse_args()

# Create a properly formatted JWT using environment data
token = cbdauth.getToken(keyid=environment.keyid,
                         secret=environment.secret,
                         clientid=environment.clientid,
                         appname=environment.appname)

# Build the API request URL.  The getNodes API path is /api/v2/nodes
url = 'https://%s:%s/api/v2/nodes' % (environment.dashboard, environment.port)

# Specify the fields to be returned as query parameters
#
# Note: some additional fields such as network and organization will always
# be returned
url += '?fields=/system-state/hostname,/system-state/type,'
url += '/system-state/ip,/system-state/sn'

# Append the list of types as a query parameter.
# If not specified, use Device (Router+Switch+WAP)
if args.type:
  for type in args.type:
    url += '&type=' + urllib.parse.quote(type)
else:
  url += '&type=Device'
  
# Append the search string as a query parameter
if args.search:
  url += '&search-str=' + urllib.parse.quote(args.search)

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
