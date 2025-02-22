import sys
import socket
from datetime import datetime
import json
import time

# MAX_BYTES = 1024 #Constant for max bytes to receive in a log message
# MAX_TIMEOUT = 600

HOUR_MILLIS = 3600000

configFile = open('config.json')
config = json.load(configFile)

ipAddr = ""
port = 0
logFilePath = ""
timeout = 0
maxBytes = 0
formatType = ""
maxLogs = 0

hasConfig = 1

#TODO add default values if it's not specified
if config['ip_address'] == "":
    print('Configured IP Address missing: Please configure an IP address in the config file')
    hasConfig = 0
else:
    ipAddr = config['ip_address']
if config['port'] == "":
    print('Configured port missing: Please configure a port in the config file')
    hasConfig = 0
else:
    port = config['port']
if config['log_file_path'] == "":
    print('Configured port missing: Please configure a log file path in the config file')
    hasConfig = 0
else:
    logFilePath = config['log_file_path']
if config['timeout'] == "":
    print('Configured timeout missing: Please configure a timeout value in the config file')
    hasConfig = 0
else:
    timeout = config['timeout']
if config['max_bytes'] == "":
    print('Configured max bytes missing: Please configure a max bytes value in the config file')
    hasConfig = 0
else:
    maxBytes = config['max_bytes']
if config['format_type'] == "":
    print('Configured format type missing: Please configure a format type value in the config file')
    hasConfig = 0
else:
    formatType = config['format_type']
if config['max_logs'] == "":
    maxLogs = 100
else:
    maxLogs = config['max_logs']

if hasConfig == 0:
    sys.exit(1)


def verifyHost (hostInfo):
    hostsLogCounter = hostInfo[1]
    hostsLogTime = hostInfo[2]
    # compare current time and first log time
    logTimeDifference = time.time() - hostsLogTime

    #If the last log was more than an hour ago allow the log
    if logTimeDifference > HOUR_MILLIS:
        return True
    #otherwise check the counter
    else:
        # if the counter is more than or equal to the max logs don't allow the log
        if hostsLogCounter >= maxLogs:
            return False
        else:
            return True



def logMessage (addr, message, logger):
    if formatType == "syslog":
        logger.CreateSyslogMessage(addr[0], message)
    elif formatType == "csv":
        logger.CreateCSVLogMessage(addr[0], message)
    elif formatType == "xml":
        logger.CreateXMLLogMessage(addr[0], message)

class Logger:
    def __init__(self, logfilePath):
        self.logfilePath = logfilePath
        
    def Log(self, logMessage):
        with open(self.logfilePath, "a") as file:
            file.write(f'{logMessage}')
    
    def CreateSyslogMessage(self, receivedFrom, message):
        dt = datetime.now().strftime("%m-%d-%Y %H:%M:%S")  #formatting date and time for the log
        parts = message.split('|')
        if len(parts) == 3:
            severity = parts[0]
            level = parts[1]
            logMessage = parts[2]
            print(f"LOG: {dt} [{receivedFrom}] [{severity}] [{level}] - {logMessage}")
            self.Log(f'{dt} [{receivedFrom}][{severity}] [{level}] - {logMessage}\n')

    def CreateCSVLogMessage(self, receivedFrom, message):
        dt = datetime.now().strftime("%d-%m-%Y,%H:%M:%S")  # formatting date and time for the log
        parts = message.split('|')
        if len(parts) == 3:
            severity = parts[0]
            level = parts[1]
            logMessage = parts[2]
            print(f"LOG: {dt},[{severity}],[{level}],[{receivedFrom}],- {logMessage}")
            self.Log(f"LOG: {dt},[{severity}],[{level}],[{receivedFrom}],- {logMessage}\n")

    def CreateXMLLogMessage(self, receivedFrom, message):
        dt = datetime.now().strftime("<date>%m-%d-%Y</date> <time>%H:%M:%S</time>")  # formatting date and time for the log
        parts = message.split('|')
        if len(parts) == 3:
            severity = parts[0]
            level = parts[1]
            logMessage = parts[2]
            print(f"LOG: {dt} <severity>[{severity}]</severity> <level>[{level}]</level> "
            "<received_from>[{receivedFrom}]</received_from> - <message>{logMessage}</message>")
            self.Log(f"LOG: {dt} <severity>[{severity}]</severity> <level>[{level}]</level> "
            "<received_from>[{receivedFrom}]</received_from> - <message>{logMessage}</message>\n")


logger = Logger(logFilePath)

LISTEN_IP = ipAddr
LISTEN_PORT = port

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #create a UDP socket

sock.bind((LISTEN_IP, LISTEN_PORT))  #bind it to an IP and Port

sock.settimeout(timeout)

activeLoggingHosts = []
hostAdded = False
#initialize to true or the first host won't be added
allowLog = True


while True:
    try:
        data, addr = sock.recvfrom(maxBytes)
        message = data.decode('utf-8')

        for host in activeLoggingHosts:
            # check if address is in the list of hosts
            if host[0] == addr[0]:
                #If the log is allowed write the log message
                allowLog = verifyHost(host)
                if allowLog:
                    if host[1] >= maxLogs:
                        #reset the counter and the last log time
                        host[1] = 0
                        host[2] = time.time()
                    logMessage(addr, message, logger)
                    #increment the counter by 1
                    host[1] += 1
                    hostAdded = True

        #If the host hasn't been added and they are allowed to log
        if hostAdded == False and allowLog:
            # Add the new host to the list
            activeLoggingHostsInfo = [addr[0], 1, time.time()]
            activeLoggingHosts.append(activeLoggingHostsInfo)
            #log the message
            logMessage(addr, message, logger)

        #reset flags
        hostAdded = False
        allowLog = False

    except UnicodeDecodeError:
        logger.CreateSyslogMessage(addr[0], "3|WARN|Logger couldn't decode message, skipping")
    except socket.timeout:
        logger.CreateSyslogMessage('Server', "3|WARN|Socket timed out, no data received.")
    except KeyboardInterrupt:
        sock.close()
        break
    except Exception as e:
        remote_addr = addr[0] if 'addr' in locals() else 'Unknown'
        logger.CreateSyslogMessage(addr[0], f"4|WARN|Logger experienced unknown exception: {e}")




