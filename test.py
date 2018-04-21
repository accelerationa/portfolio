import requests
import json
from StringIO import StringIO


r = requests.get('https://www.google.com/finance/getprices?q=ADR&i=3600&p=2Y&f=d,c,h,l,o,v')
print type(r.content)