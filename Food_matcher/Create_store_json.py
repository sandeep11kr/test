import pandas as pd
import json
import argparse
import re
from ast import literal_eval

parser = argparse.ArgumentParser()
parser.add_argument('--store_location_file', "-s", help = "the file having the store details")
parser.add_argument("--file", "-f", help="mapped file location")
parser.add_argument("--master_loc", "-m", help="master file location")
parser.add_argument("--output_loc", "-o", help="master file location")

#params
args = parser.parse_args()

if args.file == None:
    args.file = '../melian/melian/Food_matcher/DoorDash_vs_Website_CouncilBluffs.csv'

if args.master_loc ==None:
    args.master_loc = 'master_menu.csv'

if args.output_loc ==None:
    args.output_loc = 'CouncilBluffs.json'
if args.store_location_file ==None:
    args.store_location_file = 'doordash\Fazoli_DoorDash_CouncilBluffs_56.csv'

def get_item_id(df, list_compare, column_fetch, column_compare):
    # print(list_compare, type(list_compare))
    fetch_list = []
    for i in list_compare:
      if i in list(df[column_compare].unique()):
        print(i)
        print(df[column_fetch][df[column_compare]==i].values, '\n\n')
        fetch_list.append(df[column_fetch][df[column_compare]==i].values[0])
      else:
        pass
    return fetch_list

master_df = pd.read_csv(args.master_loc)
df = pd.read_csv(args.file)
df.rename(columns={'Website_name':'name', "Website_category":"category", 
                    'Website_price': "price", "Website_description": "description"}, inplace = True)
df = pd.merge(df, master_df[['master_product_id', 'name']], on=['name'])
df['DoorDash_suggested item'] = df['DoorDash_suggested item'].str.replace("[0-9]+\. ", "").\
                                str.split('; ')
df['DoorDash_name'] = df['DoorDash_name'].str.replace("[0-9]+\. ", "").str.strip()
df['recommendation'] = df.apply(lambda x: get_item_id(df, 
                        literal_eval(str(x['DoorDash_suggested item'])), 
                        'master_product_id','DoorDash_name'), axis=1)
df = df.sort_values("name").reset_index(drop = True)
df.index.name = "store_product_id"
df = df.reset_index()
df[['store_product_id', 'recommendation', 'price', 'name', 'category', 'description']].\
    to_json('temp.json', orient='records')

address=''
zipcode = ''
store_name =''
with open(str(args.store_location_file)) as file:
    address = file.readline()
    print(address)
    m = re.search("([A-Za-z]+)_([A-Za-z]+)_([A-Za-z]+)", str(args.store_location_file))
    pin = re.search("(\d{5})", str(address))
    store_name = m.group(1)
    zipcode = pin.group(1)
    print(store_name, zipcode)
with open('temp.json') as json_file:
    recc = json.load(json_file)
    print(recc)
    data = {"store": {"name":store_name, "address": address, "zipcode": zipcode},\
       "recommendations":recc}
with open(str(args.output_loc), 'w') as outfile:
        json.dump(data, outfile)
    
