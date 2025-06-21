from .capacity_query_base import CapacityQueryBase
from .batch_result import CollectorCollection

class CapacityStorageCollector(CapacityQueryBase):
    def __init__(self):
        super().__init__()
        self.name = "Capacity Storage"
        self.batching_query = '''EVALUATE SELECTCOLUMNS(SUMMARIZECOLUMNS(
                        StorageByWorkspacesandHour[Date],
                        "SetSize", COUNTROWS(StorageByWorkspacesandHour)
                    ), 
         	"SetKey", StorageByWorkspacesandHour[Date], 
         	"SetSize", [SetSize]
        )'''
        self.query_template = '''EVALUATE SUMMARIZECOLUMNS(
                        StorageByWorkspacesandHour[WorkspaceId],
                        StorageByWorkspacesandHour[OperationName],
                        StorageByWorkspacesandHour[Billing type],
                        StorageByWorkspacesandHour[StorageType],
                        StorageByWorkspacesandHour[StaticStorageInGb],
                        StorageByWorkspacesandHour[Utilization (GB)],
                        StorageByWorkspacesandHour[WorkloadKind],
                        StorageByWorkspacesandHour[Date],
                        TREATAS({{{keys_text}}}, StorageByWorkspacesandHour[Date])
                    )'''
    
    def map_data(self, metrics) -> CollectorCollection:
        result = CollectorCollection("CapacityStorage")

        for entry in metrics:
            result.append({
                'WorkspaceId': entry.get('StorageByWorkspacesandHour[WorkspaceId]'),
                'OperationName': entry.get('StorageByWorkspacesandHour[OperationName]'),
                'BillingType': entry.get('StorageByWorkspacesandHour[Billing type]'),
                'StorageType': entry.get('StorageByWorkspacesandHour[StorageType]'),
                'StaticStorageInGb': entry.get('StorageByWorkspacesandHour[StaticStorageInGb]'),
                'UtilizationGb': entry.get('StorageByWorkspacesandHour[Utilization (GB)]'),
                'WorkloadKind': entry.get('StorageByWorkspacesandHour[WorkloadKind]'),
                'Date': entry.get('StorageByWorkspacesandHour[Date]')
                })
            
        return result
    
    def format_key(self, key) -> str:
        return str(key).replace('T', ' ')
