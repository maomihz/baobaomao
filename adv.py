from requests import get
from re import search
from random import choice
from base64 import b64encode

# Configs
ad_params = {
    'pcl': '55YXfeBODD7lAQdTRPNqKxsTwYkKi8eL1U6QURCpvZ4Z4HmZCS1YSnh0Xt2mybKQM7fd_aI_0Qj8NixHToWvxw..',
    'app_id': '100'
}
headers = {
    'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
}
tmp_file = 'urls.txt'
md_file = 'README.md'

ad_url = choice([
    'newversionupdate.thereadysystemscontentsset.bid',
    'testpconly12.thereadysystemscontentsset.download',
    'checksoft.yoursafestplacetocontent.review',
    'learn2upgrade.yoursafestcenter4contentsafegood.stream'
])

def test_url(url):
    r = get(url, headers=headers, allow_redirects=False)
    return r.status_code == 200

count = 0
while True:
    if count > 4:
        exit()
    count += 1
    r = get('http://kay-61.com/gts/', headers=headers, params={
        'token': 'f70b20908e28e16872529d1f8a385c5888680d54'
    })
    v_id_match = search(r'v_id=(.+?)[&"]', r.text)

    if not v_id_match:
        print('Error finding v_id')
        print(r.text)
        continue

    v_id = v_id_match.group(1)
    ad_params['v_id'] = v_id
    r2 = get('http://' + ad_url + '/dl.php',
                headers=headers,
                params=ad_params,
                allow_redirects=False)
    loc = search(r'https?://.+?\.dmg', r2.headers['Location'])
    if not loc:
        print('dmg error')
        print(r2.headers)
        continue
    loc = loc.group(0)
    success = True
    print(loc)
    break

# loc = 'https://s3.amazonaws.com/ff00a276-c291-48f0-aa66-dbb762eff4/G5fE/YJjz/AdobeFlashPlayerInstaller.dmg'
# loc = 'https://s3.amazonaws.com/3437bd/FD25C0261/AdobeFlashPlayerInstaller.dmg'

# Read old lists, update, and write back
try:
    with open(tmp_file, 'r') as f:
        f_urls = f.read().split('\n')
        urls = [a for a in f_urls if a]
        print(urls)
except FileNotFoundError:
    urls = []

if loc not in urls:
    urls.append(loc)
new_urls = list(filter(test_url, urls))
with open(tmp_file, 'w') as f:
    new_urls_s = '\n'.join(new_urls)
    f.write(new_urls_s)

# Generate Markdown
md = '''
# 刷流量啦！

以下是从莫名的广告网站收集来的刷流量链接，实时更新。

| 开刷 |  链接 |
|:---:|:---:|
'''
for u in new_urls:
    md += '|[Link](https://meow.maomihz.com/?{0})|[{1}]({1})|\n'.format(
        b64encode(u.encode('utf-8')).decode('utf-8'), u
    )
with open(md_file, 'w') as f:
    f.write(md)
