from .batch_result import BatchResult, CollectorCollection

class DeploymentPipelinesCollector:
    def __init__(self):
        self.name = "Deployment Pipelines"
        self.active = True
        self.batch_size = 500

    def collect(self, context, next_batch_id: str):

        batch_index = 0
        if next_batch_id is not None:
            batch_index = int(next_batch_id)

        skip = self.batch_size * batch_index
        reponse = context.clients['pbi'].get(f'v1.0/myorg/admin/pipelines?$skip={skip}&$top={self.batch_size}&$expand=stages,users', additional_headers={"Content-Type": "application/json"})
        
        result = BatchResult()
        if reponse is not None:
            if not hasattr(reponse, 'error'):
                result.append(self.__map_items(reponse))
            else:
                return None

        return result
    

    def __map_items(self, items):
        result = CollectorCollection("DeploymentPipelines")

        for item in items['value']:
            result.append({
                'Id': item.get('id'),
                'DisplayName': item.get('displayName'),
                'Stages': item.get('stages'),
                'Users': item.get('users')
                })
            
        return result
