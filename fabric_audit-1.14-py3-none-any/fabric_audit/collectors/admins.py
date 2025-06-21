from .batch_result import BatchResult, CollectorCollection

class AdminsCollector:
    def __init__(self):
        self.name = "Admins"
        self.active = True
        self.batch_list = []

    def collect(self, context, next_batch_id: str):

        batch_index = 0
        if next_batch_id is None:
            self.__populate_batch_list(context)
        else:  
            batch_index = int(next_batch_id)

        if len(self.batch_list) > 0:
            role_id = self.batch_list[batch_index].get('id')
            members = context.clients['graph'].get(f'v1.0/directoryRoles/{role_id}/members', additional_headers={"Content-Type": "application/json"})

            result = BatchResult()
            if members is not None:
                if not hasattr(members, 'error'):
                    result.append(self.__map_members(self.batch_list[batch_index], members))
                    if len(self.batch_list) > batch_index + 1:
                        result.next_batch_id = str(batch_index + 1)
                else:
                    return None

            return result

    def __populate_batch_list(self, context):
        roles = context.clients['graph'].get('v1.0/directoryRoles', additional_headers={"Content-Type": "application/json"})
        if not hasattr(roles, 'error'):
            for role in roles.get('value'):
                if role.get('displayName') in ['Fabric Administrator', 'Global Administrator']:
                    self.batch_list.append(role)

    def __map_members(self, role, members):
        result = CollectorCollection("Admins")

        for item in members['value']:
            result.append({
                'Role': role.get('displayName'),
                'DisplayName': item.get('displayName'),
                'Mail': item.get('mail'),
                'UserPrincipalName': item.get('userPrincipalName'),
                'BusinessPhones': item.get('businessPhones')
                })
            
        return result