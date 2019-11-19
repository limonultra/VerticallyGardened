import configparser

def readConfig():
    conf = {}
    config = configparser.ConfigParser()
    config.read('../config.cfg')

    conf["token"]        = config['THINGSBOARD']['token']
    conf["refreshToken"] = config['THINGSBOARD']['refreshToken']

    return conf
