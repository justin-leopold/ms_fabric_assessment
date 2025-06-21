from .base import BaseClient

class FabricClient(BaseClient):
    def __init__(self, context):
        super().__init__(context)
        match context.environment:
            case 'USGov':
                self.scope = 'https://analysis.usgovcloudapi.net/powerbi/api/.default'
            case 'USGovMil':
                self.scope = 'https://mil.analysis.usgovcloudapi.net/powerbi/api/.default'
            case 'USGovHigh':
                self.scope = 'https://high.analysis.usgovcloudapi.net/powerbi/api/.default'
            case _:
                self.scope = 'https://analysis.windows.net/powerbi/api/.default'   
        self.token_key = 'pbi'

    def get_api_root(self) -> str:
        return 'https://api.fabric.microsoft.com/'