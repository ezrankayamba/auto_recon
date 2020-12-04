import json
import pysftp
import pandas as pd
import utils
import os
import re
import sys
import traceback


BASE_REMOTE_DIR = '/data/exchangefiles/'
with open('credentials.json') as creds_file:
    creds = json.load(creds_file)
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    creds['cnopts'] = cnopts
    # print(creds)
    try:
        with pysftp.Connection(**creds) as sftp:
            print('Connected...')
            with open('config.json') as file:
                categories = json.load(file)['categories']

                for cat in categories:
                    name = cat['name']
                    print()
                    print(f'================={name}======================')
                    if not cat['enabled']:
                        continue
                    try:
                        r_f1, r_f2, tg_file_date, ot_file_date, sep, regex = utils.get_files(cat, sftp)
                        print(r_f1, r_f2)

                        def extract_trx(x):
                            txn = re.match(regex, x).group(1)
                            return txn
                        with sftp.open(r_f1) as csv_file1, sftp.open(r_f2) as csv_file2:
                            df1 = pd.read_csv(csv_file1)
                            df2 = pd.read_csv(csv_file2, sep)
                            # print(df1.head())
                            # del cat['columns']['TRANSFER_ID_REGEX']
                            df2.rename(columns=cat['columns'], inplace=True)
                            print(df2.head())
                            print(df2.columns)

                            if regex:
                                df2["TRANSFER_ID"] = df2['TRANSFER_ID'].apply(extract_trx)
                                df2["TRANSFER_ID"] = pd.to_numeric(df2["TRANSFER_ID"])
                            if 'Transfer_ID' in df1.columns:
                                df1.rename(columns={'Transfer_ID': 'TRANSFER_ID'}, inplace=True)
                            df = pd.merge(df1, df2[["TRANSFER_ID", "TransStatus", "ReceiptNo"]], on='TRANSFER_ID', how='left')
                            print(df.head())

                            dt_str = tg_file_date.strftime('%Y%m%d')
                            path = f'outputs/{name}'
                            if not os.path.exists(path):
                                os.makedirs(path)
                            df1.to_csv(f'{path}/Tigo_{name}_{dt_str}.csv', index=False)
                            df2.to_csv(f'{path}/Other_{name}_{dt_str}.csv', index=False)
                            df.to_csv(f'{path}/Result_{name}_{dt_str}.csv', index=False)
                    except Exception as ex:
                        print("Error: ", ex)
                        print("-"*60)
                        traceback.print_exc(file=sys.stdout)
                        print("-"*60)

    except Exception as ex:
        print(ex)
