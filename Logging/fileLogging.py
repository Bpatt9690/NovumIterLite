import time
from datetime import date, datetime
import arrow
import os

class logger:
    def __init__(self):
        self.tz_NY = arrow.now().to("America/New_York").tzinfo
        self.host_path = '/home/pi/NovumIterLite/'

    def logData(self,data,level):

        self.setupFiles()
        
        if level == 'INFO':
            self.logInfo(data)

        elif level == 'ERROR':
            self.logError(data)

        else:
            print(level)

    def logError(self, data):
        timestamp = self.timeStamp()
        print(f"{timestamp} ERROR: {data}")
        with open(f"Logging/Error/{datetime.now().date()}.txt", "a") as f:
            f.write(f"{data}\n")

    def logInfo(self, data):
        timestamp = self.timeStamp()
        path = self.host_path+'Logging/Info/'+str(datetime.now().date())+'.txt'
        with open(path, "a") as f:
            f.write(f"{data}\n")

    def timeStamp(self): 
        datetime_NY = datetime.now(self.tz_NY)
        return str(datetime_NY.strftime("%H:%M:%S"))

    def setupFiles(self):
        errorPath = self.host_path + 'Logging/Error/'+str(datetime.now().date())+'.txt'
        infoPath = self.host_path + 'Logging/Info/'+str(datetime.now().date())+'.txt'

        if not os.path.exists(errorPath):
            # Create the file if it doesn't exist
            with open(errorPath, 'w') as file:
                file.write('Data:')
            print(f"File '{errorPath}' created")
        else:
            print(f"File '{errorPath}' already exists")

        if not os.path.exists(infoPath):
            # Create the file if it doesn't exist
            with open(infoPath, 'w') as file:
                file.write('Data:')
            print(f"File '{infoPath}' created")
        else:
            print(f"File '{infoPath}' already exists")