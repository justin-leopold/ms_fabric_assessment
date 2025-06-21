from .capacity_query_base import CapacityQueryBase
from .batch_result import CollectorCollection

class CapacityUtilizationCollector(CapacityQueryBase):
    def __init__(self):
        super().__init__()
        self.name = "Capacity Utilization"
        self.batching_query = '''EVALUATE SELECTCOLUMNS(SUMMARIZECOLUMNS(
                        'TimePoints'[TimePoint],
                        __CapacityFilterTable,
                        FILTER(TimePoints,'All Measures'[CU Limit] == 1),
                        "SetSize", COUNTROWS(TimePoints)
                    ),
         	"SetKey", 'TimePoints'[TimePoint],
         	"SetSize", [SetSize]
        )'''
        self.query_template = '''EVALUATE CALCULATETABLE(SUMMARIZECOLUMNS(
                    'TimePoints'[TimePoint],
                    __CapacityFilterTable,
                    "CapacityId", IGNORE(CALCULATE(MIN('Capacities'[capacityId]))),
                    "CU_Limit", 'All Measures'[CU Limit],
                    "Cumulative_CU_Usage__s_", IGNORE('All Measures'[Cumulative CU Usage (s)]),
                    "xInteractive", IGNORE('All Measures'[xInteractive]),
                    "xBackground", IGNORE('All Measures'[xBackground]),
                    "xInteractivePreview", IGNORE('All Measures'[xInteractivePreview]),
                    "xBackgroundPreview", IGNORE('All Measures'[xBackgroundPreview]),
                    "SKU_CU_by_TimePoint", IGNORE('All Measures'[SKU CU by TimePoint]),
                    "MinPremiumCapacityState", IGNORE(CALCULATE(MIN('SystemEvents'[PremiumCapacityState])))
                    ), TREATAS({{{keys_text}}}, 'TimePoints'[TimePoint]))'''

    def map_data(self, metrics) -> CollectorCollection:
        result = CollectorCollection("CapacityUtilization")

        for entry in metrics:
            result.append({
                'TimePoint': entry.get('TimePoints[TimePoint]'),
                'CapacityId': entry.get('[CapacityId]'),
                'TotalCUs': entry.get('[Cumulative_CU_Usage__s_]'),
                'InteractiveCUs': entry.get('[xInteractive]'),
                'BackgroundCUs': entry.get('[xBackground]'),
                'InteractivePreviewCUs': entry.get('[xInteractivePreview]'),
                'BackgroundPreviewCUs': entry.get('[xBackgroundPreview]'),
                'SkuCUsbyTimePoint': entry.get('[SKU_CU_by_TimePoint]'),
                'PremiumCapacityState': entry.get('[MinPremiumCapacityState]')
                })

        return result

    def format_key(self, key) -> str:
        return str(key).replace('T', ' ')
