from .batch_result import BatchResult, CollectorCollection
import requests
import csv
import re

class ServicePlansCollector():
    def __init__(self):
        self.name = "ServicePlans"
        self.active = True
    
    def collect(self, context, next_batch_id: str):
        article = requests.get('https://learn.microsoft.com/en-us/entra/identity/users/licensing-service-plan-reference')
        file_url = re.search("https[^<>]*licensing.csv", article.text).group()

        response = requests.get(file_url)
        if response.status_code == 200:
            csv_reader = csv.DictReader(response.text.splitlines(), delimiter=',')
            result = BatchResult()
            collection = CollectorCollection('ServicePlans')
            for row in csv_reader:
                collection.append(row)
            result.append(collection)
            return result
    