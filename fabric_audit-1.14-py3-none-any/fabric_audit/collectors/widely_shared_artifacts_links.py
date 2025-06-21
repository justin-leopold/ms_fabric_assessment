from .batch_result import BatchResult, CollectorCollection

class WidelySharedArtifactsLinksCollector:
    def __init__(self):
        self.name = "WidelySharedArtifactsLinks"
        self.active = True

    def collect(self, context, next_batch_id: str):

        widely_shared_artifacts_links = context.clients['pbi'].get('v1.0/myorg/admin/widelySharedArtifacts/linksSharedToWholeOrganization', additional_headers={"Content-Type": "application/json"})
        result = BatchResult()
        if widely_shared_artifacts_links is not None:
            if not hasattr(widely_shared_artifacts_links, 'error'):
                if 'ArtifactAccessEntities' in widely_shared_artifacts_links:
                    result.append(self.__map_widely_shared_artifacts_links(widely_shared_artifacts_links))
                else:
                    print("Key 'ArtifactAccessEntities' not found in the response.")

                    return None
            else:
                return None
        return result
    

    def __map_widely_shared_artifacts_links(self, widely_shared_artifacts_links):
        result = CollectorCollection("WidelySharedArtifactsLinks")

        for item in widely_shared_artifacts_links['ArtifactAccessEntities']:
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
                'SharerPrincipalType': item.get('sharer').get('principalType')
                })
            
        return result