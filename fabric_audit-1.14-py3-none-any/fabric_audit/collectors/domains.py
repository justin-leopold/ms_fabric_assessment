from .batch_result import BatchResult, CollectorCollection

class DomainsCollector:
    def __init__(self):
        self.name = "Domains"
        self.active = True

    def collect(self, context, next_batch_id: str):

        reponse = context.clients['fabric'].get('v1/admin/domains', additional_headers={"Content-Type": "application/json"})
        
        result = BatchResult()
        if reponse is not None:
            if not hasattr(reponse, 'error'):
                result.append(self.__map_items(reponse))
            else:
                return None

        return result
    

    def __map_items(self, items):
        result = CollectorCollection("Domains")

        for item in items['domains']:
            result.append({
                'Id': item.get('id'),
                'DisplayName': item.get('displayName'),
                'Description': item.get('description'),
                'ParentDomainId': item.get('parentDomainId'),
                'ContributorsScope': item.get('contributorsScope'),
                })
            
        return result
