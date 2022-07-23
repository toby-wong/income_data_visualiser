from chalice import Chalice
from chalicelib.csv_utils import *

app = Chalice(app_name='backend')


@app.route('/')
def index():
    return {'hello': 'world'}

# @app.route('/regions', methods=['GET'])
# def list_regions():
#     # return table of results

#     return {'SA4 HH Weekly Income Counts': get_csv_data('SA4 HH Weekly Income Counts.csv').to_csv()}

# @app.route('/regions/{region}', methods=['GET'])
# def regions_filter(region):
#     # return table of results
#     return {region: multi_sort_csv('SA4 HH Weekly Income Counts.csv', [{'column': 'SA4 Region Name', 'query': region}]).to_csv()}



# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#

if __name__ == '__main__':
    print(list_regions())