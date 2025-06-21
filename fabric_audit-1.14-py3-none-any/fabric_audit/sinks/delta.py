import datetime
from ..collectors.batch_result import BatchResult, CollectorCollection
import traceback
import logging
from pyspark.sql import SparkSession 
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from pyspark.sql.functions import lit

class DeltaSink(logging.Handler):
    def __init__(self, credentials, runId: str, log_level: int):
        super().__init__(log_level)
        self.credentials = credentials
        self.database = None
        self.client = None
        self.runId = runId

    def set_connection(self, connection: str):
        db = connection.replace('delta://', '')
        self.database = len(db) > 0 and db != 'default' and db or None
    
    def is_valid_sink(self, connection: str):
        return connection.startswith('delta://')

    def write(self, collection: CollectorCollection):
        spark = SparkSession.builder.getOrCreate()
        schema = StructType([ 
            StructField(field.replace(' ', '_').replace('(', '').replace(')', ''), StringType(), True) 
            for field in collection.fields
            ])
        df = spark.createDataFrame(
            collection.data, 
            schema
        )
        full_df = df.withColumn('Iteration', lit(self.runId))
        tableName = collection.name
        if(self.database is not None):
            tableName = f'{self.database}.{tableName}'
        full_df.write.mode('append').format('delta').saveAsTable(tableName)


    def emit(self, message, stack_trace=None, no_print:bool=False):
        spark = SparkSession.builder.getOrCreate()
        fields = ['Iteration', 'DateTime', 'Message', 'StackTrace']
        schema = StructType([ StructField(field, TimestampType() if field == 'DateTime' else StringType(), True) for field in fields])
        df = spark.createDataFrame(
            [(self.runId, datetime.datetime.now(), message, stack_trace)], 
            schema
        )
        tableName = 'Log'
        if(self.database is not None):
            tableName = f'{self.database}.{tableName}'
        df.write.mode('append').format('delta').saveAsTable(tableName)
        formatted_time = datetime.datetime.now().strftime('%H:%M:%S')
        fullMessage = f'[{formatted_time}] {message}\n'
        if not no_print:
            print(fullMessage)
        

    def error(self, message, ex: Exception = None):
        if ex is None:
            self.emit(message)
        else:
            self.emit(message, str(traceback.format_exception(ex)).replace('\\n', '\n'))