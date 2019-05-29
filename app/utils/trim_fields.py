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
        data[field] = str(data[field])

    return data
