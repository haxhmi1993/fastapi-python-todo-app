
def success_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successfull'
    }


def invalid_request_response():
    return {
        'status': 400,
        'transaction': 'Failed'
    }
