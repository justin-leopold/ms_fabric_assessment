from .batch_result import BatchResult, CollectorCollection

class CapacitiesCollector:
    def __init__(self):
        self.name = "Capacities"
        self.active = True

    def collect(self, context, next_batch_id: str):

        capacities = context.clients['pbi'].get('v1.0/myorg/admin/capacities', additional_headers={"Content-Type": "application/json"})
        
        result = BatchResult()
        if capacities is not None:
            if not hasattr(capacities, 'error'):
                result.append(self.__map_capacities(capacities))
            else:
                return None

        return result
    

    def __map_capacities(self, capacities):
        result = CollectorCollection("Capacities")

        for item in capacities['value']:
            result.append({
                'Id': item.get('id'),
                'DisplayName': item.get('displayName'),
                'SKU': item.get('sku'),
                'State': item.get('state'),
                'Region': item.get('region'),
                'CapacityUserAccessRight': item.get('capacityUserAccessRight'),
                'Admins': item.get('admins'),
                })
            
        return result