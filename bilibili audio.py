import requests
import re
import json
from lxml import etree
import os

e = "b站音频"
if not os.path.exists(e):
    os.mkdir(e)

cookie = "buvid3=FFF2A175-1D39-59CD-CBD1-67170D3A88A033008infoc; b_nut=1711377633; buvid4=275E9C2D-D600-41C6-74C1-02B76B485E7D22393-024030704-08Ez73LMktRnV7Gn47CzPw%3D%3D; CURRENT_FNVAL=4048; _uuid=A2FB66FA-B1031-BB57-1B52-C2D831A5F731033198infoc; bsource=search_bing; rpdid=|(k~RkmJ~~mJ0J'u~uuJ~~YJl; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTE2MzY4MzUsImlhdCI6MTcxMTM3NzU3NSwicGx0IjotMX0.sVCmRm3gyAj_k5NtpsO9Q1lMN8q4wq80QgPgDYqskis; bili_ticket_expires=1711636775; SESSDATA=832e7043%2C1726929643%2C2b868%2A32CjCbtgpP_RUGPmv_tZpB9qklMN7svfqkw7sixa1ZubRutTQ0m7mTsBDuxs2eHTprSj0SVlFoZlV1ZzF6RHBXZm52LVNVUjdIVk85cThueVlHWExBR0o1VlkwdkhadnllNFZwUGJOT3NFbTgxTjJUR1J4ZkNSOEhXbU1WSXl6NVdHZEpRSmJBZlVnIIEC; bili_jct=04569ea3076228c722dc3ddf21e2e950; DedeUserID=396761918; DedeUserID__ckMd5=dae6264f4de26749; sid=7ic5kya0; enable_web_push=DISABLE; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; home_feed_column=4; hit-dyn-v2=1; PVID=1; b_lsid=10A4FEF2A_18E7FE86FC9; bp_video_offset_396761918=913557853337288738; fingerprint=b18c4dd11c3f3dacaf9206d43b868247; buvid_fp_plain=undefined; buvid_fp=b18c4dd11c3f3dacaf9206d43b868247; browser_resolution=625-587"  # 请替换为您的实际cookie值

while True:
    url = input("请输入url：")

    headers = {
        "cookie": cookie,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    }
    resp_ = requests.get(url, headers=headers)
    resp = resp_.text
    resp_.close()

    tree = etree.HTML(resp)
    title = tree.xpath('//h1/text()')[0]

    try:
        tree1 = tree.xpath('/html/head/script[4]/text()')[0]
        tree1 = re.sub(r'window.__playinfo__=', '', tree1)
        tree1 = json.loads(tree1)
    except:
        print("不是script[4]")
        tree1 = tree.xpath('/html/head/script[3]/text()')[0]
        tree1 = re.sub(r'window.__playinfo__=', '', tree1)
        tree1 = json.loads(tree1)

    id_list = [audio['id'] for audio in tree1['data']['dash']['audio']]
    audio_url = tree1['data']['dash']['audio'][id_list.index(max(id_list))]['backupUrl'][0]

    print("正在下载", title)
    headers521 = {
        "referer": url,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36",
    }

    resp2_ = requests.get(audio_url, headers=headers521)
    resp2 = resp2_.content
    resp2_.close()

    new_title = re.sub(r'[\\/:*?"<>|\n]', '_', title)
    with open(f"{e}/{new_title}.m4a", mode='wb') as x:
        x.write(resp2)

    print("Audio downloaded:", new_title)