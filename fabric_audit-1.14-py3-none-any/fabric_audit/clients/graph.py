from .base import BaseClient

class GraphClient(BaseClient):
    def __init__(self, context):
        super().__init__(context)
        match context.environment:
            case 'USGov':
                self.scope = 'https://graph.microsoft.com/.default'
            case 'USGovMil':
                self.scope = 'https://dod-graph.microsoft.us/.default'
            case 'USGovHigh':
                self.scope = 'https://graph.microsoft.us/.default'
            case _:
                self.scope = 'https://graph.microsoft.com/.default'
        self.token_key = 'pbi'
    
    def get_api_root(self) -> str:
        match self.context.environment:
            case "USGov":
                return 'https://graph.microsoft.com/'
            case 'USGovMil':
                return 'https://dod-graph.microsoft.us/'
            case "USGovHigh":
                return 'https://graph.microsoft.us/'
            case _:
                return 'https://graph.microsoft.com/'