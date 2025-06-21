from ..batch_result import CollectorCollection

class DatamartsScanner:
    def map(self, scanResult):
        result = CollectorCollection("Datamarts")

        for workspace in scanResult['workspaces']:
            if workspace.get('datamarts') is not None:
                for item in workspace['datamarts']:
                    result.append({
                        'Id': item.get('id'),
                        'Name': item.get('name'),
                        'Type': item.get('type'),
                        'Description': item.get('description'),
                        'ConfiguredBy': item.get('configuredBy'),
                        'ModifiedBy': item.get('modifiedBy'),
                        'ModifiedDateTime': item.get('modifiedDateTime'),
                        'SensitivityLabel': item.get('sensitivityLabel', {}).get('labelId'),
                        'DatasourceUsages': item.get('datasourceUsages'),
                        'Endorsement': item.get('endorsementDetails', {}).get('endorsement'),
                        'CertifiedBy': item.get('endorsementDetails', {}).get('certifiedBy'),
                        'WorkspaceId': workspace.get('id'),
                        })
            
        return result