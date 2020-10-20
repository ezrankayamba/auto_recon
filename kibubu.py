import dicttoxml as xml
import requests
import random
import time

URL = 'http://10.99.1.161:6060/TELEPIN'


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
        print(res_xml)
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


if __name__ == "__main__":
    numbers = [
        (255658123367, 8989),
        (255713123066, 2020),
        (255717490680, 1710),
        (255713123303, 1985),
        # (255717812122, 5050),
        (255715875043, 2708),
    ]
    for _ in range(1000):
        for num in numbers:
            amount = random.randint(100, 10000)
            msisdn, pin = num
            do_kibubu(amount, msisdn, pin)
        time.sleep(10)
