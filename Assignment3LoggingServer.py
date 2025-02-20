import sys
import socket
from datetime import datetime

MAX_BYTES = 1024 #Constant for max bytes to receive in a log message
MAX_TIMEOUT = 600
# Access cmd line arguments, must be exactly 3
if len(sys.argv) != 3:
    print('Usage: logger.py 127.0.0.1 C:\\Log.log\nExiting service')
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
            print(f"LOG: {dt} [{receivedFrom}] [{severity}] [{level}] - {logMessage}")
            self.Log(f'{dt} [{receivedFrom}][{severity}] [{level}] - {logMessage}\n')
        else:
            self.Log(f'{dt} [?] [Malformed Log] - {message}\n')


logger = Logger(sys.argv[2])

LISTEN_IP = sys.argv[1]
LISTEN_PORT = 13000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #create a UDP socket

sock.bind((LISTEN_IP, LISTEN_PORT))  #bind it to an IP and Port

sock.settimeout(MAX_TIMEOUT)

while True:
    try:
        data, addr = sock.recvfrom(MAX_BYTES)
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
         remote_addr = addr[0] if 'addr' in locals() else 'Unknown'
         logger.CreateLogMessage(addr[0], f"4|WARN|Logger experienced unknown exception: {e}")


