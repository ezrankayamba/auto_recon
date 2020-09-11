import json
import pysftp
import pandas as pd
import utils
import os

BASE_REMOTE_DIR = '/data/exchangefiles/'
with open('credentials.json') as creds_file:
    creds = json.load(creds_file)
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    creds['cnopts'] = cnopts
    print(creds)
    with pysftp.Connection(**creds) as sfpt:
        print('Connected...')
        with open('config.json') as file:
            categories = json.load(file)['categories']
            for cat in categories:
                r_f1, r_f2, tg_file_date, ot_file_date = utils.get_files(cat)
                print(r_f1, r_f2, tg_file_date, ot_file_date)
                with sfpt.open(r_f1) as csv_file1, sfpt.open(r_f2) as csv_file2:
                    df1 = pd.read_csv(csv_file1)
                    df2 = pd.read_csv(csv_file2)
                    print(df1.head())
                    print(df2.head())
                    df2.rename(columns=cat['columns'], inplace=True)
                    df = pd.merge(df1, df2[["TRANSFER_ID", "TransStatus", "ReceiptNo"]], on='TRANSFER_ID', how='left')
                    print(df.head())
                    name = cat['name']
                    dt_str = tg_file_date.strftime('%Y%m%d')
                    path = f'outputs/{name}'
                    if not os.path.exists(path):
                        os.makedirs(path)
                    df1.to_csv(f'{path}/Tigo_{name}_{dt_str}.csv', index=False)
                    df2.to_csv(f'{path}/Other_{name}_{dt_str}.csv', index=False)
                    df.to_csv(f'{path}/Result_{name}_{dt_str}.csv', index=False)
