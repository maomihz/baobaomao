from requests import get
from re import search
from random import choice
from base64 import b64encode
from json import loads, dumps
from datetime import datetime
import jinja2 as j2
from os.path import dirname

json_file = 'urls.json'
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6"
}
ad_params = {
    "pcl": "55YXfeBODD7lAQdTRPNqKxsTwYkKi8eL1U6QURCpvZ4Z4HmZCS1YSnh0Xt2mybKQM7fd_aI_0Qj8NixHToWvxw..",
    "app_id": "100"
}

# Jinja Environment
env = j2.Environment(
    loader=j2.FileSystemLoader(dirname(__file__))
)
env.filters['b64'] = lambda u : b64encode(u.encode('utf-8')).decode('utf-8')
def dateformat(value, format='%m/%d %H:%M'):
    return datetime.fromtimestamp(value).strftime(format)
env.filters['dateformat'] = dateformat

# Configs
def test_url(url):
    r = get(url, headers=headers, allow_redirects=False)
    return r.status_code == 200

def get_url():
    for i in range(4):
        # Request the source page
        r = get('http://kay-61.com/gts/', headers=headers, params={
            'token': 'f70b20908e28e16872529d1f8a385c5888680d54'
        })

        # Try to find a v_id
        v_id_match = search(r'v_id=(.+?)[&"]', r.text)
        if not v_id_match:
            continue
        ad_params['v_id'] = v_id_match.group(1)
        ad_url = search('http://(.+?)/', r.url).group(1)


        # Request the dl url
        r2 = get('http://' + ad_url + '/dl.php',
                    headers=headers,
                    params=ad_params,
                    allow_redirects=False)
        loc = search(r'https?://.+?\.dmg', r2.headers['Location'])
        if not loc:
            continue

        loc = loc.group(0)
        return (loc, ad_url)

if __name__ == '__main__':
    with open(json_file, 'r') as j:
        config = loads(j.read())

    dmg, host = get_url()

    # Add host to config
    if host not in config['ad_urls']:
        config['ad_urls'].append(host)

    # Append to the url list
    if dmg not in config['urls']:
        config['urls'][dmg] = {
            'url': dmg,
            'discovered': datetime.now().timestamp()
        }

    # Check url list
    config['urls'] = {
        k: v for k, v in config['urls'].items()
        if test_url(k)
    }

    # Still write the url TXT
    urls = sorted(config['urls'].values(), key=lambda x : x['discovered'], reverse=True)
    with open('urls.txt', 'w') as f:
        f.write('\n'.join(u['url'] for u in urls) + '\n')

    # Render Markdown Template
    template = env.get_template('README.md.j2')
    template.stream(urls=urls, hosts=config['ad_urls']).dump('README.md')

    with open('urls.json', 'w') as f:
        f.write(dumps(config, indent=2))
