# url4api

Library provides function `split` that splits an url into set of attributes.
This is a functionality put on top of standard urllib.parse. So url has to be
valid, but you can define that there is expected version component of given
type (ie integer or float) and any other attribute.

Example usage:

```python

import url4api

print(url4api.split('http://www.example.com/').as_dict())
{'port': None, 'url': '', 'protocol': 'http', 'domain': 'www.example.com'}

print(url4api.split('http://www.example.com/dd/ff/').as_dict())
{'port': None, 'url': 'dd/ff/', 'protocol': 'http', 'domain': 'www.example.com'}

print(url4api.split('http://www.example.com/3.0/dd/ff/').as_dict())
{'port': None, 'url': '3.0/dd/ff/', 'protocol': 'http', 'domain': 'www.example.com'}

print(url4api.split('http://www.example.com/3.0/dd/ff/', pattern='<version:number>/<...>').as_dict())
{'port': None, 'url': 'dd/ff/', 'protocol': 'http', 'domain': 'www.example.com', 'version': 3}

print(url4api.split('http://www.example.com/3.0/dd/ff/', pattern='<version:double>/<...>').as_dict())
{'port': None, 'url': 'dd/ff/', 'protocol': 'http', 'domain': 'www.example.com', 'version': 3.0}

print(url4api.split('http://www.example.com/3.0/letters/f/', pattern='<version:double>/<namespace>/<...>').as_dict())
{'port': None, 'version': 3.0, 'url': 'f/', 'protocol': 'http', 'namespace': 'letters', 'domain': 'www.example.com'}

# or more exotic:

print(url4api.split('http://www.example.com/3.0/letters/f/', pattern='<version:double>/<namespace>/').as_dict())
{'port': None, 'version': 3.0, 'url': '', 'protocol': 'http', 'namespace': 'letters', 'domain': 'www.example.com'}
```

Pattern is a string that should contains groups, each group can be defined as `<some_name>` or `<some_name:some_type>`.

Where:
    `some_name` is any unicode valid string
    `some_type` is one of: `number`, `double`, `string` or `bool` (if not provided defaults to string)

There is special group `<...>` that consumes everything that follows.

## Testing

Git clone reposiotry, pip install depedency and then run nosetests by typing `nosetests`.
