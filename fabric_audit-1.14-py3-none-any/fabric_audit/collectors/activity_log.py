import datetime
from .batch_result import BatchResult, CollectorCollection

class ActivityLogCollector:
    def __init__(self):
        self.name = "Activity Log"
        self.activity_log_days = 8
        self.end_date = datetime.date.today()
        self.start_date = datetime.date.today()
        self.batch_hours = 24
        self.active = True
    
    def collect(self, context, next_batch_id: str):

        if next_batch_id is None:
            for activity_flag in [flag for flag in context.flags if flag.startswith('activitydays')]:
                days = int(activity_flag.replace("activitydays", ""))
                if days > 0 and days <= 30:
                    self.activity_log_days = days
                    context.logger.emit(f'Activity Log export set to {days} days.')

            self.start_date = datetime.date.today() - datetime.timedelta(days=self.activity_log_days - 1)

            range_from = datetime.datetime(year=self.start_date.year, month=self.start_date.month, day=self.start_date.day)
        else:  
            range_from = datetime.datetime.strptime(next_batch_id, '%Y-%m-%d-%H')

        range_to = range_from + datetime.timedelta(hours=self.batch_hours)
        range_to_exclusive = range_to - datetime.timedelta(seconds=1)
        datetime_format = '%Y-%m-%dT%H:%M:%SZ'
        activity_uri = f'v1.0/myorg/admin/activityevents?startDateTime=%27{range_from.strftime(datetime_format)}%27&endDateTime=%27{range_to_exclusive.strftime(datetime_format)}%27'
        activities_response = context.clients['pbi'].get(activity_uri, additional_headers={"Content-Type": "application/json"})
        if activities_response is not None:
            if not hasattr(activities_response, 'error'):
                activities = activities_response.get('activityEventEntities')
                ct = activities_response.get('continuationToken')
                while ct is not None:
                    activity_uri = activities_response.get('continuationUri')
                    activities_response = context.clients['pbi'].get(activity_uri, additional_headers={"Content-Type": "application/json"})
                    if not hasattr(activities_response, 'error'):
                        activities.extend(activities_response.get('activityEventEntities'))
                        ct = activities_response.get('continuationToken')
                    else: 
                        return None
                    
                result = BatchResult()
                result.append(self.__map_activities(range_from, activities))
            else:
                return None
            
        result.batch_friendly_name = range_from.strftime('%Y-%m-%d-%H')
        batch_start_days = (range_to - datetime.datetime.combine(self.start_date, datetime.time(0,0,0))).days
        result.batch_progress = batch_start_days / self.activity_log_days

        if range_to <= datetime.datetime(self.end_date.year, self.end_date.month, self.end_date.day, 23, 59, 59):
            result.next_batch_id = range_to.strftime('%Y-%m-%d-%H')
        else: 
            result.next_batch_id = None
            

        return result
    
    def __map_activities(self, range_datetime: datetime, activities):
        range_id = range_datetime.date().strftime('%Y%m%d%H')
        result = CollectorCollection(f'ActivityLog')
        result.partition = range_id
        for event in activities:
            result.append({
                'Id': event.get('Id'),				
                'RecordType': event.get('RecordType'),		 
                'CreationTime': event.get('CreationTime'),      
                'Operation': event.get('Operation'),    
                'OrganizationId': event.get('OrganizationId'),    
                'UserType': event.get('UserType'),  
                'UserKey': event.get('UserKey'),        
                'Workload' :event.get('Workload'),         
                'UserId': event.get('UserId'),        
                'ClientIP': event.get('ClientIP'),          
                'UserAgent': event.get('UserAgent'),        
                'Activity': event.get('Activity'),       
                'ItemName': event.get('ItemName'),        
                'WorkSpaceName': event.get('WorkSpaceName'),     
                'DatasetName': event.get('DatasetName'),       
                'ReportName': event.get('ReportName'),        
                'CapacityId': event.get('CapacityId'),        
                'CapacityName': event.get('CapacityName'),      
                'WorkspaceId': event.get('WorkspaceId'),       
                'AppName': event.get('AppName'),           
                'ObjectId': event.get('ObjectId'),      
                'ObjectType': event.get('ObjectType'),     
                'DatasetId': event.get('DatasetId'),         
                'ReportId': event.get('ReportId'),          
                'IsSuccess': event.get('IsSuccess'),         
                'ReportType': event.get('ReportType'),        
                'RequestId': event.get('RequestId'),         
                'ActivityId': event.get('ActivityId'),        
                'AppReportId': event.get('AppReportId'),       
                'DistributionMethod': event.get('DistributionMethod'),
                'ConsumptionMethod': event.get('ConsumptionMethod'), 
                'TableName': event.get('TableName'),
                'DashboardName': event.get('DashboardName'),
                'DashboardId': event.get('DashboardId'), 
                'Datasets': event.get('Datasets'),
                'DataflowId': event.get('DataflowId'),
                'DataflowType': event.get('DataflowType'),
                'EmbedTokenId': event.get('EmbedTokenId'),
                'CustomVisualAccessTokenResourceId': event.get('CustomVisualAccessTokenResourceId'),
                'CustomVisualAccessTokenSiteUri': event.get('CustomVisualAccessTokenSiteUri'),
                'DataConnectivityMode': event.get('DataConnectivityMode')
                })
            
        return result