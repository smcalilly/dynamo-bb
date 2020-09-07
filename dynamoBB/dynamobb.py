""" dynamobb = some baby classes to interface with DynamoDB """
import boto3

class DynamoClient:
    """
        A wrapper class for interacting with DynamoDB via boto3.

        __init__: establishes the Dynamo client with the boto3 library

        A client has:
            - table_name = a DynamoDB table name. required.
            - kwargs = **kwargs that are passed to the boto3 client. optional
    """

    def __init__(self, table):
        self.table = self._init_table(table)
        self.kwargs = table.get('kwargs', {})

    def _init_table(self, table):
        try:
            table_name = table.get('table_name')
            return boto3.resource('dynamodb').Table(table_name)
        except ValueError as error:
            return error

    def scan(self, **kwargs):
        records = []

        response = self.table.scan(**self.kwargs)

        for row in response['Items']:
            records.append(row)

        while 'LastEvaluatedKey' in response:
            response = self.table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey'],
                **self.kwargs
            )

            for row in response['Items']:
                records.append(row)

        return records

    def update_item(self, **kwargs):
        return self.table.update_item(**kwargs)

    def get_table_metadata(self):
        return {
            'table_name': self.table.table_name,
            'primary_key': self.table.key_schema[0],
            'item_count': self.table.item_count,
            'attributes': self.table.attribute_definitions,
            'global_secondary_indexes': self.table.global_secondary_indexes,
            'local_secondary_indexes': self.table.local_secondary_indexes,
            'table_arn': self.table.table_arn,
            'table_size_bytes': self.table.table_size_bytes
        }

    def get_item(self, **kwargs):
        response = self.table.get_item(**kwargs, **self.kwargs)
        return response['Item']


class DynamoTable(DynamoClient):
    """
    A DynamoDB cache and interface.

    __init__: creates a Dynamo table cache by scanning a table and returning a list of items from the table.

    attributes:
        - client = a DynamoDB resource with a boto3 interface
        - items = cache for the table items. all changes go through this.
    """

    def __init__(self, table):
        super().__init__(table)
        self.items = self.__init_items()

    def __init_items(self):
        return self.scan()


class DynamoMap:
    """
    A map of DynamoTable instances.

    attributes:
        tables = a list of DynamoTable instances
    """
    def __init__(self, tables):
        self.tables = self.__set_tables(tables)

    def __set_tables(self, tables):
        client_tables = {}

        for table in tables:
            client_table = DynamoTable(tables[table])

            client_tables.update({
                table: client_table
            })

        return client_tables


    def join(self, a_table, where={}):
        """Returns a list of items where there is an association between two tables."""
        b_table_attr = next(iter(where.keys()))
        b_table_id = next(iter(where.values()))

        # need to implement a faster way of doing this
        results = [d for d in a_table.items if d.get(b_table_attr, '') == b_table_id]

        return results
