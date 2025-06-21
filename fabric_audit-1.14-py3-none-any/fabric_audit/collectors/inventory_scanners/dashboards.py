from ..batch_result import CollectorCollection

class DashboardsScanner:
    def map(self, scanResult):
        result = CollectorCollection("Dashboards")

        for workspace in scanResult['workspaces']:
            if workspace.get('dashboards') is not None:
                for item in workspace['dashboards']:
                    result.append({
                        'Id': item.get('id'),
                        'DisplayName': item.get('displayName'),
                        'IsReadOnly': item.get('isReadOnly'),
                        'EmbedUrl': item.get('embedUrl'),
                        'SensitivityLabel': item.get('sensitivityLabel', {}).get('labelId'),
                        'WorkspaceId': workspace.get('id'),
                        })
            
        return result