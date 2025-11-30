# Web tool to Assist Liver Transplant Diagnosis

## Introduction

This program provides a web interface to identify the most suitable liver transplant protocols based on patients' diagnoses.

## Requirements

* [Python](https://www.python.org/) 3.8 or later
* `pip` and the `venv` module for Python
* [Flask](https://flask.palletsprojects.com) 2.1.1 or later.

## Installation

### Quick setup

* On Windows, run `script/deploy_win.bat` in a console or from the file manager.
The script will ensure that Python is installed and the work environment for the server is present.
If not present, Python will be automatically installed and the virtual environment created.
* On Mac OS X, run `script/deploy_mac.command` in a terminal or from the Finder.
The script will check that Python is installed and the work environment for the server is present.
Note that if Python is not installed, the script will use [Homebrew](https://brew.sh) to install it.
If Homebrew is not present, the script will try to install it first.
**Administrator rights are needed to install Homebrew!**
* On Linux, `run script/deploy_lin.sh` in a terminal.
Note that Python must be installed beforehand.
If not present, the script will stop.
The script will install the work environment if necessary and deploy the server.

> The scripts need to create a directory at the root of the user home directory to install the work environment for the tool.

### Advanced usage

#### Installation

##### Prerequisites

* Python 3.8 or later installed and available in the environment path.
* The `pip` package manager for Python.
* The `venv` module for the version of Python used.
This is typically installed with standard Python packages but may not be installed automatically on some distributions.

##### Steps

A few notes in advance: for convenience, we will assume the following:

* The Python interpreter is called with the executable `python`.
This may change from installation to installation and the executable should be replaced with the correct executable on your machine.
* As recommended by the Python community, and enforced since Python 3.10, we will use a virtual environment, created specifically for the tool, and located in `${HOME}/venv-lt_clear`.
If you want to use an existing virtual environment or directly use the site installation, simply modify the related commands.

After these preliminary notes, the procedure to install the package would be,

1. Create a new virtual environment with the command

```
python -m venv ${HOME}/venv-lt_clear
```

2. Load the new virtual environment.  The actual command depends on the platform

    * on UNIX (Linux or MacOS X): `source ${HOME}/venv-lt_clear/bin/activate`
    * on Windows with Powershell: `. ${HOME}/venv-lt_clear/Scripts/Activate.ps1`

3. Install the `web-lt_clear` package.
Assuming the package has been downloaded into `${HOME}/Downloads`, run

```
pip install ${HOME}/Downloads/web-lt_clear/
```
`pip` will install the dependencies necessary for the web tool, including the *_Flask_* server.

#### Usage

Once the work environment has been installed, using the server is simple:

1. Open a terminal
2. "Source" the virtual environment
    * on UNIX (Linux or MacOS X): `source ${HOME}/venv-lt_clear/bin/activate`
    * on Windows with Powershell: `. ${HOME}/venv-lt_clear/Scripts/Activate.ps1`
3. Run the app `lt_clear_app`
4. Open a web browser and connect to `127.0.0.1:5000`.

The server can be stopped with CTRL+C.
