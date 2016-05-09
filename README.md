serene_bardeen
==============

Article link tracer


# Installation
----------

## Prerequsite

```bash
sudo apt-get update
sudo apt-get install build-essential python-dev mongodb
sudo apt-get install python-software-properties
sudo apt-get update

wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
rm get-pip.py

```

# API
----------

## Link
### Create short link

- API: `POST {{base_url}}/api/links`
- Parameters:
    - secret
	- original_link: The original link to be registered.
	- article_id: The article containing the original link.
- Response:
```json
{
      "id": "1234",
      "article_id": "9e04af84-a7ed-4578-8d5b-b0660bf94dfa",
      "original_link": "http://www.google.com",
      "created_at": 1415402702,
      "short_link": "{{base_url}}/1234"
}

```

### Redirect link

- API: `GET {{base_url}}/{{link_id}}`
- Parameters: none
- Response: 302

----------


## Click
### Get click events

- API: `GET {{base_url}}/api/clicks`
- Parameters:
    - Please see http://api.mongodb.org/python/current/api/pymongo/collection.html#pymongo.collection.Collection.find
    - spec: Available fields `click_id`, `link_id`, `ip`, `user_agent`, `created_at`.
    - fields
    - limit: Default is `100`.
- Response:
```json
[
    {
        "click_id": "54604e66802692367bcb991a",
        "link_id": "54604e8f802692367bcb991c",
        "ip": "170.190.250.24",
        "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "created_at": 1415597860
    }
]

```

