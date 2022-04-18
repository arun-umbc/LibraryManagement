def create_response_dict(data, message, success=True, page=None, **kwargs):
    response_dict = dict()
    if success:
        response_dict["data"] = data
    if page:
        response_dict['page'] = page
    response_dict["message"] = message
    response_dict["success"] = success
    response_dict.update(kwargs)
    return response_dict