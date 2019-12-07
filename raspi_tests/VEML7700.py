import smbus
import time


bus  = smbus.SMBus(0) # i2c channel 0

addr = 0x10

# Write Command Codes
ALS_CONF_0 = 0x00
ALS_WH     = 0x01
ALS_WL     = 0x02

# Power Saving Command Code
POWER_SAVE = 0x03


# Read Command Codes
ALS        = 0x04
WHITE      = 0x05
ALS_INT    = 0x06


# We're gonna write to all 3 write commands
# and the power saving command tu fully configure
# the sensor


# Use ALS_CONF_0 command code to configure
# the VEML7700 sensor
# ALS_CONF_0 is a 16-bit configuration register
# that follows the format:
# REGISTER_NAME  BITS
# Reserved       15:13
# ALS_GAIN       12:11  [00 01 10 11]
# Reserved       10
# ALS_IT         9:6    [1100 1000 0000 0001 0010 0011]
# ALS_PERS       5:4    00 01 10 11
# Reserved       3:2
# ALS_INT_EN     1      0 1
# ALS_SD         0      0 1
ALS_CONF_VALUES   = [0x00, 0x10] # 0001 0000 | 0000 0000
ALS_WH_VALUES     = [0x00, 0x00]
ALS_WL_VALUES     = [0x00, 0x00]
POWER_SAVE_VALUES = [0x00, 0x00]



# Write the values to the sensor
bus.write_i2c_block_data(addr, ALS_CONF_0, ALS_CONF_VALUES)
bus.write_i2c_block_data(addr, ALS_WH    , ALS_WH_VALUES)
bus.write_i2c_block_data(addr, ALS_WL    , ALS_WL_VALUES)
bus.write_i2c_block_data(addr, POWER_SAVE, POWER_SAVE_VALUES)


while True:
    time.sleep(.150) # 150ms, greater than the IT

    wordRead   = bus.read_word_data(addr, ALS)

    # GAIN 1/8 and IT 100 -> Resolution = 0.4608
    # GAIN 1/8 and IT 25  -> Resolution = 1.8432
    resolution = 0.4608
    
    # Calculate Lux Level [wordRead * resolution]
    luxLevel   = round(wordRead * resolution, 1)

    print("Lux level: " + str(luxLevel) + "lx")
    
