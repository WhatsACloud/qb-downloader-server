from downloader.config import LOG_LOCATION
from loguru import logger

def setup():
    logger.remove(0)
    logger.add(LOG_LOCATION)

def log_err(intuit_tid, msg):
    logger.error(f"intuit_tid: ({intuit_tid}) | {msg}")

"""
class Logger:
    def __init__(self):
        self.log_location = LOG_LOCATION
        self.file_log = None
    def open(self):
        if self.file_log == None:
            try:
                self.file_log = open(self.log_location, "a")
            except Exception as err:
                print(err)
    def close(self):
        if self.file_log != None:
            try:
                self.file_log.close()
            except Exception as err:
                print(err)
        self.file_log = None
    def log(self, intuit_tid, error_txt):
        if self.file_log == None:
            print("WARNING: please instantiate logger by calling Logger.open() first!")
            return
        try:
            self.file_log.write(f"{datetime.now()} intuit_tid: {intuit_tid}\n {error_txt} \n\n")
        except Exception as err:
            print("FILE WRITE EXCEPTION: ", err)
"""