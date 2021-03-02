#!/root/programs/kibubu/.venv/bin/python

import dicttoxml as xml
import requests
import random
import time
import csv

URL = 'http://10.99.1.161:6060/TELEPIN'


def topup_100k(msisdn):
    print('Topup')
    req_xml = f'''
        <TCSRequest>
        <UserName>255659632115</UserName>
        <TerminalType>USD</TerminalType>
        <Password>1902</Password>
        <Function name="PAYMENT">
            <Param1>{msisdn}</Param1>
            <Param2>100000</Param2>
            <Param5>187</Param5>
            <Param11>TTT1603719225346R9701</Param11>
        </Function>
        <CheckOnly>false</CheckOnly>
        </TCSRequest>
    '''
    print(req_xml)
    headers = {
        'Content-Type': 'text/xml'
    }
    res = requests.post(URL, req_xml, headers=headers)
    if res.ok:
        res_xml = res.text
        print(res_xml)
        root = ET.fromstring(res_xml)
        print(root)
    else:
        print('Failed: ', res.text)


def signup_contr(amount, msisdn, pin):
    print('Signup')
    req_xml = f'''
        <TCSRequest>
        <UserName>{msisdn}</UserName>
        <Password>{pin}</Password>
        <TERMINALTYPE>USD</TERMINALTYPE>
        <Function name="SUBSCRIBECONTRIBUTETOSAVINGPLAN">
            <param1>5</param1>
            <param2>{amount}</param2>
        </Function>
        </TCSRequest>
    '''
    print(req_xml)
    headers = {
        'Content-Type': 'text/xml'
    }
    res = requests.post(URL, req_xml, headers=headers)
    if res.ok:
        res_xml = res.text
        print(res_xml)
    else:
        print('Failed: ', res.text)


def saving_trans(amount, msisdn, pin):
    print('Saving: ', amount, msisdn, pin)
    req_xml = f'''
        <TCSRequest>
        <UserName>{msisdn}</UserName>
        <Password>{pin}</Password>
        <TERMINALTYPE>USD</TERMINALTYPE>
        <Function name="SAVINGCONTRIBUTION">
            <param2>{amount}</param2>
        </Function>
        </TCSRequest>
    '''
    print(req_xml)
    headers = {
        'Content-Type': 'text/xml'
    }
    res = requests.post(URL, req_xml, headers=headers)
    if res.ok:
        res_xml = res.text
        print("Res", res_xml)
        if 'TcsError_110208' in res_xml:
            topup_100k(msisdn)
            signup_contr(amount, msisdn, pin)
    else:
        print('Failed: ', res.text)


def withdraw_trans(amount, msisdn, pin):
    print('Withdraw: ', amount, msisdn, pin)
    req_xml = f'''
        <TCSRequest>
        <UserName>{msisdn}</UserName>
        <Password>{pin}</Password>
        <TERMINALTYPE>USD</TERMINALTYPE>
        <Function name="SAVINGWITHDRAWAL">
            <param1>False</param1>
            <param3>{amount}</param3>
        </Function>
        </TCSRequest>
    '''
    print(req_xml)
    headers = {
        'Content-Type': 'text/xml'
    }
    res = requests.post(URL, req_xml, headers=headers)
    if res.ok:
        res_xml = res.text
        print(res_xml)
    else:
        print('Failed: ', res.text)


def do_kibubu(amount, msisdn, pin):
    saving_trans(amount, msisdn, pin)
    amount = random.randint(round(amount * 0.6), amount)
    withdraw_trans(amount, msisdn, pin)


def numbers():
    file_name = 'kibubu.csv'
    with open(file_name, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield (row['11 Digit Msisdn'], row['Pin'])


if __name__ == "__main__":
    while True:
        try:
            for num in numbers():
                amount = random.randint(100, 10000)
                msisdn, pin = num
                do_kibubu(amount, msisdn, pin)
            time.sleep(10)
        except Exception as ex:
            print(ex)
