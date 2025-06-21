from .batch_result import BatchResult
from .inventory_scanners import *
import time

class InventoryCollector:
    def __init__(self):
        self.maxBatchSize = 100
        self.name = "Inventory"
        self.batch_list = []
        self.active = True

    def collect(self, context, next_batch_id: str):

        if len(self.batch_list) == 0:
            self.__populate_batch_list(context)

        batch_index = 0
        if next_batch_id is not None: 
            batch_index = next_batch_id
        
        result = BatchResult()
        if len(self.batch_list) > 0:
            if context.troubleshooting_delay_s > 0:
                context.logger.emit(f'Troubleshootig delay injected: {context.troubleshooting_delay_s}s. Should never happen during delivery.')
                time.sleep(context.troubleshooting_delay_s)
                
            workspaceList = '","'.join(self.batch_list[batch_index])
            batchBody = f'{{"workspaces":["{workspaceList}"]}}'
            scanUrl = 'v1.0/myorg/admin/workspaces/getInfo?lineage=True&datasourceDetails=True&datasetSchema=True&datasetExpressions=True&getArtifactUsers=true'
            scanInfo = context.clients['pbi'].post(scanUrl, data=batchBody, additional_headers={"Content-Type": "application/json"})
            if not hasattr(scanInfo, 'error'):
                while True:
                    scanStatus = context.clients['pbi'].get('v1.0/myorg/admin/workspaces/scanStatus/' + scanInfo["id"])
                    if scanStatus['status'] == 'Succeeded':
                        break

                scanResult = context.clients['pbi'].get('v1.0/myorg/admin/workspaces/scanResult/' + scanInfo["id"])

                scanner_classes = [cls for cls in globals() if 'Scanner' in cls]
                for scanner in scanner_classes:
                    inst = globals()[scanner]()
                    result.append(inst.map(scanResult))

                if batch_index < len(self.batch_list) - 1:
                    result.next_batch_id = batch_index + 1
                    
                result.batch_progress = batch_index * 1.0 / len(self.batch_list)

                return result
    
    def __populate_batch_list(self, context):
        ws_list_uri = 'v1.0/myorg/admin/workspaces/modified'
        if 'skippersonalworkspaces' in context.flags:
            ws_list_uri = ws_list_uri + '?excludePersonalWorkspaces=True'
        workspaces = context.clients['pbi'].get(ws_list_uri)
        batchSize = self.maxBatchSize
        if context.troubleshooting_batch_size > 0:
            batchSize = context.troubleshooting_batch_size
        if not hasattr(workspaces, 'error'):
            current_batch = []
            for ws in workspaces:
                current_batch.append(ws['id'])
                if len(current_batch) == batchSize:
                    self.batch_list.append(current_batch)
                    current_batch = []

            if len(current_batch) > 0:
                self.batch_list.append(current_batch)
            