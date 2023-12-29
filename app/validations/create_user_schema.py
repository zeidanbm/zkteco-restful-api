schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "user_id": { "type": "integer" },
    "user_data": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "privilege": { "type": "integer", "enum": [0, 1, 2] },
        "password": { "type": "string" },
        "group_id": { "type": "integer" },
        "card": { "type": "integer" }
      },
      "required": ["name"]
    }
  },
  "required": ["user_id", "user_data"]
}
