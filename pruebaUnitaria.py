import time
import board
import busio
import VEML7700_Lib

# This example sets the ambient light integration time to 400ms
# and prints the ambient light sensor data in lux

i2c = busio.I2C(board.SCL, board.SDA)
veml7700 = VEML7700_Lib.VEML7700(i2c)

veml7700.light_integration_time = veml7700.ALS_400MS

while True:
    print("Lux: ", veml7700.lux)
    time.sleep(0.1)
