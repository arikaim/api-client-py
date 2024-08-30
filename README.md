## Arikaim CMS Api Client for python
![version: 1.0.0](https://img.shields.io/github/release/arikaim/api-client-py.svg)
![license: MIT](https://img.shields.io/badge/License-MIT-blue.svg)


This repo is part of  [Arikaim CMS](http://arikaim.com)  project.


### Installation

```sh
pip install arikaim-client
```

### Usage

```python

from arikaim.client.client import ArikaimClient

client = ArikaimClient(host,apiKey)

data = {
    request data fields  key: value
}

response = client.request(method,url,data)

print(response.status)
print(response.to_dictonary())


#Add header
client.add_header({ 'key': 'value' })


#POST request 
response = client.post(url,data)

#GET request
response = client.get(url)

#PUT request
response = client.put(url,data)


```
