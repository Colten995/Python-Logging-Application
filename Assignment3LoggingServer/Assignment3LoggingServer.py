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

# Default config values
defaultIPAddr = "127.0.0.1"
defaultPort = 13000
defaultLogFilePath = "C:\\Logs\\log.log"
defaultTimeout = 600
defaultMaxBytes = 1024
defaultFormatType = "syslog"
defaultMaxLogs = 100

hasConfig = 1

# Get IP Address from config file and validate
if config['ip_address'] == "" or config['ip_address'].isnumeric():
    ipAddr = defaultIPAddr
else:
    ipAddr = config['ip_address']

# Get port number from config file and validate
if 0 > config['port'] > 65535:
    port = defaultPort
else:
    port = config['port']

# Get log file path from config file and validate
if config['log_file_path'] == "" or config['log_file_path'].isnumeric():
    logFilePath = defaultLogFilePath
else:
    logFilePath = config['log_file_path']

# Get timeout from config file and validate
if config['timeout'] < 0:
    timeout = defaultTimeout
else:
    timeout = config['timeout']

# Get max bytes from config file and validate
if config['max_bytes'] < 0:
    maxBytes = defaultMaxBytes
else:
    maxBytes = config['max_bytes']

# Get format type from config file and validate
if config['format_type'] == "" or config['format_type'].isnumeric() or (config['format_type'] != 'syslog' and config['format_type'] != 'xml' and config['format_type'] != 'csv'):
    formatType = defaultFormatType
else:
    formatType = config['format_type']

# Get maximum number of logs from the config file and validate
if config['max_logs'] < 0:
    maxLogs = defaultMaxLogs
else:
    maxLogs = config['max_logs']


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

class Logger:
    def __init__(self, logfilePath):
        self.logfilePath = logfilePath
        
    def Log(self, logMessage):
        with open(self.logfilePath, "a") as file:
            file.write(f'{logMessage}')

    def CreateLog(self, receivedFrom, message):
        parts = message.split('|')
        if len(parts) == 3:
            severity = parts[0]
            level = parts[1]
            logMessage = parts[2]

            if formatType == "syslog":
                dt = datetime.now().strftime("%m-%d-%Y %H:%M:%S")  # formatting date and time for the log
                print(f"LOG: {dt} [{receivedFrom}] [{severity}] [{level}] - {logMessage}")
                self.Log(f'{dt} [{receivedFrom}][{severity}] [{level}] - {logMessage}\n')
                return True
            elif formatType == "csv":
                dt = datetime.now().strftime("%d-%m-%Y %H:%M:%S")  # formatting date and time for the log
                print(f"LOG: {dt},[{severity}],[{level}],[{receivedFrom}],- {logMessage}")
                self.Log(f"LOG: {dt},[{severity}],[{level}],[{receivedFrom}],- {logMessage}\n")
                return True
            elif formatType == "xml":
                dt = datetime.now().strftime("%m-%d-%Y %H:%M:%S")  # formatting date and time for the log
                print(f"LOG: {dt} <severity>[{severity}]</severity> <level>[{level}]</level> "
                "<received_from>[{receivedFrom}]</received_from> - <message>{logMessage}</message>")
                self.Log(f"LOG: {dt} <severity>[{severity}]</severity> <level>[{level}]</level> "
                "<received_from>[{receivedFrom}]</received_from> - <message>{logMessage}</message>\n")
                return True
        else:
            return False


logger = Logger(logFilePath)

LISTEN_IP = ipAddr
LISTEN_PORT = port

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #create a UDP socket

sock.bind((LISTEN_IP, LISTEN_PORT))  #bind it to an IP and Port

sock.settimeout(timeout)

activeLoggingHosts = []
currentHostInfo = []
hostExists = False
#initialize to true or the first host won't be added
allowLog = True


while True:
    try:
        data, addr = sock.recvfrom(maxBytes)
        message = data.decode('utf-8')

        # See if the host is in the list of hosts already
        for host in activeLoggingHosts:
            if host[0] == addr[0]:
                hostExists = True
                currentHostInfo = host

        # If the host hasn't been added, add them to the list
        if hostExists == False:
            # Add the new host to the list
            activeLoggingHostsInfo = [addr[0], 1, time.time()]
            activeLoggingHosts.append(activeLoggingHostsInfo)
            currentHostInfo = activeLoggingHostsInfo

        # Make sure currentHostInfo is not empty before verifying host
        if currentHostInfo != []:
            # Verify the host is allowed to log
            if verifyHost(currentHostInfo):
                # Reset their number of logs if they are over the maximum amount
                if currentHostInfo[1] >= maxLogs:
                    # reset the counter and the last log time
                    currentHostInfo[1] = 0
                    currentHostInfo[2] = time.time()
                # If the log is successful increment the counter
                if logger.CreateLog(addr[0], message):
                    # increment the counter by 1
                    currentHostInfo[1] += 1

        #reset flags
        hostExists = False

    except UnicodeDecodeError:
        logger.CreateLog(addr[0], "3|WARN|Logger couldn't decode message, skipping")
    except socket.timeout:
        logger.CreateLog('Server', "3|WARN|Socket timed out, no data received.")
    except KeyboardInterrupt:
        sock.close()
        break
    except Exception as e:
        remote_addr = addr[0] if 'addr' in locals() else 'Unknown'
        logger.CreateLog(addr[0], f"4|WARN|Logger experienced unknown exception: {e}")




