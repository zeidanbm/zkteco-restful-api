import jsonschema

def validate_data(data, schema=None):
    if schema:
        try:
            jsonschema.validate(instance=data, schema=schema)
        except jsonschema.exceptions.ValidationError as e:
            return str(e)
        
    return None