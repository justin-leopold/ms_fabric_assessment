from .batch_result import BatchResult, CollectorCollection

class SubscribedSkusCollector:
    def __init__(self):
        self.name = "OrgLicenses"
        self.active = True

    def collect(self, context, next_batch_id: str):

        skus = context.clients['graph'].get('v1.0/subscribedSkus', additional_headers={"Content-Type": "application/json"})
        
        result = BatchResult()
        if skus is not None:
            if not hasattr(skus, 'error'):
                result.append(self.__map_skus(skus))
            else:
                return None

        return result
    

    def __map_skus(self, items):
        result = CollectorCollection("OrgLicenses")

        for item in items['value']:
            result.append({
                'SkuPartNumber': item.get('skuPartNumber'),
                'Enabled': item.get('prepaidUnits', {}).get('enabled'),
                'LockedOut': item.get('prepaidUnits', {}).get('lockedOut'),
                'Suspended': item.get('prepaidUnits', {}).get('suspended'),
                'Warning': item.get('prepaidUnits', {}).get('warning'),
                'Consumed': item.get('consumedUnits'),
                })
            
        return result
