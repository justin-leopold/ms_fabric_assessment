from .capacity_query_base import CapacityQueryBase
from .batch_result import CollectorCollection

class CapacitySummaryCollector(CapacityQueryBase):
    def __init__(self):
        super().__init__()
        self.name = "Capacity Summary"
        self.batching_query = '''EVALUATE SELECTCOLUMNS(SUMMARIZECOLUMNS(
                        CUDetail[Start of Hour],
                        "SetSize", COUNTROWS(CUDetail)
                    ), 
         	"SetKey", CUDetail[Start of Hour], 
         	"SetSize", [SetSize]
        )'''
        self.query_template = '''EVALUATE CALCULATETABLE(SUMMARIZE(
                        CUDetail,
                        CUDetail[Start of Hour],
                        "CUs", SUM(CUDetail[CUs]),
                        "MinBaseUnits", MIN(CUDetail[BaseCapacityUnits]),
                        "MaxBaseUnits", MAX(CUDetail[BaseCapacityUnits]),
                        "MinAutoScaleUnits", MIN(CUDetail[AutoScaleCapacityUnits]),
                        "MaxAutoScaleUnits", MAX(CUDetail[AutoScaleCapacityUnits]),
                        "Interactive", SUM(CUDetail[Interactive]),
                        "Interactive Delay %", SUM(CUDetail[Interactive Delay %]),
                        "Interactive Rejection %", SUM(CUDetail[Interactive Rejection %]),
                        "Background", SUM(CUDetail[Background]),
                        "Background Rejection %", SUM(CUDetail[Background Rejection %])
                    ), TREATAS({{{keys_text}}}, CUDetail[Start of Hour]))'''
    
    def map_data(self, metrics) -> CollectorCollection:
        result = CollectorCollection("CapacitySummary")

        for entry in metrics:
            result.append({
                'DateTime': entry.get('CUDetail[Start of Hour]'),
                'CUs': entry.get('[CUs]'),
                'MinBaseUnits': entry.get('[MinBaseUnits]'),
                'MaxBaseUnits': entry.get('[MaxBaseUnits]'),
                'MinAutoScaleUnits': entry.get('[MinAutoScaleUnits]'),
                'MaxAutoScaleUnits': entry.get('[MaxAutoScaleUnits]'),
                'Interactive': entry.get('[Interactive]'),
                'Interactive Delay %': entry.get('[Interactive Delay %]'),
                'Interactive Rejection %': entry.get('[Interactive Rejection %]'),
                'Background': entry.get('[Background]'),
                'Background Rejection %': entry.get('[Background Rejection %]')
                })
            
        return result
    
    def format_key(self, key) -> str:
        return str(key).replace('T', ' ')
