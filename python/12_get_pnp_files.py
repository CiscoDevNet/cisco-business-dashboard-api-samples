#!/usr/bin/env python3
"""Retrieve a list of PnP files from Cisco FindIT Network Manager.

Query the Cisco FindIT Network Manager API for a list of configuration and
image files available for use with Network Plug and Play.  Two separate API
calls are performed - one for each file type.  The details of the Manager to
query are contained in the environment.py file.

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

import requests
import json
import sys
import argparse

import environment
import finditauth

def doAPIQuery(url,jwt,v=True):
  """
  Query the Cisco FindIT Network Manager API using the provided path and token.
  Returns a JSON object parsed from the response payload.  Exits in the event
  of an error.
  
  Note there is no consideration given here to paging.  So if there are more
  than 20 entries in a query for a list, only the first 20 entries will be
  returned.  
  
  Arguments:
    url - The URL to be queried
    jwt - A properly formatted JWT to use authenticating with the Manager
    v   - Verify the certificate of the Manager.  Set to False for self-
          signed certs
  """
  try:
    # Build and send the API request
    response=requests.get(url,headers={'Authorization':"Bearer %s" % jwt},
                         verify=v)

  except requests.exceptions.RequestException as e:
    # Generally this will be a connection error or timeout.  HTTP errors are
    # handled in the else section below
    print("Failed with exception:",e)
    sys.exit(1)

  else:
    if response.status_code == 200:
      # Request succeeded
      # The API response payload is a JSON object
      return(response.json())
    else:
      # Some other error occurred.
      print('HTTPError:',response.status_code,response.headers)
    
      # Most errors return additional information as a json payload
      if 'application/json' in response.headers['Content-Type']:
        print('Error payload:')
        print(json.dumps(response.json(),indent=2))
      sys.exit(1)

def main():
  # Simple command line arguments for help and version
  parser = argparse.ArgumentParser(description='Retrieve a list of PnP files '
                                   'available in FindIT Network Manager.')
  parser.add_argument('--version', action='version', version='%(prog)s 1.0')
  args = parser.parse_args()

  # Create a properly formatted JWT using 
  token = finditauth.getToken(keyid=environment.keyid,
                              secret=environment.secret,
                              clientid=environment.clientid,
                              appname=environment.appname)

  # Get image list
  imagedata = doAPIQuery('https://%s:%s/api/v2/pnp/images' % 
                         (environment.manager, environment.port),
                         token, environment.verify_mgr_cert)

  # Iterate through the response and print in a nice-ish table
  print('='*48,'PnP Images','='*49)
  print("| {:25} | {:64} | {:10} |".format('File ID','Filename','Size'))
  print('|','-'*25,'+','-'*64,'+','-'*10,'|')
  for image in imagedata['data']:
    print("| {id:25} | {file-name:64} | {file-size:10} |".format(**image))
  print('+','-'*25,'+','-'*64,'+','-'*10,'+','\n')

  # Get config list
  configdata = doAPIQuery('https://%s:%s/api/v2/pnp/configs' % 
                         (environment.manager, environment.port),
                         token, environment.verify_mgr_cert)

  # Iterate through the response and print in a nice-ish table
  print('='*48,'PnP Configs','='*48)
  print("| {:25} | {:64} | {:10} |".format('File ID','Filename','Size'))
  print('|','-'*25,'+','-'*64,'+','-'*10,'|')
  for config in configdata['data']:
    print("| {id:25} | {file-name:64} | {file-size:10} |".format(**config))
  print('+','-'*25,'+','-'*64,'+','-'*10,'+','\n')

if __name__== "__main__":
  main()
