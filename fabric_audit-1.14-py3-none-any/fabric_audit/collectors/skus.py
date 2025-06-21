from .batch_result import BatchResult, CollectorCollection
from lxml import etree
from io import StringIO
import requests

class SKUsCollector():
    def __init__(self):
        self.name = "SKUs"
        self.active = True

    def collect(self, context, next_batch_id: str):
        result = BatchResult()
        collection = CollectorCollection('SKUs')
        lines = [["P1", 25, 50, 30, 10, 40, 1500, 64],
                 ["P2", 50, 75, 60, 10, 80, 1500, 128],
                 ["P3", 100, 100, 120, 10, 160, 6000, 256],
                 ["P4", 200, 200, 240, 20, 320, 12000, 512],
                 ["P5", 400, 200, 480, 40, 640, 24000, 1024],
                 ["F2", 3, 5, 2, 1, 1, 300, 2],
                 ["F4", 3, 5, 2, 1, 2, 300, 4],
                 ["F8", 3, 10, 3.75, 1, 5, 300, 8],
                 ["F16", 5, 10, 7.5, 2, 10, 300, 16],
                 ["F32", 10, 10, 15, 5, 20, 300, 32],
                 ["F64", 25, 50, 30, 10, 40, 1500, 64],
                 ["F128", 50, 75, 60, 10, 80, 1500, 128],
                 ["F256", 100, 100, 120, 10, 160, 6000, 256],
                 ["F512", 200, 200, 240, 20, 320, 12000, 512],
                 ["F1024", 400, 200, 480, 40, 640, 24000, 1024],
                 ["F2048", 400, 200, 960, 40, 1280, 24000, 2048],
                 ["FT1", 25, 50, 30, 10, 40, 1500, 64],
                 ["A1", 3, 10, 3.75, 1, 5, 300, 8],
                 ["A2", 5, 10, 7.5, 2, 10, 300, 16],
                 ["A3", 10, 10, 15, 5, 20, 300, 32],
                 ["A4", 25, 50, 30, 10, 40, 1500, 64],
                 ["A5", 50, 75, 60, 10, 80, 1500, 128],
                 ["A6", 100, 100, 120, 10, 160, 6000, 256],
                 ["A7", 200, 200, 240, 20, 320, 12000, 512],
                 ["A8", 400, 200, 480, 40, 640, 24000, 1024],
                 ["DCT1", 25, 50, 30, 10, 40, 1500, 64],
                 ["EM1", 3, 10, 3.75, 1, 5, 300, 8],
                 ["EM2", 5, 10, 7.5, 2, 10, 300, 16],
                 ["EM3", 10, 10, 15, 5, 20, 300, 32]
                 ]

        for sku in lines:
            row = {}
            row['SKU'] = sku[0]
            row['Max memory (GB)'] = sku[1]
            row['Max concurrent DirectQuery connections (per semantic model)'] = sku[2]
            row['Live connection (per second)'] = sku[3]
            row['Max memory per query (GB)'] = sku[4]
            row['Model refresh parallelism'] = sku[5]
            row['Direct Lake rows per table (in millions)'] = sku[6]
            row['CU per Second'] = sku[7]
            collection.append(row)

        result.append(collection)
        return result
