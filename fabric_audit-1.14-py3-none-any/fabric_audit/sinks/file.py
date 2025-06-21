import os
import datetime
import csv
from ..collectors.batch_result import BatchResult, CollectorCollection
import traceback
import logging
from pathlib import Path

class FileSink(logging.Handler):
    def __init__(self, credentials, runId, log_level: int):
        super().__init__(log_level)
        self.credentials = credentials
        self.out_path = ''
        self.runId = runId

    def set_connection(self, connection: str):
        self.out_path = connection.replace('file://', '')

    def is_valid_sink(self, connection: str):
        return connection.startswith("file://")

    def write(self, collection: CollectorCollection):
        path = self.__ensure_out_path()
        filePath = None
        if collection.partition is None:
            filePath = f'{path}/{collection.name}.csv'
        else:
            filePath = f'{path}/{collection.name}.{collection.partition}.csv'
        addHeaders = not os.path.exists(filePath)
        with open(filePath, 'a', newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file,fieldnames=collection.fields,extrasaction='ignore', quoting=csv.QUOTE_ALL, lineterminator='\n')
            if addHeaders:
                writer.writeheader()
            writer.writerows(collection.data)

    def emit(self, message: str, no_print: bool = False):
        path = self.__ensure_out_path()
        formatted_time = datetime.datetime.now().strftime('%H:%M:%S')
        if hasattr(message, 'msg'):
            message = self.format(message)
        fullMessage = f'[{formatted_time}] {message}\n'
        if not no_print:
            print(message)

        logPath =  f'{path}/audit.log'
        with open(logPath, 'a+', encoding="utf-8") as file:
            file.write(fullMessage)

    def error(self, message, ex: Exception = None):
        self.emit(message)
        if ex is not None:
            self.emit(str(traceback.format_exception(ex)).replace('\\n', '\n'))

    def __ensure_out_path(self):
        path = f'{self.out_path}/{self.runId}'
        Path(path).mkdir(parents=True, exist_ok=True)
        return path