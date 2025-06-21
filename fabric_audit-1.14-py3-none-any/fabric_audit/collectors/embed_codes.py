from .batch_result import BatchResult, CollectorCollection

class EmbedCodesCollector:
    def __init__(self):
        self.name = "Embed Codes"
        self.active = True

    def collect(self, context, next_batch_id: str):
        tokens_response = context.clients['pbi'].get('v1.0/myorg/admin/widelySharedArtifacts/publishedToWeb', additional_headers={"Content-Type": "application/json"})
        if tokens_response is not None:
            if not hasattr(tokens_response, 'error'):
                tokens = tokens_response.get('ArtifactAccessEntities')
                ct = tokens_response.get('continuationToken')
                while ct is not None:
                    tokens_uri = tokens_response.get('continuationUri')
                    tokens_response = context.clients['pbi'].get(tokens_uri, additional_headers={"Content-Type": "application/json"})
                    if not hasattr(tokens_response, 'error'):
                        tokens.extend(tokens_response.get('ArtifactAccessEntities'))
                        ct = tokens_response.get('continuationToken')
                    else: 
                        return None

                result = BatchResult()
                result.append(self.__map_embed_codes(tokens))
            else:
                return None

        return result
    

    def __map_embed_codes(self, items):
        result = CollectorCollection("EmbedCodes")

        for item in items:
            result.append({
                'ArtifactId': item.get('artifactId'),
                'ArtifactType': item.get('artifactType'),
                'ArtifactName': item.get('artifactName'),
                'UserDisplayName': item.get('sharer', {}).get('displayName'),
                'UserEmailAddress': item.get('sharer', {}).get('emailAddress'),
                'UserIdentifier': item.get('sharer', {}).get('identifier'),
                'UserGraphId': item.get('sharer', {}).get('graphId'),
                'UserPrincipalType': item.get('sharer', {}).get('principalType'),
                })
            
        return result