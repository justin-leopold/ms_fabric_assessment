from ..batch_result import CollectorCollection

class ExplorationsScanner:
    def map(self, scanResult):
        result = CollectorCollection("Explorations")

        for workspace in scanResult['workspaces']:
            if workspace.get('Exploration') is not None:
                for item in workspace['Exploration']:
                    result.append({
                        'Id': item.get('id'),
                        'Name': item.get('name'),
                        'Description': item.get('description'),
                        'State': item.get('state'),
                        'CreatedBy': item.get('createdBy'),
                        'ModifiedBy': item.get('modifiedBy'),
                        'CreatedDate': item.get('createdDate'),
                        'LastUpdatedDate': item.get('lastUpdatedDate'),
                        'SensitivityLabel': item.get('sensitivityLabel', {}).get('labelId'),
                        'Endorsement': item.get('endorsementDetails', {}).get('endorsement'),
                        'CertifiedBy': item.get('endorsementDetails', {}).get('certifiedBy'),
                        'WorkspaceId': workspace.get('id'),
                        })
            
        return result