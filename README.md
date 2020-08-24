# DynamoBB
DynamoBB is a *baby* (aka bb) package for interfacing with DynamoDB. It wraps Boto3. This is an experimental package, so use in production at your own risk.

## Why would I want to wrap Boto3?
Boto3 is a self-described low-level package meant for using AWS resources, so it's easy to encapsulate some of the details that might lead to messy code.

More importantly, you might sometimes work with Dynamo tables that are designed like a relational database. In that case, DynamoBB provides an interface to join two tables together.


## How does it work?
DynamoBB creates a cache after a full table scan. This allows you to work with an entire table in memory. This is useful when you're doing stuff like writing a CSV and need the table to reference. 

### Install
```
pip install git+https://git@github.com/smcalilly/dynamoBB.git
```


## Usage
To setup the in-memory cache, you need to initialize the DynamoBB class with a Dynamo table client. 
```
# setup the clients 
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

# initialize the cache
DYNAMO = dynamobb.DynamoMap(dynamo_clients)

# establish the individual table classes
customers = DYNAMO.tables['customers']
locations = DYNAMO.tables['locations']

# join a customer and location table
customer_locations = DYNAMO.join(locations, where={'customerId': customers['customerId']})
```

## Don't want a cache?
Since the above example creates a cache, you will probably run into issues if you're doing write operations or using this in a Lambda that doesn't usually start cold. In that case, just use the basic wrapper classes like this:

### Get an item from a table
```
client = dynamobb.DynamoClient(table='customers', 'AttributesToGet': ['customerId', 'name'])
customer = client.get_item(Key={'customerId': customer_id})
```

### Basic Boto3 method
This method directly scans DynamoDB and has no cache.
```
client.scan(table) 
```
This is a baby library and wraps Boto3 instead of inheriting from (as I write this, now I think I should change that !). Because of this, the library doesn't include all of the Boto3 methods for Dynamo. That's no problem, because thanks to Python, you can also use the Boto3 instance like this:
```
client.table.update_item(item)
```
