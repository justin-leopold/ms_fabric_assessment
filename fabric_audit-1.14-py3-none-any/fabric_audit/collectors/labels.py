from .batch_result import BatchResult, CollectorCollection
from .query_base import QueryBase

class LabelsCollector(QueryBase):
    def __init__(self):
        super().__init__();
        self.name = "Labels"

    def is_valid(self, context):
        return context.purview_model_id is not None
    
    def required_information(self):
        return "Purview Hub semantic model ID"

    def collect(self, context, next_batch_id: str):
        self.semantic_model_id = context.purview_model_id

        labels = self.query_model('EVALUATE SUMMARIZECOLUMNS(\'Fabric Items\'[MIP label Id], \'Fabric Items\'[Label name])', context)
        
        result = BatchResult()
        if labels is not None:
            if not hasattr(labels, 'error'):
                result.append(self.__map_items(labels))
            else:
                return None
        else:
            return None

        return result
    

    def __map_items(self, labels):
        result = CollectorCollection("Labels")

        for label in labels:
            result.append({
                'Id': label.get('Fabric Items[MIP label Id]'),
                'Name': label.get('Fabric Items[Label name]')
                })
            
        return result