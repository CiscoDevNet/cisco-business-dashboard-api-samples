# FindIT Network Manager API Samples

This project contains sample scripts demonstrating usage of the FindIT Network Manager API, using Python.

The concepts and techniques shown can be extended to enable programmatic access to allow visibility and management of Cisco 100 to 500 Series network devices through FindIT Network Manager.  The sample scripts included are simple and intended to demonstrate the capabilities and use of the API.  They should not be used for production purposes without significant modifications.

(ToDo) Also included is a Postman collection covering the requests used in the sample.

These scripts require the use of FindIT Network Manager release 2.0 or higher.

## Getting started
(Verify This)
* Install Python 3:

    On Windows, choose the option to add to PATH environment variable

* Clone this repo:

    ```bash
    git clone https://github.com/CiscoDevNet/findit-network-manager-api-samples.git
    cd findit-network-manager-api-samples
    ```

* Dependency Installation (you may need to use `pip3` on Linux or Mac)

    ```bash
    pip install -r requirements.txt
    ```

* Copy `environment.template.py` to `environment.py` and edit to specify the details of your FindIT Network Manager instance

## Usage

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

## Getting help

More information about the FindIT Network Manager API may be found at (devnet URL) or by browsing to https://your_manager_address/api/.  You may contact Cisco Developer Support (url) for assistance with the use of the API.

If you experience any issues with the installation, configuration or operation of FindIT Network Manager or Cisco 100 to 500 series products, contact the Small Business TAC using the contacts found at https://www.cisco.com/go/sbsc.

If you have any questions, concerns, or bug reports associated with the sample scripts contained in this repository, please file an issue in the [Issue Tracker](./issues).

## Getting involved

Any suggestions and enhancements to these sample scripts are welcome.  See [CONTRIBUTING](./CONTRIBUTING.md) for more information on how to contribute.


----

## Licensing info

This code is licensed under the Cisco Sample Code License, Version 1.1. See [LICENSE](./LICENSE) for details.
