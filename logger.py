
from pydantic import BaseModel
import sys, os, json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
__main_path__ = os.path.dirname(__file__)
file_name     = __file__.split('/')[-1]

from tamga import Tamga
from config import config

class loggerFileTest(BaseModel):
    level:str
    message:str

class loggerWriteError(BaseModel):
    type:str
    message:str


class logger:
    def __init__(self):
        os.makedirs('./log', exist_ok=True)
        self.logger = Tamga(
            logToFile=True,
            logToJSON=True,
            logJSON=os.path.join(__main_path__, config.loggerJsonFilePath),
            logFile=os.path.join(__main_path__, config.loggerTextFilePath),
            logToConsole=True
        )
        self.levels = ['info', 'warning', 'error', 'success', 'debug', 'critical']

    def write(self, body:dict, displayJestMessage=True):
        body = json.loads(body)
        level   = body.get('level', None)
        # message = body.get('message')
        if level in self.levels and level and body:
            if level == 'info':
                self.logger.info(body.get('message') if displayJestMessage else body)
            elif level == 'warning':
                self.logger.warning(body.get('message') if displayJestMessage else body)
            elif level == 'error':
                self.logger.error(body.get('message') if displayJestMessage else body)
            elif level == 'success':
                self.logger.success(body.get('message') if displayJestMessage else body)
            elif level == 'debug':
                self.logger.debug(body.get('message') if displayJestMessage else body)
            elif level == 'critical':
                self.logger.critical(body.get('message') if displayJestMessage else body)
            else:
                self.logger.warning(loggerWriteError(type='logicError', message='There is a problem with if/else cercle'))
        else:
            self.logger.custom(level=level, message=body.get('message') if displayJestMessage else body, color='gray')


if __name__ == '__main__':
    message = loggerFileTest(level='debug', message="This is test for `/plugin/logger.py` file").model_dump_json()
    logger().write(body=message)

