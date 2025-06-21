class QueryBase:
    def __init__(self):
        self.semantic_model_id = None
        self.active = True

    def query_model(self, query: str, context):
        safe_query = query.replace('\'', '\\\'')
        request = f'{{ queries: [ {{ query: \'{safe_query}\' }}]}}'
        response = context.clients['pbi'].post(f'v1.0/myorg/datasets/{self.semantic_model_id}/executeQueries', data=request)
        if not hasattr(response, 'error'):
            return response.get('results')[0].get('tables')[0].get('rows') 
        else:
            return None
        
    def is_valid(self, context):
        return self.semantic_model_id is not None
    
    def required_information(self):
        return 'Semantic model ID'