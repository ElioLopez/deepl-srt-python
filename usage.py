import json
import os
import urllib.parse
import urllib.request


with open(os.path.dirname(os.path.abspath(__file__)) + '/config.json') as j:
    config = json.load(j)

AUTH_KEY = config['auth_key']
DEEPL_TRANSLATE_EP = 'https://api.deepl.com/v2/usage'


def monitor_usage():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; utf-8'
    }

    params = {
        'auth_key': AUTH_KEY
    }

    req = urllib.request.Request(
        DEEPL_TRANSLATE_EP,
        method='POST',
        data=urllib.parse.urlencode(params).encode('utf-8'),
        headers=headers
    )

    try:
        with urllib.request.urlopen(req) as res:
            res_json = json.loads(res.read().decode('utf-8'))
            print(json.dumps(res_json, indent=2, ensure_ascii=False))
    except urllib.error.HTTPError as e:
        print(e)


if __name__ == '__main__':
    monitor_usage()
