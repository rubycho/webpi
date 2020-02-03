import os

from django.test import TestCase
from api.utils.gpio import GPIOControl, GPIOGetter, GPIOSetter, PinNotAllowed


class GPIOTest(TestCase):
    pin, mode, val = -1, -1, -1
    pwm, freq, duty = -1, -1, -1

    @classmethod
    def setUpClass(cls):
        if 'PIGPIO_ADDR' not in os.environ:
            raise Exception()

        cls.pin = GPIOControl.GENERAL_PINS[0]
        cls.mode = GPIOGetter.mode(cls.pin)
        cls.val = GPIOGetter.value(cls.pin)

        cls.pwm = GPIOGetter.pwm(cls.pin)
        cls.freq = GPIOGetter.pwm_freq(cls.pin)
        cls.duty = GPIOGetter.pwm_dutycycle(cls.pin)

    def test_allowed_pin_or_raise(self):
        self.assertRaises(PinNotAllowed, GPIOControl.allowed_pin_or_raise, -1)

    def test_list(self):
        result = GPIOGetter.list()
        self.assertEqual(len(result), len(GPIOControl.GENERAL_PINS + GPIOControl.HW_PWM_PINS))

    def test_type(self):
        for pin in GPIOControl.GENERAL_PINS:
            self.assertEqual(GPIOGetter.type(pin), 'GENERAL')

        for pin in GPIOControl.HW_PWM_PINS:
            self.assertEqual(GPIOGetter.type(pin), 'HW_PWM')

    def test_mode(self):
        GPIOSetter.mode(self.pin, 1)
        self.assertEqual(GPIOGetter.mode(self.pin), 1)

        GPIOSetter.mode(self.pin, 0)
        self.assertEqual(GPIOGetter.mode(self.pin), 0)

    def test_value(self):
        GPIOSetter.mode(self.pin, 1)

        GPIOSetter.value(self.pin, 1)
        self.assertEqual(GPIOGetter.value(self.pin), 1)

        GPIOSetter.value(self.pin, 0)
        self.assertEqual(GPIOGetter.value(self.pin), 0)

    def test_pwm(self):
        GPIOSetter.pwm_dutycycle(self.pin, 128)
        GPIOSetter.pwm_freq(self.pin, 400)

        self.assertEqual(GPIOGetter.pwm_dutycycle(self.pin), 128)
        self.assertEqual(GPIOGetter.pwm_freq(self.pin), 400)

    @classmethod
    def tearDownClass(cls):
        if cls.pwm:
            GPIOSetter.pwm_dutycycle(cls.pin, cls.duty)
            GPIOSetter.pwm_freq(cls.pin, cls.freq)
        else:
            GPIOSetter.mode(cls.pin, cls.mode)
            GPIOSetter.value(cls.pin, cls.val)
