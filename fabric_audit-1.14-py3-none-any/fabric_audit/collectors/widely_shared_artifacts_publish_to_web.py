from .batch_result import BatchResult, CollectorCollection

class WidelySharedArtifactsPublishToWebCollector:
    def __init__(self):
        self.name = "WidelySharedArtifactsPublishToWeb"
        self.active = True

    def collect(self, context, next_batch_id: str):

        widely_shared_artifacts_publish_to_web = context.clients['pbi'].get('v1.0/myorg/admin/widelySharedArtifacts/publishedToWeb', additional_headers={"Content-Type": "application/json"})
        result = BatchResult()
        if widely_shared_artifacts_publish_to_web is not None:
            if not hasattr(widely_shared_artifacts_publish_to_web, 'error'):
                result.append(self.__map_widely_shared_artifacts_publish_to_web(widely_shared_artifacts_publish_to_web))
            else:
                return None

        return result
    

    def __map_widely_shared_artifacts_publish_to_web(self, widely_shared_artifacts_publish_to_web):
        result = CollectorCollection("WidelySharedArtifactsPublishToWeb")

        for item in widely_shared_artifacts_publish_to_web['ArtifactAccessEntities']:
            result.append({
                'ArtifactId': item.get('artifactId'),
                'DisplayName': item.get('displayName'),
                'ArtifactType': item.get('artifactType'),
                'AccessRight': item.get('accessRight'),
                'ShareType': item.get('shareType'),
                'SharerDisplayName': item.get('sharer').get('displayName'),
                'SharerEmailAdress': item.get('sharer').get('emailAddress'),
                'SharerIdentifier': item.get('sharer').get('identifier'),
                'SharerGraphId': item.get('sharer').get('graphId'),
                'SharerPrincipalType': item.get('sharer').get('principalType'),
                })
            
        return result