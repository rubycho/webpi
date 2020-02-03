# webpi

Raspberry PI Controllable API. (Graduation Project)

## This Provides
- give me contents

## Test Environment

- Raspberry PI 2
- Raspbian Buster (2019-06)
- SDCard >= 32GB

## Dependencies

- `django` and `drf` for API server
- `pigpio` for controlling gpio
- `psutil` for retrieving process information

## Run for dev purpose

```bash
# (On PI) install and activate pigpio
./install.sh

# (On Computer) setup
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt 

# (On Computer) run
export PIGPIO_ADDR={YOUR_PI_ADDR} 
python manage.py runserver
```

## Test

- uses django.test(`unittest`)

```bash
$ export PIGPIO_ADDR={YOUR_PI_ADDR}
$ coverage run manage.py test
```
