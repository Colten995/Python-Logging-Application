# Name: Logger
# Description: This class is used to parse log messages for the information and save the information to a log file. The create log message creates the log using the
# format specified in the config file

from datetime import datetime

class Logger:

    # Name: __init__
    # Description: This is the default constructor for the log. It simply creates the logger with the log file path
    # Params: self : Reference to the object being constructed
    #       : logFilePath : The path to the file that the logs will be saved in
    def __init__(self, logfilePath, formatType):
        self.logfilePath = logfilePath
        self.formatType = formatType

    # Name: Log
    # Description: This is the method that is called to open the log file and write the log into it
    # Params: self : Reference to the object being constructed
    #       : logMessage : The log that will be written to the file
    # Returns : nothing
    def Log(self, logMessage):
        with open(self.logfilePath, "a") as file:
            file.write(f'{logMessage}')

    # Name: CreateLog
    # Description: This method parses the log message received and gets the individual parts of it. Then it creates a new log message in the specified format and logs it.
    #              If the incoming log message is malformed or not formatted correctly it is not logged
    # Params: self : Reference to the object being constructed
    #       : receivedFrom : This is the IP Address of the client that sent the message
    #       : message : This is the actual log message that is received and parsed
    # Returns: boolean : indicates if the log was actually created or not
    def CreateLog(self, receivedFrom, message):
        # Split the log message into it's different sections
        parts = message.split('|')
        if len(parts) == 3:
            severity = parts[0]
            level = parts[1]
            logMessage = parts[2]

            # Check log format type and create the log using the provided format
            if self.formatType == "syslog":
                dt = datetime.now().strftime("%m-%d-%Y %H:%M:%S")  # formatting date and time for the log
                self.Log(f'{dt} [{receivedFrom}][{severity}] [{level}] - {logMessage}\n')
                return True
            elif self.formatType == "csv":
                dt = datetime.now().strftime("%d-%m-%Y %H:%M:%S")  # formatting date and time for the log
                self.Log(f"LOG: {dt},[{severity}],[{level}],[{receivedFrom}],- {logMessage}\n")
                return True
            elif self.formatType == "xml":
                dt = datetime.now().strftime("%m-%d-%Y %H:%M:%S")  # formatting date and time for the log
                self.Log(f"LOG: {dt} <severity>[{severity}]</severity> <level>[{level}]</level> "
                "<received_from>[{receivedFrom}]</received_from> - <message>{logMessage}</message>\n")
                return True
        # If we can't split the log, don't log it and indicate the logging was unsuccessful
        else:
            return False