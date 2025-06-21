from ..batch_result import CollectorCollection

class WorkspaceUsersScanner:
    def map(self, scanResult):
        result = CollectorCollection("WorkspaceUsers")

        for workspace in scanResult['workspaces']:
            if workspace.get('users') is not None:
                for item in workspace['users']:
                    result.append({
                        'EmailAddress': item.get('emailAddress'),
                        'GroupUserAccessRight': item.get('groupUserAccessRight'),
                        'Identifier': item.get('identifier'),
                        'PrincipalType': item.get('principalType'),
                        'DisplayName': item.get('displayName'),
                        'WorkspaceId': workspace.get('id'),
                        })
            
        return result