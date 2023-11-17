# BAAS utils

## Installation

lastest version: 0.0.2

```shell
pip install baas-utils @ git+ssh://git@gitlab.com/wowx-baas/baas-utils@<version>
```

## Usage

## Security

### AbstractToken

The AbstractToken class is an abstract base class that can be subclassed to create specific token objects. It provides the basic structure and attributes for token objects. Here's an example of how to use it:

```python
from jwt_token_factory import AbstractToken

# Create a subclass of AbstractToken
class MyToken(AbstractToken):
    pass

# Create an instance of the token
token = MyToken(data={'key1': 'value1', 'key2': 'value2'}, token='example_token')

# Access the token string and data
print(token.token)  # 'example_token'
print(token.data)   # {'key1': 'value1', 'key2': 'value2'}
```

### AbstractTokenFactory

The AbstractTokenFactory class is an abstract base class for token factories. It provides the common interface and functionality for encoding and decoding tokens. Subclasses must implement the _encode and_decode methods according to their specific token encoding and decoding logic. Here's an example of how to use it:

```python
from utils.security.credential_token import AbstractTokenFactory

# Create a subclass of AbstractTokenFactory
class MyTokenFactory(AbstractTokenFactory):
    def _encode(self, data: str, *args, **kwargs) -> MyToken:
        # Custom encoding logic
        token = encode_data_into_token(data)
        return MyToken(data=data, token=token)

    def _decode(self, token: MyToken | str, *args, **kwargs) -> dict[str, any]:
        # Custom decoding logic
        decoded_data = decode_token_data(token)
        return decoded_data

# Create an instance of the token factory using environment variables
factory = MyTokenFactory(from_env=True)

# Encode data into a token
data = 'example_data'
token = factory.encode(data)
# token is an instance of MyToken

# Decode the token and retrieve the data
decoded_data = factory.decode(token)
print(decoded_data)  # 'example_data'
```

### JwtToken and JwtTokenFactory

> The JWT Token Factory is a Python package that provides functionality for encoding and decoding JSON Web Tokens (JWTs). JWTs are commonly used for authentication and authorization purposes in web applications. This package includes an abstract base class for token objects and an abstract base class for token factories, along with a concrete implementation for JWT tokens.

The JwtToken and JwtTokenFactory classes are concrete implementations of the abstract classes AbstractToken and AbstractTokenFactory, respectively. They provide functionality specific to JSON Web Tokens (JWTs). Here's an example of how to use them:

```python
from utils.security.credential_token import JwtToken, JwtTokenFactory

# Create an instance of the JWT token factory
factory = JwtTokenFactory(secret='my_secret', algorithm='HS256') 
# Load from env with keys (JWT_SECRET, JWT_ALGORITHM)
# factory = JwtTokenFactory(from_env=True)

# Encode data into a JWT token
data = {'user_id': 123}
token = factory.encode(data)

# Decode the JWT token and retrieve the data
decoded_data = factory.decode(token)
print(decoded_data)  # {'user_id': 123}
```

## Values

### is_sub_dict

The is_sub_dict function takes two dictionaries, dict_a and dict_b, and an optional set of attributes to ignore during the comparison (ignore_attrs). It compares the key-value pairs in dict_b against dict_a to determine if dict_b is a sub-dictionary of dict_a.

The function returns a tuple containing a boolean value indicating whether dict_b is a sub-dictionary of dict_a, and a string indicating the first attribute that is not present in dict_a or has a different value.

Here are some examples demonstrating the usage of the is_sub_dict function:

```python

from utils.values import compare

dict_a = {'name': 'John', 'age': 30, 'city': 'New York'}
dict_b = {'name': 'John', 'age': 30}
result, key = compare.is_sub_dict(dict_a, dict_b)
print(result)
print(key)
# Output: 
# True 
# None

dict_c = {'name': 'John', 'age': 30, 'city': 'Los Angeles'}
dict_d = {'name': 'John', 'age': 30, 'city': 'New York'}
result, key = compare.is_sub_dict(dict_c, dict_d)
print(result)
print(key)
# Output:
# False 
# city

dict_e = {'name': 'John', 'age': 30, 'city': 'New York'}
dict_f = {'name': 'John', 'age': 30, 'country': 'USA'}
result, key = compare.is_sub_dict(dict_e, dict_f)
print(result)
print(key)
# Output: 
# False
# country
```

### prettier_dict

The prettier_dict function returns a pretty-printed string representation of a nested dictionary. It indents nested elements and sorts keys.

Call the prettier_dict function and pass the dictionary you want to pretty-print as the d argument:

