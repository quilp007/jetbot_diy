import time
from pca9685 import PCA9685

# Mock I2C class for testing without hardware
class MockI2C:
    def writeto_mem(self, address, register, buffer):
        print(f"I2C Write to Address: {hex(address)}, Register: {hex(register)}, Data: {list(buffer)}")

    def readfrom_mem(self, address, register, size):
        print(f"I2C Read from Address: {hex(address)}, Register: {hex(register)}, Size: {size}")
        if register == 0x00: # MODE1
            return bytearray([0x10]) # Return SLEEP bit set
        return bytearray([0x00] * size)

def main():
    # Initialize I2C bus
    i2c = MockI2C()

    # Initialize PCA9685
    pca = PCA9685(i2c)

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
    print(f"Set PWM for channel {channel} to on: {on_tick}, off: {off_tick}")

    time.sleep(1)

    # Set all PWM channels to off
    pca.set_all_pwm(0, 0)
    print("All PWM channels turned off.")


if __name__ == "__main__":
    main()
