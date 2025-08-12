# PCA9685 Python Library

This is a Python library for the NXP PCA9685 16-channel, 12-bit PWM I2C-bus LED/servo driver.

## Features

- Set PWM frequency for all channels.
- Set PWM duty cycle for individual channels.

## Usage

Here is a simple example of how to use the library:

```python
import time
from pca9685 import PCA9685
from smbus2 import SMBus

def main():
    # Initialize I2C bus
    bus = SMBus(1) # Or 0, depending on your Raspberry Pi version

    # Initialize PCA9685
    pca = PCA9685(bus)

    # Set PWM frequency to 60hz
    pca.set_pwm_freq(60)

    # Set a PWM channel to a specific value
    # For example, channel 0 with a 50% duty cycle
    # The PCA9685 has 4096 steps (12-bit)
    # 50% of 4096 is 2048
    channel = 0
    on_tick = 0
    off_tick = 2048
    pca.set_pwm(channel, on_tick, off_tick)

    time.sleep(1)

    # Set all PWM channels to off
    pca.set_all_pwm(0, 0)


if __name__ == "__main__":
    main()
```

## I2C Dependency

This library relies on an I2C interface object that provides `writeto_mem(address, register, buffer)` and `readfrom_mem(address, register, size)` methods. A common library that provides this interface is `smbus2` for Raspberry Pi.
