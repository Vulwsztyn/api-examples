#!/usr/bin/env python3

import requests
import base64
import uuid
import urllib
import sys

from OpenSSL import crypto
from datetime import datetime

API_KEY = open('./api_key').read()
assert API_KEY is not None

API_BASE = sys.argv[1] if len(sys.argv) > 1 else 'https://api.walutomat.pl'
URI = '/api/v2.0.0/transfer/iban'

private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, open('./private.key').read())

ts = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
submit_id = uuid.uuid4()

body = {
    'volume': '90.00',
    'currency': 'USD',
    'dryRun': 'false',
    'title': 'Przelew z walutmatu',
    'accountNumber': 'PL71967221037685356996377436',
    'recipientName': 'Adventure Works Ltd',
    'transferCostInstruction': 'SENDER_VOLUME',
    'submitId': submit_id
}

urlencoded = urllib.parse.urlencode(body)
data_to_sign = f'{ts}{URI}{urlencoded}'

signature = crypto.sign(private_key, data_to_sign, 'sha256') 
signature_base64 = base64.b64encode(signature)

headers = {
  'X-API-Key': API_KEY,
  'X-API-Signature': signature_base64,
  'X-API-Timestamp': ts,
  'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.post(f'{API_BASE}{URI}', data = urlencoded, headers = headers)

print(response.text)