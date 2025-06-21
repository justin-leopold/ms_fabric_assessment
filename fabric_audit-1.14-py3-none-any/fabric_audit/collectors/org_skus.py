from .batch_result import BatchResult, CollectorCollection

class OrgSkusCollector:
    def __init__(self):
        self.name = "OrgSkus"
        self.active = True

    def collect(self, context, next_batch_id: str):

        skus = context.clients['graph'].get('v1.0/directory/subscriptions', additional_headers={"Content-Type": "application/json"})

        result = BatchResult()
        if skus is not None:
            if not hasattr(skus, 'error'):
                result.append(self.__map_skus(skus))
            else:
                return None

        return result
    

    def __map_skus(self, items):
        result = CollectorCollection("OrgSkus")

        for item in items['value']:
            services = item.get('serviceStatus')
            if services is not None and len(services) > 0:
                for service in services:
                    result.append({
                        'SkuId': item.get('skuId'),
                        'SkuPartNumber': item.get('skuPartNumber'),
                        'TotalLicenses': item.get('totalLicenses'),
                        'ServicePlanId': service.get('servicePlanId'),
                        'ServicePlanName': service.get('servicePlanName')
                        })
            else:
                result.append({
                        'SkuId': item.get('skuId'),
                        'SkuPartNumber': item.get('skuPartNumber'),
                        'TotalLicenses': item.get('totalLicenses'),
                        'ServicePlanId': '',
                        'ServicePlanName': ''
                        })
            
            
        return result
