from .batch_result import BatchResult, CollectorCollection
import json

class GatewaysCollector:
    def __init__(self):
        self.name = "Gateways"
        self.active = True

    def collect(self, context, next_batch_id: str):

        items = context.clients['pbi'].get('v2.0/myorg/me/gatewayClusters?$expand=memberGateways', additional_headers={"Content-Type": "application/json"})
        
        result = BatchResult()
        if items is not None:
            if not hasattr(items, 'error'):
                result.append(self.__map_gateways(items))
            else:
                return None

        return result
    

    def __map_gateways(self, items):
        result = CollectorCollection("Gateways")

        for item in items['value']:
            for member in item.get('memberGateways'):
                record = {
                    'clusterId': item.get('id'),
                    'clusterName': item.get('name'),
                    'type': item.get('type'),
                    'cloudDatasourceRefresh': item.get('options', {}).get('CloudDatasourceRefresh'),
                    'customConnectors': item.get('options', {}).get('CustomConnectors'),
                    'version': member.get('version'),
                    'status': member.get('status'),
                    'versionStatus': member.get('versionStatus'),
                    'nodeId': member.get('nodeId'),
                    }
                annotation = member.get('annotation')
                if annotation is not None:
                    a_json = json.loads(annotation)
                    record['machine'] = a_json.get('gatewayMachine')
                    record['contactInformation'] = a_json.get('gatewayContactInformation'),
                result.append(record)
            
        return result