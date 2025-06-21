from ..batch_result import CollectorCollection

class NotebooksScanner:
    def map(self, scanResult):
        result = CollectorCollection("Notebooks")

        for workspace in scanResult['workspaces']:
            if workspace.get('Notebook') is not None:
                for item in workspace['Notebook']:
                    result.append({
                        'Id': item.get('id'),
                        'Name': item.get('name'),
                        'Description': item.get('description'),
                        'State': item.get('state'),
                        'ConfiguredBy': item.get('configuredBy'),
                        'ModifiedBy': item.get('modifiedBy'),
                        'CreatedDate': item.get('createdDate'),
                        'LastUpdatedDate': item.get('lastUpdatedDate'),
                        'SensitivityLabel': item.get('sensitivityLabel', {}).get('labelId'),
                        'Endorsement': item.get('endorsementDetails', {}).get('endorsement'),
                        'CertifiedBy': item.get('endorsementDetails', {}).get('certifiedBy'),
                        'WorkspaceId': workspace.get('id'),
                        })
            
        return result