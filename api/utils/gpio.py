import pigpio
from pigpio import error

from typing import List


class GPIOControl:
    GENERAL_PINS = [5, 6, 16, 17, 22, 23, 24, 25, 26, 27]
    HW_PWM_PINS = [12, 13, 18, 19]

    gpio = pigpio.pi()

    @classmethod
    def allowed_pin_or_raise(cls, pin: int):
        if pin not in cls.GENERAL_PINS + cls.HW_PWM_PINS:
            raise PinNotAllowed(pin)


class GPIOGetter(GPIOControl):
    @classmethod
    def type(cls, pin: int) -> str:
        cls.allowed_pin_or_raise(pin)
        if pin in cls.GENERAL_PINS:
            return 'GENERAL'
        if pin in cls.HW_PWM_PINS:
            return 'HW_PWM'

    @classmethod
    def mode(cls, pin: int) -> str:
        cls.allowed_pin_or_raise(pin)
        mode = cls.gpio.get_mode(pin)
        if mode is pigpio.INPUT:
            return 'INPUT'
        elif mode is pigpio.OUTPUT:
            return 'OUTPUT'
        return 'ALT'

    @classmethod
    def value(cls, pin: int) -> int:
        cls.allowed_pin_or_raise(pin)
        return cls.gpio.read(pin)

    @classmethod
    def pwm(cls, pin: int) -> bool:
        cls.allowed_pin_or_raise(pin)
        try:
            cls.gpio.get_PWM_dutycycle(pin)
            return True
        except error:
            return False

    @classmethod
    def pwm_freq(cls, pin: int) -> int:
        cls.allowed_pin_or_raise(pin)
        return cls.gpio.get_PWM_frequency(pin) if cls.pwm(pin) else 0

    @classmethod
    def pwm_dutycycle(cls, pin: int) -> int:
        cls.allowed_pin_or_raise(pin)
        return cls.gpio.get_PWM_dutycycle(pin) if cls.pwm(pin) else 0

    @classmethod
    def list(cls) -> List[dict]:
        return [cls.get(pin) for pin in cls.GENERAL_PINS + cls.HW_PWM_PINS]

    @classmethod
    def get(cls, pin: int) -> dict:
        cls.allowed_pin_or_raise(pin)
        return {
            'pin': pin,
            'type': cls.type(pin),
            'mode': cls.mode(pin),
            'value': cls.value(pin),
            'pwm': cls.pwm(pin),
            'pwm_freq': cls.pwm_freq(pin),
            'pwm_dutycycle': cls.pwm_dutycycle(pin)
        }


class GPIOSetter(GPIOControl):
    @classmethod
    def mode(cls, pin: int, out: bool):
        cls.allowed_pin_or_raise(pin)
        if out:
            cls.gpio.set_mode(pin, pigpio.OUTPUT)
        else:
            cls.gpio.set_mode(pin, pigpio.INPUT)

    @classmethod
    def value(cls, pin: int, on: bool):
        cls.allowed_pin_or_raise(pin)
        cls.gpio.set_mode(pin, pigpio.OUTPUT)
        cls.gpio.write(pin, int(on))

    @classmethod
    def pwm_freq(cls, pin: int, freq: int):
        cls.allowed_pin_or_raise(pin)
        cls.gpio.set_mode(pin, pigpio.OUTPUT)
        cls.gpio.set_PWM_frequency(pin, freq)

    @classmethod
    def pwm_dutycycle(cls, pin: int, dutycycle: int):
        cls.allowed_pin_or_raise(pin)
        cls.gpio.set_mode(pin, pigpio.OUTPUT)
        cls.gpio.set_PWM_dutycycle(pin, dutycycle)


class PinNotAllowed(Exception):
    def __init__(self, pin: int):
        super().__init__('Pin {} is not allowed'.format(pin))
