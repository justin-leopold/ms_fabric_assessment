from .batch_result import BatchResult, CollectorCollection
from .query_base import QueryBase

class CapacityQueryBase(QueryBase):

    def __init__(self):
        super().__init__()
        self.name = "Capacity Query Base"
        self.batching_query = ''
        self.query_template = ''
        self.batch_list = []

    def is_valid(self, context):
        return context.capacity_metrics_dataset_id is not None

    def required_information(self):
        return "Fabric Capacity Metrics semantic model ID"

    def collect(self, context, next_batch_id: str):
        self.semantic_model_id = context.capacity_metrics_dataset_id

        batch_index = 0
        if next_batch_id is None:
            self.__populate_batch_list(context)
        else:
            batch_index = next_batch_id

        result = BatchResult()
        if len(self.batch_list) > 0:
            capacity_id = self.batch_list[batch_index]['capacity']
            keys = self.batch_list[batch_index]['keys']
            context.logger.emit(f'Reading capacity {capacity_id} metrics set containing {len(keys)} keys')

            keys_text = '"' + '","'.join(keys) + '"'
            data = self.query_model(f'''DEFINE MPARAMETER CapacityID = "{capacity_id}"
                VAR __CapacityFilterTable = TREATAS({{"{capacity_id}"}}, 'Capacities'[capacityId])
                ''' + self.query_template.format(keys_text = keys_text), context)


            result.append(self.map_data(data))

            if batch_index < len(self.batch_list) - 1:
                result.next_batch_id = batch_index + 1
                result.batch_progress = batch_index * 1.0 / len(self.batch_list)

            return result
        else:
            return None


    def __populate_batch_list(self, context):
        capacities = self.query_model('EVALUATE SELECTCOLUMNS(Capacities, Capacities[capacityId])', context)

        if capacities is not None:
            for capacity in capacities:
                current_capacity = capacity.get('Capacities[capacityId]')

                set_stats = self.query_model(f'''DEFINE MPARAMETER CapacityID = "{current_capacity}"
                VAR __CapacityFilterTable = TREATAS({{"{current_capacity}"}}, 'Capacities'[capacityId])
                {self.batching_query}''', context)

                if set_stats is not None:
                    start_index = 0
                    continue_paging = True
                    while continue_paging:
                        running_total = 0
                        keys = []
                        while True:
                            if start_index >= len(set_stats):
                                continue_paging = False
                                break

                            running_total += set_stats[start_index].get('[SetSize]')
                            key = set_stats[start_index].get('[SetKey]')
                            keys.append(self.format_key(key))
                            start_index += 1
                            if running_total > 100000:
                                break

                        if len(keys) <= 0:
                            break

                        self.batch_list.append(dict(capacity=current_capacity, keys=keys))

    def format_key(self, key) -> str:
        raise Exception(f'Key formatting not implemented for collector {self.name}')

    def map_data(self, metrics) -> CollectorCollection:
        raise Exception(f'Data mapping not implemented for collector {self.name}')