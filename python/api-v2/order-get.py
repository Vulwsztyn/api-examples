#!/usr/bin/env python3

import requests
import base64
import urllib
import sys

from OpenSSL import crypto
from datetime import datetime

ORDER_ID = 'f60281e2-f59d-4039-a751-bb7d26b28ba7'

API_KEY = open('./api_key').read()
assert API_KEY is not None
API_BASE = sys.argv[1] if len(sys.argv) > 1 else 'https://api.walutomat.pl'
URI = '/api/v2.0.0/market_fx/orders'
query = {'orderId': ORDER_ID}

private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, open('./private.key').read())

ts = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
urlencoded = urllib.parse.urlencode(query)
data_to_sign = f'{ts}{URI}?{urlencoded}'
signature = crypto.sign(private_key, data_to_sign, 'sha256') 
signature_base64 = base64.b64encode(signature)

headers = {
  'X-API-Key': API_KEY,
  'X-API-Signature': signature_base64,
  'X-API-Timestamp': ts
}
payload= {'currencyPair': 'EURPLN'}
response = requests.get(f'{API_BASE}{URI}', headers=headers, params=query).text

print(response)
