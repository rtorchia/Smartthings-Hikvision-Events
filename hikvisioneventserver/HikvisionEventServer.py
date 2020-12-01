#!/user/bin/python
#!/usr/bin/python3.8
## python3.8
## Hikvision Event Server
## Tested with Hikvison NVR DS-7608NI-EV2 / 8P
## Written by Ralph Torchia (ralphtorchia1 at gmail dot com)
## Copyrighted 2019-2020
## This code is under the terms of the GPL v3 license.

## v1.3

import sys
import configparser
import json
import requests
import os
import datetime
import logging
from logging.handlers import RotatingFileHandler

from hikvisionapi import Client

# Get config settings
class HVServerConfig():
    def __init__(self, configfile):

        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self.CAMERA = ['0', '1', '2', '3', '4', '5', '6', '7']

        self.IPADDR = self.read_config_var('hikvision', 'ipaddress', 'http://localhost', 'str')
        self.USER = self.read_config_var('hikvision', 'user', 'admin', 'str')
        self.PASS = self.read_config_var('hikvision', 'pass', 'admin', 'str')
        self.HOSTPORT = self.read_config_var('smartthings', 'hostport', 'localhost', 'str')
        self.ACCESSTOKEN = self.read_config_var('smartthings', 'accesstoken', 'accesstoken', 'str')
        self.APPKEY = self.read_config_var('smartthings', 'appkey', 'appkey', 'str')

        self.LOGFILE = self.read_config_var('logging', 'logfile', '','str')
        self.LOGMAXSIZE = self.read_config_var('logging', 'logmaxsize', 102400, 'int')
        self.LOGMAXBACKUPS = self.read_config_var('logging', 'logmaxbackups', 5, 'int')
        if self.LOGFILE == '':
            self.LOGGING = False
        else:
            self.LOGGING = True

        for i in range(8):
            self.CAMERA[i] = self.read_config_var('cameras', 'cam'+str(i), 'camera '+str(i+1), 'str')

    def read_config_var(self, section, variable, default, type = 'str', quiet = False):
            try:
                if type == 'str':
                    return self._config.get(section,variable)
                elif type == 'bool':
                    return self._config.getboolean(section,variable)
                elif type == 'int':
                    return int(self._config.get(section,variable))
            except (configparser.NoSectionError, configparser.NoOptionError):
#                self.defaulting(section, variable, default, quiet)
                return default

def hikevents_logger(hikevent):
    if config.LOGGING:
        outfile.info(hikevent)
    else:
        print(hikevent)

# Main
while True:
    cfgfile = 'hikvisionevents.cfg'
    
    #cfgfile=cfgpath + 'hikvisionevents.cfg'
    pathname = os.path.dirname(sys.argv[0])
    cfgpath = os.path.abspath(pathname)
    configfile = os.path.join(cfgpath, cfgfile)

    if os.path.exists(configfile):
        print (f'Hikvisoin Events Server loading {cfgfile} file.')
        config = HVServerConfig(configfile)
        
        if config.LOGGING:
            outfile = logging.getLogger('hikevents_logger')
            outfile.setLevel(logging.INFO)
            outfile_handler = logging.handlers.RotatingFileHandler(config.LOGFILE, mode="a", maxBytes=(config.LOGMAXSIZE), backupCount=config.LOGMAXBACKUPS)
            outfile.addHandler(outfile_handler)
            print(f"Writing logfile to {config.LOGFILE}")
        
        log_msg = 'Logging started at: ' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        hikevents_logger(log_msg)
        hikevents_logger('Connecting to Hikvision NVR...')
        try:
            nvr = Client(config.IPADDR, config.USER, config.PASS)
            hikevents_logger('Monitoring for events from NVR @ http://'+config.IPADDR)
            nvrinfo = nvr.System.deviceInfo(method='get')
            hikevents_logger('  Name: ' + nvrinfo['DeviceInfo']['deviceName'])
            hikevents_logger('  Serial: ' + nvrinfo['DeviceInfo']['serialNumber'])
            hikevents_logger('  Model: ' + nvrinfo['DeviceInfo']['model'])
            hikevents_logger('  Firmware: ' + nvrinfo['DeviceInfo']['firmwareVersion'])
            hikevents_logger('  Cameras: ')
            for i in range (8):
                hikevents_logger('    ' + str(i+1) + ') ' + config.CAMERA[i])
        except:
            hikevents_logger('ERROR: Hikvision NVR not found!')
            sys.exit()

    else:
        sys.exit('ERROR: hikvisionevents.cfg file not found!')

    while True:
        try:
            nvrevent = nvr.Event.notification.alertStream(method='get', type='stream')

            if nvrevent:
                eventchannelID = 'dynChannelID'
                if 'channelID' in nvrevent:
                    eventchannelID = 'channelID'

                cameranumber = int(nvrevent[0]['EventNotificationAlert'][eventchannelID]) - 1
                if  cameranumber not in list(range(0,8)) :
                    cameranumber = 0

                body = {
                        'eventType': nvrevent[0]['EventNotificationAlert']['eventType'],
                        'eventTime': nvrevent[0]['EventNotificationAlert']['dateTime'],
                        'cameraName': config.CAMERA[cameranumber],
                        'channelName': nvrevent[0]['EventNotificationAlert'][eventchannelID]
                        }

                headers = {'Content-Type': 'application/json'}
                    
                urls = {
                        'host': config.HOSTPORT,
                        'path': '/api/token/' + config.ACCESSTOKEN + '/smartapps/installations/' + config.APPKEY + '/event',
                        'port': '443',
                        }

                urlreq = 'https://' + urls['host'] + ':' + urls['port'] + urls['path']
                hikevents_logger(" Event detected: " + body['eventType'] + " occurred at " + body['eventTime'] + " for camera " + body['cameraName'] + " (channel=" + body['channelName'] + ")")
                # hikevents_logger(f' Event detected: {body['eventType']} occurred at {body['eventTime']} for camera {body['cameraName']} (channel={body['channelName']})')

                stconn = requests.put(urlreq, data=json.dumps(body), headers=headers)
            else:
                sys.exit('ERROR: Could not open stream to NVR!')

        except IOError:
            pass
        except KeyboardInterrupt:
            hikevents_logger('Program exececution halted by user.')
            sys.exit()
        except Exception as exception:
            hikevents_logger(f'--> {exception}')
            #pass
