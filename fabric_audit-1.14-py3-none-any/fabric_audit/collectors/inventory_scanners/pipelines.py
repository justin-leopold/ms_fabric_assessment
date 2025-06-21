from ..batch_result import CollectorCollection

class PipelinesScanner:
    def map(self, scanResult):
        result = CollectorCollection("Pipelines")

        for workspace in scanResult['workspaces']:
            if workspace.get('DataPipeline') is not None:
                for item in workspace['DataPipeline']:
                    result.append({
                        'Id': item.get('id'),
                        'Name': item.get('name'),
                        'State': item.get('state'),
                        'Description': item.get('description'),
                        'ConfiguredBy': item.get('configuredBy'),
                        'ModifiedBy': item.get('modifiedBy'),
                        'ModifiedDateTime': item.get('modifiedDateTime'),
                        'SensitivityLabel': item.get('sensitivityLabel', {}).get('labelId'),
                        'Endorsement': item.get('endorsementDetails', {}).get('endorsement'),
                        'CertifiedBy': item.get('endorsementDetails', {}).get('certifiedBy'),
                        'WorkspaceId': workspace.get('id'),
                        })
            
        return result