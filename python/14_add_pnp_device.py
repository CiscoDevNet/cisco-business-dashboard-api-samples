#!/usr/bin/env python3
"""Add a new PnP-enabled device to Cisco Business Dashboard.

Create a new PnP-enabled device record using the Cisco Business Dashboard
API.  All parameters are specified with command linbe arguements, and the
majority of parameters must be specified, with only the image and config file
being optional.  The details of the Dashboard to update are contained in the
environment.py file.

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
import cbdauth

# Get details of network to create from command line arguments
#
# For this example, we will keep it simple and only collect the mandatory
# parameters - network name and organization ID - plus the description.
parser = argparse.ArgumentParser(description='Create a new PnP-enabled device.')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('-n','--name',required=True,help='A name for the device')
parser.add_argument('-t','--type',choices=['Router', 'Switch', 'WAP'],
                    required=True,help='The type of device')
parser.add_argument('-p','--pid',required=True,help='The device product ID')
parser.add_argument('-s','--sn',required=True,help='The device serial number')
parser.add_argument('-g','--group',required=True,help='The device group ID for'
                    ' the device.')
parser.add_argument('--net',required=True,help='The network ID for the device.')
parser.add_argument('-i','--image',default=None,help='The image file ID.')
parser.add_argument('-c','--config',default=None,help='The config file ID.')
args = parser.parse_args()

# Create a dictionary of the new device's details, ready for conversion to
# a JSON payload later
device = {
  'device-name':args.name,
  'node-type':args.type,
  'pid':args.pid,
  'sn':args.sn,
  'group-id':args.group,
  'network-id':args.net,
  'image-id':args.image,
  'config-id':args.config
}

# Create a properly formatted JWT using environment data
token = cbdauth.getToken(keyid=environment.keyid,
                         secret=environment.secret,
                         clientid=environment.clientid,
                         appname=environment.appname)

try:
  # Build and send the API request.  The createPnpDevice API path is
  # /api/v2/pnp/devices.  Include the device details dictionary as a JSON
  # payload
  response=requests.post('https://%s:%s/api/v2/pnp/devices' % 
                       (environment.dashboard, environment.port),
                       headers={'Authorization':"Bearer %s" % token},
                       json=device,verify=environment.verify_cbd_cert)

except requests.exceptions.RequestException as e:
  # Generally this will be a connection error or timeout.  HTTP errors are
  # handled in the else section below
  print("Failed with exception:",e)
  sys.exit(1)

else:
  if response.status_code == 200:
    # Request succeeded
    # The API response payload is a JSON object
    print('Successfully created device with ID {}'.format(response.json()['id']))
  else:
    # Some other error occurred.
    print('HTTPError:',response.status_code,response.headers)
    
    # Most errors return additional information as a json payload
    if 'application/json' in response.headers['Content-Type']:
      print('Error payload:')
      print(json.dumps(response.json(),indent=2))
