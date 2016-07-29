Mycroft [![Build Status](https://travis-ci.org/clusterfudge/mycroft-core.svg?branch=master)](https://travis-ci.org/clusterfudge/mycroft-core)
==========

NOTE: This is a fork of [MycroftAI](https://github.com/MycroftAI)/[mycroft-core](https://github.com/MycroftAI/mycroft-core).
It has diverged in ways that the core will not be compatible going forward, but for the time being skill using the skils-sdk and skills-container should still function as expected.

# Getting Started in Ubuntu - Development Environment
- run `build_host_setup.sh` (installs debian packages with apt-get, please read it) 
- run `dev_setup.sh` (feel free to read it, as well)
- Restart session (reboot computer, or logging out and back in might work).

# Getting Started in other environments

The following packages are required for setting up the development environment,
 and are what is installed by `build_host_setup.sh`

 - `git`
 - `python 2`
 - `python-setuptools`
 - `python-virtualenv`
 - `pygobject`
 - `virtualenvwrapper`
 - `libtool`
 - `libffi`
 - `openssl`
 - `autoconf`
 - `bison`
 - `swig`
 - `glib2.0`
 - `s3cmd`
 - `portaudio19`
 - `mpg123`

## Provisioning API Keys
You may insert your own API keys into the configuration files listed below in <b>configuration</b>.

The place to insert the API key looks like the following:

`[WeatherSkill]`

`api_key = ""`

Put the relevant key in between the quotes and Mycroft Core should begin to use the key immediately.

- [STT API, Google STT](http://www.chromium.org/developers/how-tos/api-keys)
- [Weather Skill API, OpenWeatherMap](http://openweathermap.org/api)
- [Wolfram-Alpha Skill](http://products.wolframalpha.com/api/)

These are the keys currently in use in Mycroft Core.

## Configuration
Mycroft configuration consists of 3 possible config files.
- `mycroft-core/mycroft/configuration/mycroft.ini`
- `/etc/mycroft/mycroft.ini`
- `$HOME/.mycroft/mycroft.ini`

When the configuration loader starts, it looks in those locations in that order, and loads ALL configuration. Keys that exist in multiple config files will be overridden by the last file to contain that config value. This results in a minimal amount of config being written for a specific device/user, without modifying the distribution files.

# Running Mycroft Quick Start
To start the essential tasks run `./mycroft.sh start`. Which will start the service, skills, voice and cli (using --quiet mode) in a detched screen and log the output of the screens to the their respective log files (e.g. ./log/mycroft-service.log).
Optionally you can run `./mycroft.sh start -v` Which will start the service, skills and voice. Or `./mycroft.sh start -c` Which will start the service, skills and cli.

To stop Mycroft run `./mycroft.sh stop`. This will quit all of the detached screens.
To restart Mycroft run './mycroft.sh restart`.

Quick screen tips
- run `screen -list` to see all running screens
- run `screen -r [screen-name]` (e.g. `screen -r mycroft-service`) to reatach a screen
- to detach a running screen press `ctrl + a, ctrl + d`
See the screen man page for more details 

# Running Mycroft
## With `start.sh`
Mycroft provides `start.sh` to run a large number of common tasks. This script uses the virtualenv created by `dev_setup.sh`. The usage statement lists all run targets, but to run a Mycroft stack out of a git checkout, the following processes should be started:

- run `./start.sh service`
- run `./start.sh skills`
- run `./start.sh voice`

*Note: The above scripts are blocking, so each will need to be run in a separate terminal session.*

## Without `start.sh`

Activate your virtualenv.

With virtualenv-wrapper:
```
workon mycroft
```

Without virtualenv-wrapper:
```
source ~/.virtualenvs/mycroft/bin/activate
```


- run `PYTHONPATH=. python client/speech/main.py` # the main speech detection loop, which prints events to stdout and broadcasts them to a message bus
- run `PYTHONPATH=. python client/messagebus/service/main.py` # the main message bus, implemented via web sockets
- run `PYTHONPATH=. python client/skills/main.py` # main skills executable, loads all skills under skills dir

*Note: The above scripts are blocking, so each will need to be run in a separate terminal session. Each terminal session will require that the virtualenv be activated. There are very few reasons to use this method.*

# FAQ/Common Errors

#### When running mycroft, I get the error `mycroft.messagebus.client.ws - ERROR - Exception("Uncaught 'error' event.",)`

This means that you are not running the `./start.sh service` process. In order to fully run Mycroft, you must run `./start.sh service`, `./start.sh skills`, and `./start.sh voice`/`./start.sh cli` all at the same time. This can be done using different terminal windows, or by using the included `./mycroft.sh start`, which runs all four process using `screen`.
