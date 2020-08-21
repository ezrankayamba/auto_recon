import json
import pysftp
import pandas as pd
import utils

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
                r_f1, rf2 = utils.get_files(cat)
                with sfpt.open(r_f1) as csv_file1, sfpt.open(r_f2) as csv_file2:
                    df1 = pd.read_csv(csv_file1)
                    df2 = pd.read_csv(csv_file2)
                    print(df1.head())
                    print(df2.head())
                    df2.rename(columns={'Ext_TransID': 'TRANSFER_ID', 'TransID': 'ReceiptNo'}, inplace=True)
                    df = pd.merge(df1, df2[["TRANSFER_ID", "TransStatus", "ReceiptNo"]], on='TRANSFER_ID', how='inner')
                    print(df.head())
                    df.to_csv('outputs/Tigo2TTCL_20200821.csv', index=False)
