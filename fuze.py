
import struct
from statistics import fmean, mean
import numpy as np
import pandas as pd
import json
from tqdm import tqdm
import re


def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])


list_of_dicts = []
with open(r'220215.json', 'r') as f:
    data = json.load(f)
index = 0
for req_res in data:
    for log in req_res['req_res']:
        # print(log)
        # index += 1
        list_of_dicts.append(log)
df = pd.DataFrame(list_of_dicts)
df2 = df.drop(['req_headers', 'res_headers'], axis=1)
req_query = df2['req_query']
req_payload = df2['req_payload']

LENGTH = len(req_payload)  # Number of iterations required to fill pbar

pbar = tqdm(total=LENGTH)  # Init pbar
list_of_payloads = []
for row in req_payload:
    res = json.loads(row)
    pbar.update(n=1)  # Increments counter by 1
    list_of_payloads.append(res['0'])
payload_df = pd.DataFrame(columns=['payload_0'])
payload_df['payload_0'] = list_of_payloads
payload_df.drop_duplicates(inplace=True)
list_of_queries = []
keys_list = []
values_list = []
pbar2 = tqdm(total=len(req_query))
temp_query_df = pd.DataFrame(columns=['key', 'value'])
for index, row in enumerate(req_query):
    res = json.loads(row)
    keys = list(res.keys())
    values = list(res.values())
    items = list(res.items())
    list_of_queries.append(items)
    keys_list.append(keys)
    values_list.append(values)
    pbar2.update(n=1)
    # for key, value in res.items():
    #     dict_of_queries[key] = value
test_df = pd.DataFrame(columns=['key', 'value'])
test_df['key'] = keys_list
test_df['value'] = values_list
query_df = pd.DataFrame(columns=['key', 'value'])
query_df['key'] = test_df['key'].explode()
query_df['value'] = test_df['value'].explode()
query_df['value'] = query_df.value.astype(str)
query_df.drop_duplicates(inplace=True, subset=['key', 'value'])
query_df.dropna(inplace=True)
# params_per_key = query_df.groupby(['key'])['value'].apply(list))
params_per_key = pd.DataFrame(query_df.groupby(['key'])['value'].apply(list))

query_df_formatted = params_per_key.copy().T
for col in df.columns:
    try:
        curr_list = query_df_formatted[col].tolist()
        # convert curr_list to a list of integeres
        try:
            curr_list = [int(x) for x in curr_list[0]]
        except:
            curr_list = [float(x) for x in curr_list[0]]
        # replace row with the new list
        query_df_formatted.loc['value', col] = curr_list
    except Exception as e:
        print(f"{e} Failed on {col} it's probably a string")
        # df.loc['value',col] = curr_list
# params_per_key['value'] = [','.join(map(str, l)) for l in params_per_key['value']]
# THIS IS IMPORTANT AFFFF
# dict like dataframe to show param attrs
# first method and status codes
mapper_df = pd.DataFrame(
    columns=['param_name', 'type', 'attrs', 'value', 'transformed_value', 'min', 'max', 'variance', 'mean'])
for index, row in enumerate(df['method'].unique()):
    mapper_df.loc[0, 'param_name'] = 'method'
    mapper_df.loc[0, 'type'] = 'method'
    mapper_df.loc[0, 'value'] = df['method'].unique()
    mapper_df.loc[0, 'transformed_value'] = df['method'].unique()

for index2, row in enumerate(df['status'].unique()):
    mapper_df.loc[1, 'param_name'] = 'status'
    mapper_df.loc[1, 'type'] = 'status'
    mapper_df.loc[1, 'value'] = df['status'].unique()
    mapper_df.loc[1, 'transformed_value'] = df['status'].unique()

# get all ID type params, currently using simple regex, the map(len) filters out IDs with only 1 possible value in the log
temp_id_df = params_per_key[
    params_per_key.index.str.contains('ID$', flags=re.IGNORECASE) | params_per_key.index.str.contains('^ID',
                                                                                                      flags=re.IGNORECASE)]
temp_id_df = temp_id_df[temp_id_df['value'].map(len) != 1]

# int, float and string params
counter = 2
for param, row in params_per_key.iterrows():
    curr_list = row[0]
    if param in temp_id_df.index:
        # id found
        mapper_df.loc[counter, 'param_name'] = param
        mapper_df.loc[counter, 'type'] = "ID"
        mapper_df.loc[counter, 'value'] = curr_list
        mapper_df.loc[counter, 'transformed_value'] = curr_list
    else:
        try:
            try:
                # int
                curr_list = [int(x) for x in curr_list]
                mapper_df.loc[counter, 'param_name'] = param
                mapper_df.loc[counter, 'type'] = "integer"
                mapper_df.loc[counter, 'value'] = curr_list
                trasformed_values = [hex(x) for x in curr_list]
                mapper_df.loc[counter, 'transformed_value'] = trasformed_values
                mapper_df.loc[counter, 'min'] = min(curr_list)
                mapper_df.loc[counter, 'max'] = max(curr_list)
                mapper_df.loc[counter, 'variance'] = np.var(curr_list)
                mapper_df.loc[counter, 'mean'] = mean(curr_list)
            except:
                # float
                curr_list = [float(x) for x in curr_list]
                mapper_df.loc[counter, 'param_name'] = param
                mapper_df.loc[counter, 'type'] = "float"
                mapper_df.loc[counter, 'value'] = curr_list
                trasformed_values = [float_to_hex(x) for x in curr_list]
                mapper_df.loc[counter, 'transformed_value'] = trasformed_values
                mapper_df.loc[counter, 'min'] = min(curr_list)
                mapper_df.loc[counter, 'max'] = max(curr_list)
                mapper_df.loc[counter, 'variance'] = np.var(curr_list)
                mapper_df.loc[counter, 'mean'] = fmean(curr_list)
        except:
            # string
            mapper_df.loc[counter, 'param_name'] = param
            mapper_df.loc[counter, 'type'] = "string"
            mapper_df.loc[counter, 'value'] = curr_list
            mapper_df.loc[counter, 'transformed_value'] = curr_list
    counter += 1
mapper_df.loc[counter + 1, 'param_name'] = 'payload_0'
mapper_df.loc[counter + 1, 'type'] = 'string'
mapper_df.loc[counter + 1, 'value'] = payload_df['payload_0'].values
mapper_df.loc[counter + 1, 'transformed_value'] = payload_df['payload_0'].values

list_of_path_params = []
path_params = ['deals', 'address', 'license', 'notification', 'rates', 'trades', 'zip', 'pub', 'dealership',
               'insurance',
               'protection', 'rebates', 'inventory', 'logs', 'docs', 'customers/']
no_uuid_df = payload_df['payload_0'].str.replace(
    r'[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}', 'UUID', regex=True)
no_uuid_df.drop_duplicates(inplace=True)
for i in path_params:
    list_of_path_params.append(no_uuid_df[no_uuid_df.str.contains(i)])  # deals variables
for path_count, i in enumerate(list_of_path_params):
    mapper_df.loc[counter + 2 + path_count, 'param_name'] = path_params[path_count]
    mapper_df.loc[counter + 2 + path_count, 'type'] = 'path'
    mapper_df.loc[counter + 2 + path_count, 'value'] = i.to_list()
    mapper_df.loc[counter + 2 + path_count, 'transformed_value'] = i.to_list()
mapper_df['values_length'] = [len(x) for x in mapper_df['value']]
pass
