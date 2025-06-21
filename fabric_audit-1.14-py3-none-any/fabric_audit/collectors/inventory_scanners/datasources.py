from ..batch_result import CollectorCollection

class DatasourcesScanner:
    def map(self, scanResult):
        result = CollectorCollection("Datasources")

        if scanResult.get('datasourceInstances') is not None:
            for item in scanResult['datasourceInstances']:
                result.append({
                    'DatasourceType': item.get('datasourceType'),
                    'ConnectionDetails': item.get('connectionDetails'),
                    'GatewayId': item.get('gatewayId'),
                    'DatasourceId': item.get('datasourceId')
                    })
            
        return result