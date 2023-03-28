# CompactData Python Library

A Python library for parsing and serialising data in the CompactData format. CompactData is a compact data serialisation format that prioritises efficiency of data storage and transport. It is well suited for use cases where efficient data storage and transport is a priority.

## Features

- Parse CompactData strings into Python objects
- Serialise Python objects into CompactData strings
- Compatible with Python 3.6 and higher

## Installation

To install the CompactData Python library, use the following command:

```sh
pip install compactdata
```

## Usage

### Parsing CompactData strings

To parse a CompactData string into a Python object, use the `compactdata.loads()` function:

```python
import compactdata

compactdata_string = "my_object=(string=`abc`;number=1;array=[1;2;3];map=(a=1;b=2;c=3))"
parsed_object = compactdata.loads(compactdata_string)
print(parsed_object)
# Output: {'my_object': {'string': 'abc', 'number': 1, 'array': [1, 2, 3], 'map': {'a': 1, 'b': 2, 'c': 3}}}
```

### Serialising Python objects

To serialise a Python object into a CompactData string, use the `compactdata.dumps()` function:

```python
import compactdata

python_object = {"key1": "value1", "key2": 2}
compactdata_string = compactdata.dumps(python_object)
print(compactdata_string)
# Output: (key1=value1;key2=2)
```

## Examples

Here are some examples of parsing and serialising different CompactData strings and Python objects:

```python
import compactdata

# Parsing CompactData strings
compactdata_strings = [
    "my_object=(string=`abc`;number=1;array=[1;2;3];map=(a=1;b=2;c=3))",
    "[1;2;3]",
    "a=1;b=2.5;c=10e3",
    "@dv=1;salts=[(s=salts.domainverification.org;ids=[342c208d-0523-4d22-b7dd-32952dbeace2]);(s=example.com;ids=[90797a69-205b-4a35-88fe-8a186392ea15])]",
]

for compactdata_string in compactdata_strings:
    print(compactdata.loads(compactdata_string))
    
# Output:
# {'my_object': {'string': 'abc', 'number': 1, 'array': [1, 2, 3], 'map': {'a': 1, 'b': 2, 'c': 3}}}
# [1, 2, 3]
# {'a': 1, 'b': 2.5, 'c': 10000.0}
# {'@dv': 1, 'salts': [{'s': 'salts.domainverification.org', 'ids': ['342c208d-0523-4d22-b7dd-32952dbeace2']}, {'s': 'example.com', 'ids': ['90797a69-205b-4a35-88fe-8a186392ea15']}]}

# Serialising Python objects
python_objects = [
    [1, 2, 3, "123"],
    {"key1": "value1", "key2": 2},
    "string_value",
    123,
    [1, {"k": "v"}, 2],
]

for python_object in python_objects:
    print(compactdata.dumps(python_object))

# Output:
# [1;2;3;123]
# (key1=value1;key2=2)
# string_value
# 123
# [1;(k=v);2]
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support and Contributions

If you encounter any issues or have feature requests, please [open an issue](https://github.com/NUMtechnology/compactdata-python/issues) on GitHub. Contributions to this project are welcome. To contribute, please fork the repository, make your changes, and submit a pull request.

For more information about the CompactData format, visit the official website at https://compactdata.org.