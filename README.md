# webpi

Raspberry PI Controllable API. (Graduation Project)

## Check out!
- [SPA Client (webpi-app)](https://github.com/rubycho/webpi-app)
- [Endpoints (swagger)](https://app.swaggerhub.com/apis-docs/rubycho/webpi/1.0.0/)
- [Authorization (wiki)](https://github.com/rubycho/webpi/wiki/Authorization)
- [Error Responses (wiki)](https://github.com/rubycho/webpi/wiki/Error-Responses)
- [GPIO Limitations (wiki)](https://github.com/rubycho/webpi/wiki/GPIO-Limitations)

## This API Provides

- File Management
    - file(s) information on directory (like `ls -al`)
    - download and upload file
    - create directory
    - delete file or directory
- GPIO Management
    - gpio pin(s) status (**only general + hw_pwm pins**)
    - set mode of pin
    - set output value of pin
    - set pwm dutycycle and frequency of pin
- PI Infomation
    - PI spec
    - PI status (i.e. time, memory used, # of procs)
    - process information (Top 10 CPU/MEM using processes)
- Simple Terminal
    - create subprocess (`bash`)
    - make input to subprocess
    - get output from subprocess
    - kill subprocess

## Test Environment

- Raspberry PI 2
- Raspbian Buster (2019-06)
- SDCard >= 32GB

## Dependencies

- `django` and `drf` for API server
- `pigpio` for controlling gpio
- `psutil` for retrieving process information

## Install on PI

Checkout as master branch and run the following:
```bash
/home/pi/webpi$ .script/install.sh
```
Installation may take minutes to complete.

## Run for dev purpose

```bash
# setup
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt 

# run
export PIGPIO_ADDR={YOUR_PI_ADDR} 
python manage.py runserver
```

## Test

- uses django.test(`unittest`)

```bash
$ export PIGPIO_ADDR={YOUR_PI_ADDR}
$ coverage run manage.py test
```
