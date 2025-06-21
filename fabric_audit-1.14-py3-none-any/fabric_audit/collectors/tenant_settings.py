from .batch_result import BatchResult, CollectorCollection

class TenantSettingsCollector:
    def __init__(self):
        self.name = "TenantSettings"
        self.active = True

    def collect(self, context, next_batch_id: str):

        settings = context.clients['fabric'].get('v1/admin/tenantsettings', additional_headers={"Content-Type": "application/json"})
        
        result = BatchResult()
        if settings is not None:
            if not hasattr(settings, 'error'):
                result.append(self.__map_tenant_settings(settings))
            else:
                return None

        return result
    

    def __map_tenant_settings(self, settings):
        result = CollectorCollection("TenantSettings")

        settingsContainer = settings.get('tenantSettings')
        if(settingsContainer is None):
            settingsContainer = settings.get('value')

        for item in settingsContainer:
            result.append({
                'SettingName': item.get('settingName'),
                'Title': item.get('title'),
                'IsEnabled': item.get('enabled'),
                'CanSpecifySecurityGroups': item.get('canSpecifySecurityGroups'),
                'TenantSettingGroup': item.get('tenantSettingGroup'),
                'EnabledSecurityGroups': item.get('enabledSecurityGroups'),
                'ExcludedSecurityGroups': item.get('excludedSecurityGroups')
                })
            
        return result