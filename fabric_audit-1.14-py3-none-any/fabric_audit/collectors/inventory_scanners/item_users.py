from ..batch_result import CollectorCollection

class ItemUsersScanner:
    def map(self, scanResult):
        result = CollectorCollection("ItemUsers")

        for workspace in scanResult['workspaces']:
            items = []
            items.extend(workspace.get('reports', []))
            items.extend(workspace.get('dashboards', []))
            items.extend(workspace.get('dataflows', []))
            items.extend(workspace.get('datamarts', []))
            items.extend(workspace.get('eventhouses', []))
            items.extend(workspace.get('lakehouses', [])) 
            items.extend(workspace.get('ml_models', [])) 
            items.extend(workspace.get('notebooks', []))
            items.extend(workspace.get('pipelines', [])) 
            items.extend(workspace.get('warehouses', []))
            for item in items:
                for user in item.get('users', []):
                    accessRights = [k for k in user.keys() if k.endswith('UserAccessRight')]
                    result.append({
                        'ItemId': item.get('id', item.get('objectId')),
                        'Identifier': user.get('identifier'),
                        'PrincipalType': user.get('principalType'),
                        'UserType': user.get('userType'),
                        'DisplayName': user.get('displayName'),
                        'AccessRight': user[accessRights[0]] if len(accessRights) > 0 else None,
                        })
            
        return result