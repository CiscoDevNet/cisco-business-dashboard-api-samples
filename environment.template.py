#!/usr/bin/env python3
"""FindIT Network Manager environment variables

Basic environmental parameters required for using the FindIT Network Manager
API version 2.  Replace with values appropriate to your environment.
"""
manager = 'findit-manager.example.com'
port = '443'

# Set the following parameter to False if the Manager certificate is self-signed
verify_mgr_cert = True

# Generate an access key from the Administration > Users page of the FindIT
# Network Manager GUI.
keyid = '<access key id>'
secret = '<access key secret>'

# The appname should be unique to the application.  Recommended format is in
# domain name format
appname = 'examples.findit.cisco.com'

# Provide a string identifier for this application instance.  A UUID is
# recommended.  Set clientid to None to generate a UUID dynamically
clientid = None
