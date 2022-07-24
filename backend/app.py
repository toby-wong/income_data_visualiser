from chalice import Chalice
from chalicelib.csv_utils import *

app = Chalice(app_name='backend')

@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/search', methods=['GET'])
def search():
    # if app.current_request.query_params.get('state'):
    #     return {query: multi_sort_csv(state_key, [{'column': 'State', 'query': query}]).to_dict()}
    # elif app.current_request.query_params.get('region'):
    #     return {query: multi_sort_csv(region_key, [{'column': 'SA4 Region Name', 'query': query}]).to_dict()}
    # else:
    return {'Regions and State': get_regions_states()}

@app.route('/search/{query}', methods=['GET'])
def search(query):
    # return json of results
    query = query.replace('%20', ' ')
    if is_state(query):
        return {query: multi_sort_csv(state_key, [{'column': 'State', 'query': query}]).to_dict()}
    else:
        return {query: multi_sort_csv(region_key, [{'column': 'SA4 Region Name', 'query': query}]).to_dict()}

@app.route('/filter', methods=['GET'])
def filter():
    params = app.current_request.query_params
    multi = []
    if params.get('state'):
        multi.append({'column': 'State', 'query': params.get('state')})
    if params.get('composition'):
        multi.append({'column': 'Household Composition', 'query': params.get('composition')})
    if params.get('income'):
        multi.append({'column': 'Weekly Household Income', 'query': params.get('income')})
    return {'Filtered': multi_sort_csv(region_key, multi).to_dict()}

@app.route('/filter/{query}', methods=['GET'])
def filter(query):
    query = query.replace('%20', ' ')
    if is_state(query):
        return {'Regions': get_regions_in_state(query)}
    else:
        return {'Proportions': get_proportion(query)}
