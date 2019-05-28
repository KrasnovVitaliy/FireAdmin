TRIMMED_FIELDS = [
    "create_date",
    "update_date",
    "offer_type",
    "deleted"
]


def trim_fields(data):
    print(data)
    for field in TRIMMED_FIELDS:
        del data[field]
    print('!!!!!!!')
    print('data')
    return data
