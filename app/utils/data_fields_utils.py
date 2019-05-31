TRIMMED_FIELDS = [
    "create_date",
    "update_date",
    "offer_type",
    "deleted"
]


def trim_fields(data):
    for field in TRIMMED_FIELDS:
        if field in data:
            del data[field]
    return data


def fields_to_str(data):
    for field in data.keys():
        if data[field]:
            data[field] = str(data[field])

    return data


def remove_none_and_bool_fields(data):
    ret_data = {}
    for field in data.keys():
        if data[field]:
            if isinstance(data[field], bool):
                ret_data[field] = 1
            else:
                ret_data[field] = data[field]

    return ret_data


def prepare_object_data(data):
    data = trim_fields(data)
    data = remove_none_and_bool_fields(data)
    data = fields_to_str(data)

    return data
