serene_bardeen
==============

Article link tracer


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
