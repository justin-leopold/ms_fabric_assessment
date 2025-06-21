from ..batch_result import CollectorCollection

class ModelsScanner:
    def map(self, scanResult):
        result = CollectorCollection("SemanticModels")

        for workspace in scanResult['workspaces']:
            if workspace.get('datasets') is not None:
                for item in workspace['datasets']:
                    result.append({
                        'Id': item.get('id'),
                        'Name': item.get('name'),
                        'ConfiguredBy': item.get('configuredBy'),
                        'CreatedDate': item.get('createdDate'),
                        'TargetStorageMode': item.get('targetStorageMode'),
                        'ContentProviderType': item.get('contentProviderType'),
                        'SensitivityLabel': item.get('sensitivityLabel', {}).get('labelId'),
                        'WorkspaceId': workspace.get('id'),
                        'Relations': item.get('relations'),
                        'Endorsement': item.get('endorsementDetails', {}).get('endorsement'),
                        'CertifiedBy': item.get('endorsementDetails', {}).get('certifiedBy'),
                        'Tables': item.get('tables'),
                        'DatasourceUsages': ','.join([usage.get('datasourceInstanceId') for usage in item.get('datasourceUsages', [])])
                        })
            
        return result