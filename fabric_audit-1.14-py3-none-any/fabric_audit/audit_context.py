from typing import List
from .sinks.file import FileSink
from .sinks.delta import DeltaSink
import datetime
import os
import logging

class AuditContext:
    def __init__(self):
        self.collectors = []
        self.clients = {}
        self.runId =  datetime.datetime.now().strftime("%Y%m%d.%H%M%S")
        self.log_level = logging.ERROR
        self.capacity_metrics_dataset_id = None
        self.purview_model_id = None
        self.inventory_model_id = None
        self.sink = None
        self.logger = None
        self.authentication = 'Interactive'
        self.credentials = None
        self.flags = []
        self.environment = None
        self.authority = None
        self.troubleshooting_batch_size = 0
        self.troubleshooting_delay_s = 0

        self.sp_tenant_id = None
        self.sp_client_id = None
        self.sp_client_secret = None

    def set_sink(self, sink: str):
        safe_sink = sink.replace('\\', '/')
        sinks = [ 
            FileSink(self.credentials, self.runId, self.log_level), 
            DeltaSink(self.credentials, self.runId, self.log_level)
        ]
        for sink_instance in sinks:
            if sink_instance.is_valid_sink(safe_sink):
                self.sink = sink_instance
                self.logger = sink_instance
                break
        if self.sink is not None:
            self.sink.set_connection(safe_sink)
        else:
            raise Exception(f'No sink implementation for {safe_sink}') 
    
    def set_capacity_metrics_dataset(self, dataset_id: str):
        self.capacity_metrics_dataset_id = dataset_id

    def set_authentication(self, auth: str):
        supported = ('ServicePrincipal','ManagedIdentity','Interactive','FabricIdentity')
        if auth in supported:
            self.authentication = auth
        else:
            raise Exception(f'Authentication method not supported ({", ".join(supported)}): {auth}')

    def supported_flags(self):
        return ('SkipPersonalWorkspaces', 'DetailedLog', 'ActivityDays*')

    def set_flags(self, flags: List[str]):
        supported = [f.lower() for f in self.supported_flags()]
        for flag in flags: 
            safe_flag = flag.lower().strip()  
            if safe_flag in supported and safe_flag not in self.flags:
                self.flags.append(safe_flag)
            else:
                if safe_flag.startswith('activitydays'):
                    self.flags.append(safe_flag)
                else:
                    raise Exception(f'Flag not supported ({", ".join(self.supported_flags())}): {flag}')
            
        if 'DetailedLog' in self.flags:
            self.log_level = logging.DEBUG
            if self.logger is not None:
                self.logger.setLevel(self.log_level)

    def emit(self):
        self.logger.emit(f'Environment: {self.environment}', no_print=True)
        self.logger.emit(f'Flags: {",".join(self.flags)}', no_print=True)
        self.logger.emit(f'Auth: {self.authentication}', no_print=True)

    def set_service_principal(self, tenant_id, client_id, client_secret):
        self.sp_tenant_id = tenant_id
        self.sp_client_id = client_id
        self.sp_client_secret = client_secret
        os.environ['AZURE_TENANT_ID'] = tenant_id
        os.environ['AZURE_CLIENT_ID'] = client_id
        os.environ['AZURE_CLIENT_SECRET'] = client_secret
        self.allow_interactive_credentials = False