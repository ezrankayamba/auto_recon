import json
import pysftp
import pandas as pd

BASE_REMOTE_DIR = '/data/exchangefiles/'
with open('credentials.json') as creds_file:
    creds = json.load(creds_file)
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    creds['cnopts'] = cnopts
    print(creds)
    with pysftp.Connection(**creds) as sfpt:
        print('Connected...')
        f1 = f'W2B_20082020.csv'
        f2 = f'TIGO_TTCL_2020-08-20.csv'
        r_f1 = f't-pesa/TIGO/Data/Exchangefiles/{f1}'
        r_f2 = f't-pesa/TTCL/{f2}'
        with sfpt.open(r_f1) as csv_file1, sfpt.open(r_f2) as csv_file2:
            df1 = pd.read_csv(csv_file1)
            df2 = pd.read_csv(csv_file2)
            print(df1.head())
            print(df2.head())
            df2.rename(columns={'Ext_TransID': 'TRANSFER_ID'}, inplace=True)
            df = pd.merge(df1, df2, on='TRANSFER_ID', how='inner')
            print(df.head())
            df.to_csv('outputs/Tigo2TTCL_20200821.csv')
