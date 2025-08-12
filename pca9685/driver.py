import time

# Registers
MODE1 = 0x00
MODE2 = 0x01
SUBADR1 = 0x02
SUBADR2 = 0x03
SUBADR3 = 0x04
ALLCALLADR = 0x05
LED0_ON_L = 0x06
LED0_ON_H = 0x07
LED0_OFF_L = 0x08
LED0_OFF_H = 0x09
ALL_LED_ON_L = 0xFA
ALL_LED_ON_H = 0xFB
ALL_LED_OFF_L = 0xFC
ALL_LED_OFF_H = 0xFD
PRESCALE = 0xFE

# Bits
RESTART = 0x80
SLEEP = 0x10
ALLCALL = 0x01
INVRT = 0x10
OUTDRV = 0x04


class PCA9685:
    def __init__(self, i2c, address=0x40):
        self.i2c = i2c
        self.address = address
        self.reset()

    def reset(self):
        self.i2c.writeto_mem(self.address, MODE1, bytearray([0x00]))

    def set_pwm_freq(self, freq_hz):
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq_hz)
        prescaleval -= 1.0
        prescale = int(prescaleval + 0.5)

        oldmode = self.i2c.readfrom_mem(self.address, MODE1, 1)[0]
        newmode = (oldmode & 0x7F) | SLEEP
        self.i2c.writeto_mem(self.address, MODE1, bytearray([newmode]))
        self.i2c.writeto_mem(self.address, PRESCALE, bytearray([prescale]))
        self.i2c.writeto_mem(self.address, MODE1, bytearray([oldmode]))
        time.sleep(0.005)
        self.i2c.writeto_mem(self.address, MODE1, bytearray([oldmode | RESTART]))

    def set_pwm(self, channel, on, off):
        self.i2c.writeto_mem(self.address, LED0_ON_L + 4 * channel, bytearray([on & 0xFF]))
        self.i2c.writeto_mem(self.address, LED0_ON_H + 4 * channel, bytearray([on >> 8]))
        self.i2c.writeto_mem(self.address, LED0_OFF_L + 4 * channel, bytearray([off & 0xFF]))
        self.i2c.writeto_mem(self.address, LED0_OFF_H + 4 * channel, bytearray([off >> 8]))

    def set_all_pwm(self, on, off):
        self.i2c.writeto_mem(self.address, ALL_LED_ON_L, bytearray([on & 0xFF]))
        self.i2c.writeto_mem(self.address, ALL_LED_ON_H, bytearray([on >> 8]))
        self.i2c.writeto_mem(self.address, ALL_LED_OFF_L, bytearray([off & 0xFF]))
        self.i2c.writeto_mem(self.address, ALL_LED_OFF_H, bytearray([off >> 8]))
