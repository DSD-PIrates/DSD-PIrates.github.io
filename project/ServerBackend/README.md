# General Data Storage Server

```
Version : 0.0.1
Author  : GGN_2015
```

A General Data Storage Server can establish a correspondence between names and values, allowing for modification and querying of a particular value. In our general data server, all data transmission uses the HTTP protocol, and data storage and forwarding use the JSON format. Data transmission of the general data server follows the following conventions. All configuration information should be recorded in `config.json`, and the program will read the values in `config.json` in real time during the running process.

## Data Writing

### Request

We categorize data into **single-value** data and **multi-value** data. Each data has a string as its name, and if a data's name starts with an asterisk, it is a multi-value data. When you want to write a single-value data to the server, you need to send an HTTP POST request to the server and include the following content in the attached text:

```json
{
    "type" : "write",
    "name": "name_of_the_single_value_data",
    "data" : THE_OBJECT_VALUE_TO_SAVE,
    "hash" : A_HASH_VALUE
}
```

If the server has already stored a single-value data with that name, this operation will overwrite the existing data. Otherwise, this operation will create a new data record. The `hash` attribute used here involves security protection, and we will introduce the meaning and calculation method of the `hash` attribute in later paragraphs.

Writing multi-value data is similar to single-value data, but repeatedly writing to a multi-value data will not overwrite the previous data values. Specifically, the storage module will maintain a data queue for each multi-value data record. Whenever we call the interface to write data, the storage module will insert a new data at the end of the data queue. When there are more than `MAX_VALUE_CNT` data in the data queue of a multi-value data, the queue will pop elements from the head until the data volume in the queue is less than or equal to `MAX_VALUE_CNT`. The default value of `MAX_VALUE_CNT` is $100$.

### Response

When we successfully write a data, the server will provide us with a JSON data as feedback:

```json
{
    "result": "write success"
}
```

If our write operation fails for some reason, the server will modify the  `result` field to indicate the reason for the data write failure. Common reasons for failure include: database access failure, too frequent interface calls, and incorrect verification codes (`hash`). For example, you may receive JSON data like this:

```json
{
	"result": "name field must be included"
}
```

This means that you either forgot to write the name field or the written name field is not a string.

## Data Reading

### Request

All data is stored and retrieved in plaintext, and the process of retrieving data does not require verification. To retrieve a specific data, you need to send the following JSON data to the server:

```
{
	"type": "read",
	"name": "name_of_the_data",
	"maxn": MAX_OBJECT_GET
}
```

Where `MAX_OBJECT_GET` represents the number of objects you want to retrieve, and it should be a positive integer. The value of `MAX_OBJECT_GET` is not very important for retrieving single-value data. When you try to retrieve the value of a multi-value data, the server will return the closest `MAX_OBJECT_GET` data to the tail of the data queue (if the number of elements in the entire data queue is less than `MAX_OBJECT_GET`, all values in the data queue will be returned).

### Response

Assuming the request is correct, the server will return a JSON data:

```json
{
    "result": "read success",
    "data": [
        RETURN_VALUE_1,
        RETURN_VALUE_2,
        ...
    ]
}
```

If the data corresponding to the requested name is not found, the read operation will still be successful, but the contents of the data field will be an empty list. If there is an error in the request, the server will return data containing only the result field, similar to the feedback when writing data fails.

## Hash Value

Here's the algorithm in Python3 pseudo-code to calculate the value of the hash attribute in the JSON included in the POST request when we try to write data, assuming that `SERVER_PASSWORD` is a string set by the server:

```python
import json
import hashlib

def getMd5(s: str):
    assert type(s) == str
    str_to_encode = s
    md5_obj = hashlib.md5()
    md5_obj.update(str_to_encode.encode('utf-8'))
    md5_code = md5_obj.hexdigest()
    return str(md5_code)

def getObjectWithHashAttribute(GetObjectWithoutHashAttribute):
    data = GetObjectWithoutHashAttribute()
    data['hash'] = SERVER_PASSWORD
    hash_value = getMd5(json.dumps(data))
    data['hash'] = hash_value
    return data # get the correct hash value
```

