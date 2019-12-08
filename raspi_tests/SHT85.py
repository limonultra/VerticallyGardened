import smbus
import time


bus  = smbus.SMBus(1)
addr = 0x44

# Single Shot Data Acquisition Mode
SHT_SS_MSB = 0x24
SHT_SS_LSB = {'HIGH'   : 0x00,
              'MEDIUM' : 0x0B,
              'LOW'    : 0x16}


# Periodic Data Acquisition Mode
SHT_P_MSB  = {0.5 : 0x20,
              1   : 0x21,
              2   : 0x22,
              4   : 0x23,
              10  : 0x27}
SHT_P_LSB  = {0.5 : (0x32, 0x24, 0x2F),
              1   : (0x30, 0x26, 0x2D),
              2   : (0x36, 0x20, 0x2B),
              4   : (0x34, 0x22, 0x29),
              10  : (0x37, 0x21, 0x2A)}


# ART Command (Accelerated Response Time)
SHT_ART_MSB = 0x2B
SHT_ART_LSB = 0x32


# Break Command / Stop Periodic Data Acquisition Mode
SHT_BRK_MSB = 0x30
SHT_BRK_LSB = 0x93


# Reset
SHT_RST_MSB = 0x30
SHT_RST_LSB = 0xA2


# Heater
SHT_HTR_MSB = 0x30
SHT_HTR_ON  = 0x6D
SHT_HTR_OFF = 0x66


# Status Register
SHT_STA_MSB = 0xF3
SHT_STA_LSB = 0x2D


# Clear Status Register
SHT_CLR_MSB = 0x30
SHT_CLR_LSB = 0x41

SHT_SN_MSB  = 0x36
SHT_SN_LSB  = 0x82


# Read:
SHT_RD      = 0x00

def readData():
    # Expect 6 bytes: 2 Temp + 1 ACK + 2 Hum + 1 ACK = 6 bytes
    data = bus.read_i2c_block_data(addr, SHT_RD, 6)
    
    t_data = data[0] << 8 | data[1]
    h_data = data[3] << 8 | data[4]

    temp = -45. + 175. * t_data / (2**16-1.)
    relh = 100 * h_data / (2**16-1.)

    return round(temp, 4), round(relh, 4)


def singleShotRead(rep='HIGH'):
    bus.write_i2c_block_data(addr, SHT_SS_MSB, [SHT_SS_LSB[rep]])
    time.sleep(.5)

    return readData()


def setPeriodic(mps=1, rep='HIGH'):
    repDict = {'HIGH'   : 0,
               'MEDIUM' : 1,
               'LOW'    : 2}
    rep     = repDict[rep]
    
    bus.write_i2c_block_data(addr, SHT_P_MSB[mps], [SHT_P_LSB[mps][rep]])
    time.sleep(0.5)
    

def stop():
    bus.write_i2c_block_data(addr, SHT_BRK_MSB, [SHT_BRK_LSB])
    print "Break"


def reset():
    bus.write_i2c_block_data(addr, SHT_RST_MSB, [SHT_RST_LSB])
    print "Reset"


def heater(heat='on'):
    if heat == 'on':
        heat = SHT_HTR_ON
    elif heat == 'off':
        heat = SHT_HTR_OFF

    bus.write_i2c_block_data(addr, SHT_HTR_MSB, [heat])

    print "Heater is: " + heat


def sn():
    bus.write_i2c_block_data(addr, SHT_SN_MSB, [SHT_SN_LSB])
    time.sleep(0.5)

    sn_read = bus.read_i2c_block_data(addr, SHT_RD, 6)
    
    sn = sn_read[0] << 16 | sn_read[4]

    return sn






def main():
    print "Serial number:", sn()
    print "Leemos:"
    
    # Set periodic read with mps=1 adnd high repeatability
    setPeriodic()

    while True:
        temp, hum = readData()
        print "Temperature:", temp
        print "Humidity:   ", hum

        time.sleep(1.5)


if __name__ == '__main__':
    main()
