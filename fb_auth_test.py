from firebase import firebase


def get_all(project_id):
    authentication = firebase.FirebaseAuthentication('KNCU1eqNlNun9YYX2l0l54ruXAYUK0y7xyOJVrZ2', '', True, True)
    fb = firebase.FirebaseApplication('https://{}.firebaseio.com'.format(project_id), authentication)
    result = fb.get('/', None)
    return result


if __name__ == "__main__":
    print(get_all("id10-dengi-srazy-ukr"))
