# DynamoBB
DynamoBB is a baby package for interfacing with DynamoDB. It wraps Boto3. This is an experimental package, so use in production at your own risk.

## Why would I want to wrap Boto3?
Boto3 is a self-described low-level package meant for using AWS resources, so it's easy to encapsulate some of the details that might lead to messy code.

More importantly, you might sometimes work with Dynamo tables that are unfortunately designed more like a relational database than NoSQL. In that case, DynamoBB provides an interface to join two tables together.


## How does it work?
DynamoBB can create a cache after a full table scan, for when you need to work with an entire table in memory. This is useful when you're doing stuff like writing a CSV. To do this, you need to initialize the DynamoBB class with a Dynamo table client. 

### Install
```
pip install git+https://git@github.com/smcalilly/dynamo-bb.git
```

### Setup the clients:
```
dynamo_clients = {
    'customers': {
        'table_name': 'customers',
        'kwargs': {
            'AttributesToGet': ['customerId', 'name']
        }
    },
    'locations': {
        'table_name': 'locations',
        'kwargs': {
            'AttributesToGet': ['locationId', 'locationName', 'customerId']
        }
    }
}
```

### Initalize the cache
```
DYNAMO = dynamobb.DynamoMap(DYNAMO_CLIENTS)
```

### establish the individual tables
```
CUSTOMERS = DYNAMO.tables['customers']
LOCATIONS = DYNAMO.tables['locations']
```

### Join a customer and location table
```
customer_locations = DYNAMO.join(LOCATIONS, where={'customerId': customer['customerId']})
```


## Don't want a cache?
You will probably run into issues if you're doing write operations or using this in a Lambda that doesn't usually start cold. In that case, just use the basic wrapper classes like this:

### Get an item from a table
```
client = dynamobb.DynamoClient(table='customers', 'AttributesToGet': ['customerId', 'name'])
customer = client.get_item(Key={'customerId': customer_id})
```

Since it's essentially a wrapper class for Boto3, you can do any normal operation you would do with Boto3.
### Basic Boto3 method
This method directly scans DynamoDB and has no cache.
```
client.scan(table) 
```