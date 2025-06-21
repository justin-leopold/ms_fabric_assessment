from typing import List
from .audit_context import AuditContext
from azure.identity import AzureAuthorityHosts
from .clients import PbiClient, GraphClient, FabricClient
from .collectors import *

class Audit:
    def __init__(self):
        self.context = AuditContext()
        self.__populate_collectors()

    def run(self):
        if self.context.logger is None or self.context.sink is None:
            raise Exception('Sink not configured. Use set_sink(<sink connection string>) method before running the audit')

        self.context.logger.emit(f'Starting audit {self.context.runId}. Module version: {self.version()}')

        self.context.emit()

        self.__setup_clients()
        try:
            self.context.logger.emit('Connecting to the tenant.')

            self.__populate_monitoring_workspace_ids()

            self.context.logger.emit('Running collectors.')
            for collector in self.context.collectors:
                if not collector.active:
                    self.context.logger.emit(f'Skipping collector: {collector.name}.')
                    continue
                
                if hasattr(collector, 'is_valid') and not collector.is_valid(self.context):
                    self.context.logger.emit(f'Collector {collector.name} is missing required information: {collector.required_information()}')
                    continue

                self.context.logger.emit(f'Running collector: {collector.name}.')

                batchIdentifier = None
                while True:
                    batchResult = None

                    try:
                        batchResult = collector.collect(self.context, batchIdentifier)
                    except Exception as collectorException:
                        self.context.logger.error(f'Collector error: {str(collectorException)}', collectorException)

                    if batchResult is not None:
                        log_message = ''
                        if batchResult.batch_friendly_name is None:
                            log_message = f'{collector.name} items collected'
                        else:
                            log_message = f'{collector.name} batch {batchResult.batch_friendly_name} items collected'

                        if batchResult.batch_progress is not None:
                            log_message += f' ({batchResult.batch_progress:.0%})'

                        log_message += ': '

                        collection_labels = []
                        for collectionName in batchResult.collections:
                            collection_labels.append(f"{str(len(batchResult.collections[collectionName].data))} {collectionName}")
                            if len(batchResult.collections[collectionName].data) > 0:
                                self.context.sink.write(batchResult.collections[collectionName])

                        self.context.logger.emit(log_message + ", ".join(collection_labels))

                        if batchResult.next_batch_id is not None:
                            batchIdentifier = batchResult.next_batch_id
                        else:
                            break
                    else:
                        if batchIdentifier is None:
                            self.context.logger.error(f'Collection failed for collector {collector.name}.')
                        else:
                            self.context.logger.error(f'Collection failed for collector {collector.name} batch {batchIdentifier}.')
                        break

            self.context.logger.emit('Audit completed.')
        except Exception as e:
            self.context.logger.error('Audit error', e)
            raise

    def version(self):
        return '1.14'
    
    def list_collectors(self):
        return [c.name for c in self.context.collectors]

    def set_sink(self, sink):
        self.context.set_sink(sink)

    def set_capacity_metrics_dataset_id(self, dataset_id):
        self.context.capacity_metrics_dataset_id = dataset_id

    def set_service_principal(self, tenant_id, client_id, client_secret):
        self.context.set_authentication("ServicePrincipal")
        self.context.set_service_principal(tenant_id, client_id, client_secret)

    def set_flags(self, flags: List[str]):
        self.context.set_flags(flags)

    def set_authentication(self, auth):
        self.context.set_authentication(auth)

    def set_troubleshooting_values(self, delay_s, batch_size):
        self.context.troubleshooting_batch_size = batch_size
        self.context.troubleshooting_delay_s = delay_s

    def set_environment(self, environment:str):
        match environment:
            case 'Public':
                self.context.environment = 'Public'
                self.context.authority = AzureAuthorityHosts.AZURE_PUBLIC_CLOUD
            case 'USGov':
                self.context.environment = 'USGov'
                self.context.authority = AzureAuthorityHosts.AZURE_PUBLIC_CLOUD
            case 'USGovHigh':
                self.context.environment = 'USGovHigh'
                self.context.authority = AzureAuthorityHosts.AZURE_GOVERNMENT
            case 'USGovMil':
                self.context.environment = 'USGovMil'
                self.context.authority = AzureAuthorityHosts.AZURE_GOVERNMENT
            case 'China':
                self.context.environment = 'China'
                self.context.authority = AzureAuthorityHosts.AZURE_CHINA
            case 'Germany':
                self.context.environment = 'Germany'
                self.context.authority = AzureAuthorityHosts.AZURE_GERMANY
            case _:
                raise Exception(f'Environment not supported: {environment}')
                
    def skip_collectors(self, collectors_to_skip:list):
        for to_skip in collectors_to_skip:
            collector_to_skip = None
            for collector in self.context.collectors:
                if collector.name == to_skip:
                    collector_to_skip = collector
            if collector_to_skip is not None:
                collector_to_skip.active = False
            else:
                raise Exception(f'Collector not found when trying to skip: {to_skip}')

    def skip_other_collectors(self, collectors_to_run:list):
        matched_collectors = []
        for collector in self.context.collectors:
            collector.active = collector.name in collectors_to_run
            if collector.active:
                matched_collectors.append(collector.name)

        for requested in collectors_to_run:
            if requested not in matched_collectors:
                raise Exception(f'Collector not found when trying to skip other: {requested}')

    def __populate_collectors(self):
        collector_classes = [cls for cls in globals() if 'Collector' in cls]
        for collector in collector_classes:
            inst = globals()[collector]()
            self.context.collectors.append(inst)

    def __setup_clients(self):
        self.context.clients["pbi"] = PbiClient(self.context)
        self.context.clients["graph"] = GraphClient(self.context)
        self.context.clients["fabric"] = FabricClient(self.context)
    
    def __populate_monitoring_workspace_ids(self):
        workspaces = self.context.clients['pbi'].get("v1.0/myorg/admin/groups?$top=1&$filter=type eq 'AdminWorkspace'")
        if workspaces is not None:
            if not hasattr(workspaces, 'error'):
                if len(workspaces['value']) > 0:
                    admin_workspace = workspaces['value'][0]
                    admin_workspaceId = admin_workspace['id']

                    models = self.context.clients['pbi'].get(f'v1.0/myorg/groups/{admin_workspaceId}/datasets')
                    if models is not None:
                        if not hasattr(models, 'error'):
                            for model in models['value']:
                                if model['name'] == 'Purview Hub':
                                    self.context.purview_model_id = model['id']
                                if model['name'] == 'Feature Usage and Adoption':
                                    self.context.inventory_model_id = model['id']
