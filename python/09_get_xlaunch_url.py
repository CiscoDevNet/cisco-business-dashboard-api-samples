#!/usr/bin/env python3
"""Retrieve a URL to access a device GUI via FindIT Network Manager.

Retrieve a URL to access the specified device's administration GUI through
an instance of Cisco FindIT Network Manager & Probe.  The device ID to be
accessed is passed as a command line option.  The details of the Manager are
contained in the environment.py file.

Note that URL provided may only be accessed from the same IP address that
performs the request.  Any other source IP will be blocked.

Command line arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -d DEVICE, --device DEVICE
                        The nodeId for the device to be accessed.


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
import argparse

import environment
import finditauth

# Get the device nodeId from command line arguments
parser = argparse.ArgumentParser(description='Retrieve a xlaunch URL for the '
                                 'specified device.')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('-d','--device',default=None,
                    help='The nodeId for the device to be accessed.')
args = parser.parse_args()

if (args.device is None):
  print("A device must be specified.")

else:
  # Create a properly formatted JWT using environment data
  token = finditauth.getToken(keyid=environment.keyid,
                              secret=environment.secret,
                              clientid=environment.clientid,
                              appname=environment.appname)

  # Build the API request.  The xlaunch URL request uses a very different
  # path to the other API operations: /controller/xl/{nodeId}?token=SIGNED_JWT
  r = requests.get('https://%s:%s/controller/xl/%s?token=%s' % 
                             (environment.manager, environment.port,
                             args.device,token), allow_redirects=False,
                             verify=environment.verify_mgr_cert)
  print(vars(r.request))
  if r.status_code == 302:                           
    print(r.headers['Location'])
  else:
    print("Unexpected response with status code {}".format(r.status_code))

