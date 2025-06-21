from ..batch_result import CollectorCollection

class LakehousesScanner:
    def map(self, scanResult):
        result = CollectorCollection("Lakehouses")

        for workspace in scanResult['workspaces']:
            if workspace.get('Lakehouse') is not None:
                for item in workspace['Lakehouse']:
                    result.append({
                        'Id': item.get('id'),
                        'Name': item.get('name'),
                        'Type': item.get('type'),
                        'Description': item.get('description'),
                        'ConfiguredBy': item.get('configuredBy'),
                        'ModifiedBy': item.get('modifiedBy'),
                        'CreatedDate': item.get('createdDate'),
                        'LastUpdatedDate': item.get('lastUpdatedDate'),
                        'SensitivityLabel': item.get('sensitivityLabel', {}).get('labelId'),
                        'DatasourceUsages': item.get('datasourceUsages'),
                        'Endorsement': item.get('endorsementDetails', {}).get('endorsement'),
                        'CertifiedBy': item.get('endorsementDetails', {}).get('certifiedBy'),
                        'WorkspaceId': workspace.get('id'),
                        })
        
        return result