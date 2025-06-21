from .batch_result import BatchResult, CollectorCollection
import requests
import re

class GatewayVersionsCollector():
    def __init__(self):
        self.name = "Gateway Versions"
        self.active = True
    
    def collect(self, context, next_batch_id: str):
        response = requests.get('https://www.microsoft.com/en-us/download/details.aspx?id=53127', headers={"User-Agent": "Fabric Assessment"})
        if response.status_code == 200:
            content = response.text
            version_match = re.findall('"version":"([^"]+)"', content)
            date_match = re.findall('"datePublished":"([^"]+)"', content)
            result = BatchResult()
            collection = CollectorCollection('GatewayLatestVersion')
            row = {}
            row['Version'] = version_match[0]
            row['Date Published'] = date_match[0]
            collection.append(row)
            result.append(collection)
            return result
    