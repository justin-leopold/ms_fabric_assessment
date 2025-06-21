from ..batch_result import CollectorCollection

class WorkspacesScanner:
    def map(self, scanResult):
        result = CollectorCollection("Workspaces")

        for workspace in scanResult['workspaces']:
            result.append({
                'Id': workspace.get('id'),
                'Name': workspace.get('name'),
                'IsReadOnly': workspace.get('isReadOnly'),
                'IsOnDedicatedCapacity': workspace.get('isOnDedicatedCapacity'),
                'CapacityId': workspace.get('capacityId'),
                'Description': workspace.get('description'),
                'Type': workspace.get('type'),
                'State': workspace.get('state'),
                'IsOrphaned': workspace.get('isOrphaned'),
                'DomainId': workspace.get('domainId'),
                'DefaultDatasetStorageFormat': workspace.get('defaultDatasetStorageFormat')
                })
            
        return result