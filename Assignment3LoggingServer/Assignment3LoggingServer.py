import sys
import socket
from datetime import datetime
import json

# MAX_BYTES = 1024 #Constant for max bytes to receive in a log message
# MAX_TIMEOUT = 600

configFile = open('config.json')
config = json.load(configFile)

hasConfig = 1
logfilePath = config['log_file_path']
port = config['port']
ipAddr = config['ip_address']
timeout = config['timeout']
maxBytes = config['max_bytes']

if ipAddr == "":
    print('Configured IP Address missing: Please configure an IP address in the config file')
    hasConfig = 0
if port == "":
    print('Configured port missing: Please configure a port in the config file')
    hasConfig = 0
if logfilePath == "":
    print('Configured port missing: Please configure a log file path in the config file')
    hasConfig = 0

if hasConfig == 0:
    sys.exit(1)

class Logger:
    def __init__(self, logfilePath):
        self.logfilePath = logfilePath
        
    def Log(self, logMessage):
        with open(self.logfilePath, "a") as file:
            file.write(f'{logMessage}')
    
    def CreateLogMessage(self, receivedFrom, message):
        dt = datetime.now().strftime("%m-%d-%Y %H:%M:%S")  #formatting date and time for the log
        parts = message.split('|')
        if len(parts) == 3:
            severity = parts[0]
            level = parts[1]
            logMessage = parts[2]
            self.Log(f'{dt} [{severity}] [{level}] - {logMessage}\n')
        else:
            self.Log(f'{dt} [?] [Malformed Log] - {message}\n')


logger = Logger(logfilePath)

LISTEN_IP = ipAddr
LISTEN_PORT = port

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #create a UDP socket

sock.bind((LISTEN_IP, LISTEN_PORT))  #bind it to an IP and Port

sock.settimeout(timeout)

while True:
    try:
        data, addr = sock.recvfrom(maxBytes)
        message = data.decode('utf-8')
        logger.CreateLogMessage(addr[0],message)
    except UnicodeDecodeError:
        logger.CreateLogMessage(addr[0],"3|WARN|Logger couldn't decode message, skipping")
    except socket.timeout:
        logger.CreateLogMessage('Server', "3|WARN|Socket timed out, no data received.")
    except KeyboardInterrupt:
        sock.close()  
        break
    except Exception as e:
         logger.CreateLogMessage(addr[0], f"4|WARN|Logger experienced unknown exception: {e}")