```python
from utils.values import parsers

my_dictionary = {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}
result = parsers.prettier_dict(my_dictionary)
print(result)
# Output
# {
#     "a": 1,
#     "b": {
#         "c": 2,
#         "d": {
#             "e": 3
#         }
#     }
# }
```

This will output the pretty-printed string representation of the dictionary.

### jsonify_datetime

The jsonify_datetime function converts a datetime object to a string representation in JSON format.

```python
my_datetime = datetime(2023, 8, 10, 10, 30, 0)
result = jsonify_datetime(my_datetime)
print(result)
```

This will output the string representation of the `datetime` object in JSON format.

### jsonify_enum

The jsonify_enum function converts an enumeration value to its string representation.

To use this function, follow these steps:

1. Define your enumeration class and values:

```python
class MyEnum(Enum):
    VALUE1 = "First Value"
    VALUE2 = "Second Value"
```

2. Call the jsonify_enum function and pass the enumeration value you want to convert as the src_enum argument:

```python
my_enum_value = MyEnum.VALUE1
result = jsonify_enum(my_enum_value)
print(result)
# Output (First Value)
```

This will output the string representation of the enumeration value.

### jsonify_dict

The jsonify_dict function converts a dictionary to a JSON-like dictionary representation. It supports conversion of datetimes and enumeration values to their string representations.

To use this function, follow these steps:

1. Define your dictionary:

```python
my_dict = {
    "key1": 123,
    "key2": datetime(2023, 8, 10, 10, 30, 0),
    "key3": MyEnum.VALUE1
}
```

2. Call the jsonify_dict function and pass the dictionary you want to convert as the src_dict argument:

```python
result = jsonify_dict(my_dict)
print(result)
# Output ({'key1': 123, 'key2': '2023-08-10 10:30:00.000000', 'key3': 'First Value'})
```

This will output the converted dictionary with datetimes and enumeration values converted to their string representations.

## Test

### REST

#### Response to Dictionary Converter

The response_to_dict function is a utility function that converts JSON-encoded response content into a dictionary. It is useful when working with HTTP APIs that return JSON responses. This function takes the response content as input and returns the corresponding dictionary representation.

Here's an example of how to use the response_to_dict function:

```python
from utils.test import rest 

response_content = '{"key": "value"}'
response_dict = rest.response_to_dict(response_content)
print(response_dict)  # {'key': 'value'}
```

#### Database

The SqlDatabase class is a Python class that represents a SQL database. It provides methods for retrieving models from a specified table, removing models by their ID, and clearing the cached models. The class utilizes the SQLAlchemy library for interacting with the database.

##### Required environment variables

- DATABASE_URI

##### Example

```python
# Create an instance of SqlDatabase using an engine
engine = sqlalchemy.create_engine('sqlite:///mydatabase.db')
database = SqlDatabase(engine=engine)

# Retrieve a model from a table
model = database.get('my_table', 'my_id')

# Remove a model from a table
database.remove('my_table', 'my_id')

# Clear the cached models
database.clear()
```

### Fixtures

Just import these fixtures

#### sql_database_uri

The sql_database_uri fixture provides the SQL database URI to your tests. It retrieves the URI from the environment variable "DATABASE_URI". To use this fixture, follow these steps:

Decorate your test function with the sql_database_uri fixture:

```python
def test_something(sql_database_uri):
    # Use the SQL database URI within the test
    ...
```

In this example, the `sql_database_uri` fixture is included as an argument in the test function.

#### sql_database

The sql_database fixture creates a SqlDatabase object using the SQL database URI provided by the sql_database_uri fixture. To use this fixture, follow these steps:

Decorate your test function with the sql_database fixture:

```python
def test_something(sql_database):
    # Use the SQL database object within the test
    ...
```

In this example, the `sql_database` fixture is included as an argument in the test function.

#### clear_log

The clear_log fixture clears the contents of a log file. It retrieves the project path from the environment variable "PROJECT_PATH" and creates a log file path using the project path. The fixture then opens the log file in write mode, effectively clearing its contents.

Decorate your test function with the clear_log fixture:

```python
def test_something(clear_log):
    # Clear the log file before running the test
    ...
```

In this example, the `clear_log` fixture is included as an argument in the test function.

### Log

You can then create an instance of the LoggingDefault class and use its methods to log messages:

```python
logger = LoggingDefault()

logger.debug("Debug message")
# Debug message
logger.debug({"name":"Example"})
# {
#      "name":"Example"
# }

logger.info("Info message")
```
