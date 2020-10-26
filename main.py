import os
import sys
import requests
import json


# r= requests.get("https://hooks.slack.com/services/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")
d= {"text":"WORK"}
#r= requests.post("https://hooks.slack.com/services/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", data=json.dumps(d))
#print(r.text)

print('hello world!', sys.argv[1])
print('---')
