from .capacity_query_base import CapacityQueryBase
from .batch_result import CollectorCollection

class CapacityMemoryCollector(CapacityQueryBase):
    def __init__(self):
        super().__init__()
        self.name = "Capacity Memory"
        self.batching_query = '''EVALUATE SELECTCOLUMNS(SUMMARIZECOLUMNS(
                        MaxMemoryByItemAndHour[Timestamp],
                        "SetSize", COUNTROWS(MaxMemoryByItemAndHour)
                    ), 
         	"SetKey", MaxMemoryByItemAndHour[Timestamp], 
         	"SetSize", [SetSize]
        )'''
        self.query_template = '''EVALUATE SUMMARIZECOLUMNS(
                        MaxMemoryByItemAndHour[Timestamp],
                        MaxMemoryByItemAndHour[ItemId],
                        MaxMemoryByItemAndHour[SkuMemory],
                        MaxMemoryByItemAndHour[Item Size (GB)],
                        TREATAS({{{keys_text}}}, MaxMemoryByItemAndHour[Timestamp])
                    )'''
    
    def map_data(self, metrics) -> CollectorCollection:
        result = CollectorCollection("CapacityMemory")

        for entry in metrics:
            result.append({
                'Timestamp': entry.get('MaxMemoryByItemAndHour[Timestamp]'),
                'ItemId': entry.get('MaxMemoryByItemAndHour[ItemId]'),
                'SkuMemory': entry.get('MaxMemoryByItemAndHour[SkuMemory]'),
                'ItemSizeGb': entry.get('MaxMemoryByItemAndHour[Item Size (GB)]')
                })
            
        return result
    
    def format_key(self, key) -> str:
        return str(key).replace('T', ' ')
