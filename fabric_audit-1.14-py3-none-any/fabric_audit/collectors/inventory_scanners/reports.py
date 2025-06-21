from ..batch_result import CollectorCollection

class ReportsScanner:
    def map(self, scanResult):
        result = CollectorCollection("Reports")

        for workspace in scanResult['workspaces']:
            if workspace.get('reports') is not None:
                for item in workspace['reports']:
                    result.append({
                        'Id': item.get('id'),
                        'Name': item.get('name'),
                        'ReportType': item.get('reportType'),
                        'DatasetId': item.get('datasetId'),
                        'CreatedBy': item.get('createdBy'),
                        'CreatedDateTime': item.get('createdDateTime'),
                        'ModifiedBy': item.get('modifiedBy'),
                        'ModifiedDateTime': item.get('modifiedDateTime'),
                        'SensitivityLabel': item.get('sensitivityLabel', {}).get('labelId'),
                        'Endorsement': item.get('endorsementDetails', {}).get('endorsement'),
                        'CertifiedBy': item.get('endorsementDetails', {}).get('certifiedBy'),
                        'WorkspaceId': workspace.get('id'),
                        })
            
        return result