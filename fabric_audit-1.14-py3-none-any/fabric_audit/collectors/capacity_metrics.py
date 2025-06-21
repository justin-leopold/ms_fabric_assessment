from .capacity_query_base import CapacityQueryBase
from .batch_result import CollectorCollection

class CapacityMetricsCollector(CapacityQueryBase):
    def __init__(self):
        super().__init__()
        self.name = "Capacity Metrics"
        self.batching_query = '''EVALUATE SELECTCOLUMNS(SUMMARIZECOLUMNS(
                        MetricsByItemandOperationandHour[Date],
                        "SetSize", COUNTROWS(MetricsByItemandOperationandHour)
                    ),
         	"SetKey", MetricsByItemandOperationandHour[Date],
         	"SetSize", [SetSize]
        )'''
        self.query_template = '''EVALUATE FILTER(SUMMARIZECOLUMNS(
                        MetricsByItemandOperationandHour[ItemId],
                        MetricsByItemandOperationandHour[DateTime],
                        MetricsByItemandOperationandHour[OperationName],
                        MetricsByItemandOperationandHour[count_operations],
                        MetricsByItemandOperationandHour[count_users],
                        MetricsByItemandOperationandHour[sum_CU],
                        MetricsByItemandOperationandHour[sum_duration],
                        MetricsByItemandOperationandHour[Throttling (min)],
                        MetricsByItemandOperationandHour[count_rejected_operations],
                        TREATAS({{{keys_text}}}, MetricsByItemandOperationandHour[Date])
                    ), MetricsByItemandOperationandHour[count_operations] > 0)'''

    def map_data(self, metrics) -> CollectorCollection:
        result = CollectorCollection("CapacityMetrics")

        for entry in metrics:
            result.append({
                'OperationsCount': entry.get('MetricsByItemandOperationandHour[count_operations]'),
                'ItemId': entry.get('MetricsByItemandOperationandHour[ItemId]'),
                'DateTime': entry.get('MetricsByItemandOperationandHour[DateTime]'),
                'OperationName': entry.get('MetricsByItemandOperationandHour[OperationName]'),
                'CU': entry.get('MetricsByItemandOperationandHour[sum_CU]'),
                'UsersCount': entry.get('MetricsByItemandOperationandHour[count_users]'),
                'Duration (s)': entry.get('MetricsByItemandOperationandHour[sum_duration]'),
                'Throttling (min)': entry.get('MetricsByItemandOperationandHour[Throttling (min)]'),
                'RejectedOperationsCount': entry.get('MetricsByItemandOperationandHour[count_rejected_operations]'),
                })

        return result

    def format_key(self, key) -> str:
        return str(key).replace('T', ' ')
