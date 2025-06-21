import json
from .batch_result import BatchResult, CollectorCollection

class TenantCollector:
    def __init__(self):
        self.name = "Tenant"
        self.active = True

    def collect(self, context, next_batch_id: str):
        response = context.clients['graph'].get('v1.0/organization', additional_headers={"Content-Type": "application/json"})
        
        result = BatchResult()
        if response is not None:
            if not hasattr(response, 'error'):
                result.append(self.__map_org(response))
            else:
                return None

        return result
    

    def __map_org(self, items):
        result = CollectorCollection("Tenant")

        tenant = sorted(
            [item for sublist in map(lambda x: x.get('verifiedDomains', []), items.get('value', [])) for item in sublist], 
            key = lambda d: d.get('isDefault', False), reverse=True
            )[0]

        result.append({
            'Tenant': tenant.get('name'),
            })
            
        return result