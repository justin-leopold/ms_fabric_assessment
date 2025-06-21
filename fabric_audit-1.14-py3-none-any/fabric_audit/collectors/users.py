from .batch_result import BatchResult, CollectorCollection
import math

class UsersCollector:
    def __init__(self):
        self.name = "Users"
        self.active = True
        self.batch_size = 999

    def collect(self, context, next_batch_id: str):

        uri = f'v1.0/users?$select=id,companyName,department,displayName,userPrincipalName,userType,assignedLicenses&$top={self.batch_size}'
        if next_batch_id is not None:
            uri = next_batch_id

        response = context.clients['graph'].get(uri, additional_headers={"Content-Type": "application/json"})
        
        if response is not None:
            if not hasattr(response, 'error'):
                users = response.get('value')

                result = BatchResult()
                result.append(self.__map_users(users))
                result.append(self.__map_user_licenses(users))

                if response.get('@odata.nextLink') is not None:
                    result.next_batch_id = response.get('@odata.nextLink') 
            else:
                return None

        return result
    

    def __map_users(self, users):
        result = CollectorCollection("Users")

        for user in users:
            result.append({
                'Id': user.get('id'),
                'CompanyName': user.get('companyName'),
                'Department': user.get('department'),
                'DisplayName': user.get('displayName'),
                'UserPrincipalName': user.get('userPrincipalName'),
                'UserType': user.get('userType')
                })
            
        return result
    
    def __map_user_licenses(self, users):
        result = CollectorCollection("UserLicenses")

        for user in users:
            for item in user.get('assignedLicenses'):
                result.append({
                    'UserId': user.get('id'),
                    'SkuId': item.get('skuId'),
                    'DisabledPlans': item.get('disabledPlans')
                    })
            
        return result