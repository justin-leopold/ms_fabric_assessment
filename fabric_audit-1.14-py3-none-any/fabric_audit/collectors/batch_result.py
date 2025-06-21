class CollectorCollection:
    def __init__(self, name: str):
        self.name = name
        self.partition = None
        self.fields = []
        self.data = []

    def append(self, row: dict):
        for key in row.keys():
            if key not in self.fields:
                self.fields.append(key)
        self.data.append(row)

class BatchResult:
    def __init__(self):
        self.collections = {}
        self.next_batch_id = None
        self.batch_progress = None
        self.batch_friendly_name = None

    def append(self, collection: CollectorCollection):
        self.collections[collection.name] = collection
    