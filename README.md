# selectm

Interfaces with a specific site for a specific use.

# System Requirements

* Python3.  
* Only tested on Linux.  Only supported on Linux.

# Installation

## Clone the Repo
First, you'll want to clone the repo to local:

```
git clone https://github.com/cmpunches/selectm.git
```

You should now have a directory in the folder you did this in called `selectm`.

At the time of writing this, that directory should have a structure resembling the following:

```
[ bagira @ forge.silogroup.org ] << ~/development/internal/selectm >>

[- tree
.
├── Conf
│   └── configuration.sample.ini
├── README.md
├── requirements.txt
└── selectm

1 directory, 5 files
```

## Install Dependencies

To be able to execute `selectm` you will need to install the dependencies.  These are listed in the `requirements.txt` file.

A `requirements.txt` is a python-specific method for listing library dependencies and your python package manager, pip, is equipped to ingest this file and install dependencies automatically.

The exact method for doing this can vary from system to system but is generally accomplished with:

```
pip install -r requirements.txt
```

More details can be found here: 

https://note.nkmk.me/en/python-pip-install-requirements/

# Configuration
Configuration should be a familiar process to most other tools.  An INI file provides the options you'll want.  A sample configuration file is provided for ease of use.

## Rename the sample configuration file / fill out values.
In the `./Conf` directory, you'll see a file named `configuration.sample.ini`.  

Rename this file to whatever you want, however if you specify the name `configuration.ini` in the same directory, then `selectm` will find it automatically when you run it.  

```
[ bagira @ forge.silogroup.org ] << ~/development/internal/selectm/Conf >>

[- mv configuration.sample.ini configuration.ini
```
*Note*: If you use a different filename than `configuration.ini`, such as scenarios where multiple instances of `selectm` will run at a time, then you will need to manually specify the configuration file path at runtime.  Instructions on how to do that are below.

There will be several values you will need to supply.  See the comments in the configuration file for all necessary details.


## Execute the Utility

Executing the `selectm` utility should seem relatively straight forward and familiar to unix users. 
```
[ bagira @ forge.silogroup.org ] << ~/development/internal/selectm >>

[- ./selectm -h
usage: selectm [-h] [-l | -la | -b] [-c CONFIG_FILE]

Interacts with a specific website.

optional arguments:
  -h, --help            show this help message and exit
  -l, --list-available  List available items
  -la, --list-all       List all items
  -b, --buy             Buy the configured item.
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        Override the path to the config file.

Designed and implemented by Chris Punches <chris.punches@silogroup.org>.
```