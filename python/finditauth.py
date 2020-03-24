#!/usr/bin/env python3
"""Generate an authentication token for use with Cisco Business Dashboard

When executed standalone, this utility will output a JWT suitable for use
with the Cisco Business Dashboard API based on data provided through command line
arguments.

When used as a module, provides the getToken function that returns a JWT.

Command line arguments:
  positional arguments:
    keyid                 The ID of the Access Key
    secret                The secret value of the Access Key

  optional arguments:
    -h, --help            show this help message and exit
    --version             show program's version number and exit
    -c CLIENTID, --clientid CLIENTID
                          The ID for this instance of the client application. A
                          random UUID will be generated if this parameter is not
                          set.
    -n NAME, --name NAME  The name to use for the client application. Defaults
                          to cbdauth.example.com.
    -v APPVER, --appver APPVER
                          The version string to use for the client application.
                          Defaults to 1.0.
    -l LIFETIME, --lifetime LIFETIME
                          The duration in seconds the token will remain valid.
                          Defaults to 3600 (one hour).


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

import jwt
import json
import uuid
import time
import argparse

def getToken(keyid,secret,clientid=None,appname="cbdscript.example.com",appver="1.0",lifetime=3600):
  """
  Generate a JWT suitable for use with version 2 of the Cisco Business
  Dashboard API.

  Arguments:
    keyid    - The key ID from the Access Key defined on the Dashboard
    secret   - The secret value for the Access Key defined on the Dashboard
    clientid - (Optional) A unique ID (UUID recommended) for the instance of
               the client application.  If not specified, a random UUID is
               generated.
    appname  - (Optional) A name to identify the application in domain name
               format.  If not specified, the string 'cbdscript.example.com'
               is used.
    appver   - (Optional) The version of the application.  If not specified,
               the string '1.0' is used.
    lifetime - (Optional) The length of time in seconds the JWT should remain
               valid.  Defaults to 3600 seconds (one hour).
  """
  if clientid == None:
    clientid = str(uuid.uuid4())

  claimset = {
    "iss":appname,
    "cid":clientid,
    "appver":appver,
    "aud":"business-dashboard.cisco.com",
    "iat":int(time.time()),
    "exp":int(time.time()+lifetime)
  }

  return jwt.encode(claimset,secret,algorithm='HS256',headers={'kid':keyid}).decode('UTF-8')

def getArgs():
  # Use argparse to collect user input
  parser = argparse.ArgumentParser(description='Generate an authentication '
                                   'token for use with version 2 of the Cisco '
                                   'Cisco Business Dashboard API.')
  parser.add_argument('--version', action='version', version='%(prog)s 1.0')
  parser.add_argument('keyid',help='The ID of the Access Key')
  parser.add_argument('secret',help='The secret value of the Access Key')
  parser.add_argument('-c','--clientid',default=str(uuid.uuid4()),help='The ID'
                      ' for this instance of the client application.  A random'
                      ' UUID will be generated if this parameter is not set.')
  parser.add_argument('-n','--name',default='cbdauth.example.com',
                      help='The name to use for the client application.  '
                      'Defaults to cbdauth.example.com.')
  parser.add_argument('-v','--appver',default='1.0',help='The version string '
                      'to use for the client application.  Defaults to 1.0.')
  parser.add_argument('-l','--lifetime',type=int,default=3600,
                      help='The duration in seconds the token will remain '
                      'valid.  Defaults to 3600 (one hour).')
  return parser.parse_args()
  
def main():
  # If executed standalone, then collect the necessary parameters from the
  # command line and print out the resulting JWT.
  args = getArgs()
  print(getToken(args.keyid,args.secret,args.clientid,args.name,args.appver,args.lifetime))
  
if __name__== "__main__":
  main()
