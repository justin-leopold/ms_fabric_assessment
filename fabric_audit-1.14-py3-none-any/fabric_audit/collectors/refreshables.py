from .batch_result import BatchResult, CollectorCollection
import math
import json

class RefreshablesCollector:
    def __init__(self):
        self.name = "Refreshables"
        self.active = True
        self.batch_size = 1000
        self.batch_list = None
    
    def collect(self, context, next_batch_id: str):
        current_batch = 0
        if next_batch_id is not None:
            current_batch = int(next_batch_id)

        uri = f'v1.0/myorg/admin/capacities/refreshables?$top={self.batch_size}'
        if current_batch > 0:
            uri = uri + f'&$skip={current_batch * self.batch_size}'

        response = context.clients['pbi'].get(uri, additional_headers={"Content-Type": "application/json"})
        if response is not None:
            if not hasattr(response, 'error'):
                refreshables = response.get('value')
                total_count = int(response.get('@odata.count'))

                if self.batch_list is None and self.batch_size < total_count:
                    batch_count = math.floor(total_count * 1.0/self.batch_size)
                    self.batch_list = range(batch_count)

                result = BatchResult()
                result.append(self.__map_refreshables(refreshables))
                if len(refreshables) >= self.batch_size:
                    result.next_batch_id = str(current_batch + 1)

                if self.batch_list is not None:
                    result.batch_progress = current_batch / len(self.batch_list)
            else:
                return None

        return result
    
    def __map_refreshables(self, items):
        result = CollectorCollection(f'Refreshables')
        for item in items:
            result.append({
                'Id': item.get('id'),
                'Name': item.get('name'),
                'Kind': item.get('kind'),
                'StartTime': item.get('startTime'),
                'EndTime': item.get('endTime'),	
                'RefreshCount': item.get('refreshCount'),	
                'RefreshFailures': item.get('refreshFailures'),	
                'AverageDuration': item.get('averageDuration'),	
                'MedianDuration': item.get('medianDuration'),	
                "RefreshesPerDay": item.get('refreshesPerDay'),			
                "LastRefresh": json.dumps(item.get('lastRefresh')),		
                "RefreshSchedule": json.dumps(item.get('refreshSchedule')),	
                "ConfiguredBy": item.get('configuredBy'),		
                })
            
        return result