from micropython import const
import adafruit_bus_device.i2c_device as i2cdevice
from adafruit_register.i2c_struct import UnaryStruct, ROUnaryStruct
from adafruit_register.i2c_bits import RWBits
from adafruit_register.i2c_bit import RWBit, ROBit

class VEML7700:

# COMMAND CODE #0: CONFIGURATION REGISTER 
    
    # Ambient light sensor gain settings
    ALS_GAINx1 = const(0x0)
    ALS_GAINx2 = const(0x1)
    ALS_GAINx1_8 = const(0x2)
    ALS_GAINx1_4 = const(0x3)
    
   # Gain value integers
    gain_values = {
        ALS_GAINx1: 1,
        ALS_GAINx2: 2,
        ALS_GAINx1_4: 0.25,
        ALS_GAINx1_8: 0.125
    }

    # Ambient light integration time settings
    ALS_IT_25MS = const(0xC)
    ALS_IT_50MS = const(0x8)
    ALS_IT_100MS = const(0x0)
    ALS_IT_200MS = const(0x1)
    ALS_IT_400MS = const(0x2)
    ALS_IT_800MS = const(0x3)

    # Integration time value integers
    integration_time_values = {
        ALS_IT_25MS: 25,
        ALS_IT_50MS: 50,
        ALS_IT_100MS: 100,
        ALS_IT_200MS: 200,
        ALS_IT_400MS: 400,
        ALS_IT_800MS: 800
    }

    # ALS_SD is ALS shut down setting, when ALS_SD=1, ambient light sensor shut down
    ALS_SD = RWBit(0x00, 0, register_width=2)
    
    # ALS_INT_EN is ALS interrupt enable setting, 
    #if ALS_INT_EN==0 -> disable interrupt, if ALS_INT_EN==1 -> enable interrupt
    ALS_INT_EN = RWBit(0x00, 1, register_width=2)

    #Ambient light gain setting. Gain settings are 2, 1, 1/4 and 1/8 
    #Settings options are: ALS_GAIN_2, ALS_GAIN_1, ALS_GAIN_1_4, ALS_GAIN_1_8
    light_gain = RWBits(2, 0x00, 11, register_width=2)
    

    light_integration_time = RWBits(4, 0x00, 6, register_width=2)


# COMAND CODE #1: HIGH THRESHOLD WINDOWS SETTING

    light_high_threshold = UnaryStruct(0x01, "<H")
    
# COMAND CODE #2: LOW THRESHOLD WINDOWS SETTING

    light_low_threshold = UnaryStruct(0x02, "<H")
    
# COMAND CODE #3: POWER SAVING MODE (PSM)

# COMAND CODE #4: ALS HIGH RESOLUTION OUTPUT DATA   

    light = ROUnaryStruct(0x04, "<H")
    
# COMAND CODE #5: WHITE CHANNEL OUTPUT DATA  

    white = ROUnaryStruct(0x05, "<H")

# COMAND CODE #6: INTERRUPT STATUS 

    light_interrupt_high = ROBit(0x06, 14, register_width=2)
    light_interrupt_low = ROBit(0x06, 15, register_width=2)

# METHODS

    # Initializes the sensor
    def __init__(self, i2c_bus, address=0x10):
        self.i2c_device = i2cdevice.I2CDevice(i2c_bus, address)
        self.light_shutdown = False  # Enable the ambient light sensor

    # Integration time value in integer form that will be used for calculating resolution
    def integration_time_value(self):
        integration_time = self.light_integration_time
        return self.integration_time_values[integration_time]

    # Gain value in integer form that will be used for calculating resolution
    def gain_value(self):
        gain = self.light_gain
        return self.gain_values[gain]

    # Calculates the resolution necessary to calculate lux
    # Based on integration time and gain settings
    def resolution(self):
        resolution_at_max = 0.0036
        gain_max = 2
        integration_time_max = 800

        if self.gain_value() == gain_max and self.integration_time_value() == integration_time_max:
            return resolution_at_max
        return resolution_at_max * (integration_time_max / self.integration_time_value()) * \
               (gain_max / self.gain_value())

    # Light value in lux
    def lux(self):
        return self.resolution() * self.light


    