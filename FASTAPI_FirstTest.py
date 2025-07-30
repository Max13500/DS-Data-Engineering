from fastapi import FastAPI

my_api = FastAPI()

@my_api.get('/')
def get_index():
    return {
        'method': 'get',
        'endpoint': '/'
        }

@my_api.get('/other')
def get_other():
    return {
        'method': 'get',
        'endpoint': '/other'
    }

@my_api.post('/')
def post_index():
    return {
        'method': 'post',
        'endpoint': '/'
        }

@my_api.delete('/')
def delete_index():
    return {
        'method': 'delete',
        'endpoint': '/'
        }

@my_api.put('/')
def put_index():
    return {
        'method': 'put',
        'endpoint': '/'
        }

@my_api.patch('/')
def patch_index():
    return {
        'method': 'patch',
        'endpoint': '/'
        }