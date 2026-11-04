#%%

import requests
import pandas as pd
import datetime
import json
import time

#%%

def get_response(**kwargs): # kwargs permite inserir params na chamada

    url = "https://www.tabnews.com.br/api/v1/contents/"

    resp = requests.get(url, params=kwargs)

    return resp

def save_data(data, option='json'):
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")


    if option == 'json':
        with open(f"data/contents/json/{now}.json", 'w') as open_file:
            json.dump(data, open_file, indent=4)

    elif option == 'parquet':
        df = pd.DataFrame(data)
        df.to_parquet(f"data/contents/parquet/{now}.json", index=False)


#%%

page = 1

while True:
    resp = get_response(page=page, per_page=100, strategy="new")
    if resp.status_code == 200:
        print(page)
        data = resp.json()
        save_data(data)
        page += 1
        if (page > 15):
            break
    else:
        time.sleep(5)


# %%
