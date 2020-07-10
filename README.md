# Cisco Business Dashboard API Samples

This project contains sample scripts demonstrating usage of the Cisco Business Dashboard API, using Python.

The concepts and techniques shown can be extended to enable programmatic access to allow visibility and management of Cisco Business network devices through Cisco Business Dashboard.  The sample scripts included are simple and intended to demonstrate the capabilities and use of the API.  They should not be used for production purposes without significant modifications.

Also included is a Postman collection and environment covering the requests used in the sample.

These scripts require the use of Cisco Business Dashboard release 2.2 or higher.

## Getting started with Python
* Install Python 3 (this is usually installed by default on Linux or Mac)

* Clone this repo and then change to the directory containing the python samples:

    ```bash
    git clone https://github.com/CiscoDevNet/cisco-business-dashboard-api-samples.git
    cd cisco-business-dashboard-api-samples/python
    ```

* Optionally setup a python virtual environment (see https://docs.python.org/3/tutorial/venv.html for more detail on virtual environments)

    ```bash
    python3 -m venv venv
	source venv/bin/activate
    ```
	On Windows, the commands to set up the virtual environment are slightly different:
	
	```bash
    py.exe -m venv venv
	venv\Scripts\activate.bat
    ```

* Dependency Installation (you may need to use `pip3` on Linux or Mac)

    ```bash
    pip install -r requirements.txt
    ```

* Copy `environment.template.py` to `environment.py` and edit to specify the details of your Cisco Business Dashboard instance

### Usage

Each script other than environment.py may be executed by passing the script name to the python3 interpreter as follows:

```bash
python3 01_get_organizations.py
```


Several of the scripts require additional information to be passed as command line parameters, and some allow command line options to further control behaviour.  If required parameters are omitted, and error will be generated.  For example:

```bash
$ python3 03_get_networks_by_org.py
usage: 03_get_networks_by_org.py [-h] [--version] orgid
03_get_networks_by_org.py: error: the following arguments are required: orgid
$
```

Available command line options may be displayed by specifying the `-h` or `--help` option as follows:

```bash
$ python3 03_get_networks_by_org.py --help
usage: 03_get_networks_by_org.py [-h] [--version] orgid

List all networks belong to the specified organization.

positional arguments:
  orgid       The ID of the organization

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
$
```

## Getting started with Postman
* Install Postman (See https://learning.postman.com/docs/getting-started/installation-and-updates/ for instructions)

* Clone this repo

    ```bash
    git clone https://github.com/CiscoDevNet/cisco-business-dashboard-api-samples.git
    ```

* Import the collection and environment files located in the cisco-business-dashboard-api-samples/postman directory into Postman.  See https://learning.postman.com/docs/getting-started/importing-and-exporting-data/ for more details on this process.

* Select the imported environment using the dropdown at the top right of the postman window and then click the environment quick view button next to the dropdown.  Fill out the fields for the Dashboard address, keyid and keysecret.

	To get a keyid and keysecret, log on to the GUI of the Dashboard and click on the username displayed at the bottom of the navigation bar.  On the user profile page display, click the Generate Access Key button to create a new access key id and secret.  Note that the secret is only displayed once so be sure to record it somewhere safe.  For more details on generating and managing access keys, consult the Cisco Business Dashboard administration guide found at https://cisco.com/go/cbd-docs.
	
* Before executing any of the other requests in the collection, make sure you execute the _Generate JWT using the RSA-Sign Crypto Library_ request.  This request uses the keyid and keysecret parameters from the environment to generate a JSON Web Token (JWT) that can be used to authenticate subsequent requests with the Dashboard.  The JWT is stored in the environment variable jwt_token.

* You may then execute any of the other requests in the collection in any order.  Some requests will request query parameters to be specified, and occasionally these parameters will be id's used by Dashboard to uniquely identify networks or devices or organizations.  These identifiers may be determined using requests higher up in the collection.

## Getting help

More information about the Cisco Business Dashboard API may be found at (devnet URL) or by browsing to https://your_dashboard_address/api/.  You may contact Cisco Developer Support (url) for assistance with the use of the API.

If you experience any issues with the installation, configuration or operation of Cisco Business Dashboard or Cisco Business products, contact the Small Business TAC using the contacts found at https://www.cisco.com/go/sbsc.

If you have any questions, concerns, or bug reports associated with the sample scripts contained in this repository, please file an issue in the [Issue Tracker](./issues).

## Getting involved

Any suggestions and enhancements to these sample scripts are welcome.  See [CONTRIBUTING](./CONTRIBUTING.md) for more information on how to contribute.


----

## Licensing info

This code is licensed under the Cisco Sample Code License, Version 1.1. See [LICENSE](./LICENSE) for details.
