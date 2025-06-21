from azure.identity import DefaultAzureCredential
from ..audit_context import AuditContext
import requests
import urllib.parse
import time
import logging

class BaseClient:
    def __init__(self, context: AuditContext):
        self.retryCount = 3
        self.success_list = [200, 202]
        self.scope = None
        self.token_key = None
        self.context = context

        logger = logging.getLogger('azure.identity')
        logger.addHandler(context.logger)
        logger.setLevel(context.log_level)

        if self.context.credentials is None:
            self.context.credentials = DefaultAzureCredential(
                authority = self.context.authority,
                exclude_interactive_browser_credential = self.context.authentication != 'Interactive',
                exclude_managed_identity_credential = self.context.authentication != 'ManagedIdentity',
                exclude_environment_credential = self.context.authentication != 'ServicePrincipal',
                exclude_workload_identity_credential = True,
                exclude_developer_cli_credential = True,
                exclude_shared_token_cache_credential = True,
                exclude_cli_credential = True,
                exclude_powershell_credential = True
            )
            

    def __get_token(self):
        if self.context.authentication == 'FabricIdentity':
            from trident_token_library_wrapper import PyTridentTokenLibrary # type: ignore
            return PyTridentTokenLibrary.get_access_token(self.token_key)
        else:
            return self.context.credentials.get_token(self.scope).token
    
    def __get_headers(self, additional_headers: dict = None):
        headers = {
            "Authorization":"Bearer " + self.__get_token(),
            "Content-Type": "application/json"
            }
        if additional_headers is not None:
            headers = headers | additional_headers
        return headers
    
    def get(self, relative_uri: str, additional_headers: dict = None):
        result = None
        for attempt in range(1, self.retryCount + 1):
            if attempt > 1:
                self.context.logger.emit(f"Retrying attempt {attempt}.")
                time.sleep(attempt ** 2)
            uri = urllib.parse.urljoin(self.get_api_root(), relative_uri)
            try:
                response = requests.get(uri, headers=self.__get_headers(additional_headers))
                result = self.__process_response(response, uri, attempt)
            except:
                result = ClientError(f'Error connecting to {uri}.', True)
            
            if not isinstance(result, ClientError):
                return result
            if not result.retry:
                break
        
        if isinstance(result, ClientError):
            self.context.logger.error(result.error)

        return result
    
    def post(self, relative_uri: str, data, additional_headers: dict = None):
        result = None
        for attempt in range(1, self.retryCount + 1):
            if attempt > 1:
                self.context.logger.emit(f"Retrying attempt {attempt}.")
                time.sleep(attempt ** 2)
            uri = urllib.parse.urljoin(self.get_api_root(), relative_uri)
            try:
                response = requests.post(uri, headers=self.__get_headers(additional_headers), data=data)
                result = self.__process_response(response, uri, attempt)
            except:
                result = ClientError(f'Error connecting to {uri}.', True)

            if not isinstance(result, ClientError):
                return result
            if not result.retry:
                break
        
        if isinstance(result, ClientError):
            self.context.logger.error(result.error)

        return result

    def __process_response(self, response, uri: str, attempt: int):
            if response.status_code in self.success_list:
                return response.json()
            
            retry_can_help = False
            if response.status_code == 429:
                self.context.logger.emit(f"Rate limiting encountered during attempt {attempt}.")
                if response.headers.get('Retry-After', None) is None:
                    waitTime = attempt ** 3 * 5
                else:
                    waitTime = int(response.headers['Retry-After'])
                self.context.logger.emit(f"Retrying in {waitTime}s. This is expected behavior for larger tenants.")
                retry_can_help = True
                time.sleep(waitTime)
            
            if response.status_code == 403:
                return ClientError(f'No access to {uri}.')
            
            if response.status_code == 404:
                return ClientError(f'No object found at {uri}. Check access.')
            
            if response.status_code == 500:
                retry_can_help = True
            
            error = f"Client error: {response.status_code} {response.text}. {uri}"
            return ClientError(error, retry_can_help)
    
    def get_api_root(self) -> str:
        raise Exception('Override missing')
    

class ClientError:
    def __init__(self, error, retry = False):
        self.error = error
        self.retry = retry
