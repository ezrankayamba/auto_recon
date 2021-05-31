import json
import pysftp
import pandas as pd
import utils
import os
import re
import sys
import traceback
from mailsender import send_mail
import configparser
import logger

config = configparser.ConfigParser()
config.read('mailsender.ini')


BASE_REMOTE_DIR = '/data/exchangefiles/'
with open('credentials.json') as creds_file:
    creds = json.load(creds_file)
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    creds['cnopts'] = cnopts
    # print(creds)
    try:
        with pysftp.Connection(**creds) as sftp:
            logger.debug('Connected...')
            with open('config.json') as file:
                categories = json.load(file)['categories']
                receivers = config['DEFAULT']['RECEIVERS']

                for cat in categories:
                    logger.debug(cat)
                    name = cat['name']
                    logger.debug()
                    logger.debug(f'================={name}======================')
                    if not cat['enabled']:
                        continue
                    try:
                        r_f1, r_f2, tg_file_date, ot_file_date, sep, regex = utils.get_files(cat, sftp)
                        logger.debug((r_f1, r_f2))

                        def extract_trx(x):
                            # print(x, regex)
                            try:
                                txn = re.match(regex, x.strip()).group(1)
                                return txn
                            except Exception as ex:
                                logger.debug(ex)
                                return None
                        tp_exists = sftp.exists(r_f1)
                        ot_exists = sftp.exists(r_f2)
                        if tp_exists and ot_exists:
                            tp_info = sftp.stat(r_f1)
                            ot_info = sftp.stat(r_f2)
                            logger.debug(("Tigo Pesa: ", tp_info))
                            logger.debug(("3rd Party: ", ot_info))
                            with sftp.open(r_f1) as csv_file1, sftp.open(r_f2) as csv_file2:
                                df1 = pd.read_csv(csv_file1)
                                df2 = pd.read_csv(csv_file2, sep)
                                df2.rename(columns=cat['columns'], inplace=True)

                                if regex:
                                    df2["TRANSFER_ID"] = df2['TRANSFER_ID'].apply(extract_trx)
                                    df2["TRANSFER_ID"] = pd.to_numeric(df2["TRANSFER_ID"])
                                if 'Transfer_ID' in df1.columns:
                                    df1.rename(columns={'Transfer_ID': 'TRANSFER_ID'}, inplace=True)
                                logger.debug(df2.head())
                                df = pd.merge(df1, df2[["TRANSFER_ID", "TransStatus", "ReceiptNo"]], on='TRANSFER_ID', how='left')
                                logger.debug(df.head())

                                dt_str = tg_file_date.strftime('%Y%m%d')
                                path = f'outputs/{name}'
                                if not os.path.exists(path):
                                    os.makedirs(path)
                                tigo_file = f'{path}/Tigo_{name}_{dt_str}.csv'
                                thirdparty_file = f'{path}/Other_{name}_{dt_str}.csv'
                                result_file = f'{path}/Result_{name}_{dt_str}.csv'
                                df1.to_csv(tigo_file, index=False)
                                df2.to_csv(thirdparty_file, index=False)
                                df.to_csv(result_file, index=False)
                                send_mail(receivers.split(','), subject=f'DAILY RECON - {name}', files=[tigo_file, thirdparty_file, result_file], zip_name=name)
                        else:
                            logger.debug("Error: ", "One of the 2 files not available")
                            msg = "Hello,\nKindly receive recon results.\n\nErrors encountered processing files"
                            if not tp_exists:
                                msg = f'{msg}\nTigo Pesa file missing:  {r_f1}'
                            if not ot_exists:
                                msg = f'{msg}\n3rd party file missing:  {r_f2}'
                            logger.debug(msg)
                            logger.debug("-"*60)
                            send_mail(receivers.split(','), subject=f'DAILY RECON - {name}', files=[], text=msg)
                    except Exception as ex:
                        logger.error(("Error: ", ex))
                        logger.error("-"*60)
                        traceback.print_exc(file=sys.stdout)
                        logger.error("-"*60)
                        send_mail(receivers.split(','), subject=f'DAILY RECON - {name}', files=[])

    except Exception as ex:
        logger.error(("Error: ", ex))
