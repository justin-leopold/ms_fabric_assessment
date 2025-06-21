from ..batch_result import CollectorCollection

class DataflowsScanner:
    def map(self, scanResult):
        result = CollectorCollection("Dataflows")

        for workspace in scanResult['workspaces']:
            if workspace.get('dataflows') is not None:
                for item in workspace['dataflows']:
                    result.append({
                        'Id': item.get('objectId'),
                        'Name': item.get('name'),
                        'ConfiguredBy': item.get('configuredBy'),
                        'Description': item.get('description'),
                        'ModifiedBy': item.get('modifiedBy'),
                        'ModifiedDateTime': item.get('modifiedDateTime'),
                        'SensitivityLabel': item.get('sensitivityLabel', {}).get('labelId'),
                        'DatasourceUsages': item.get('datasourceUsages'),
                        'Generation': item.get('generation'),
                        'Endorsement': item.get('endorsementDetails', {}).get('endorsement'),
                        'CertifiedBy': item.get('endorsementDetails', {}).get('certifiedBy'),
                        'WorkspaceId': workspace.get('id'),
                        })
            
        return result