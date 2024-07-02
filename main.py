import streamlit as st
import aiohttp
import asyncio
import re
import time
import requests

def Execute(cookie, post, share_count, delay):
	head = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
		'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': "Windows",
		'sec-fetch-dest': 'document',
		'sec-fetch-mode': 'navigate',
		'sec-fetch-site': 'none',
		'sec-fetch-user': '?1',
		'upgrade-insecure-requests': '1'
	}
	class Share:
		async def get_token(self, session):
			try:
				head['cookie'] = cookie
				async with session.get('https://business.facebook.com/content_management', headers=head) as response:
					data = await response.text()
					access_token = 'EAAG' + re.search('EAAG(.*?)","', data).group(1)
					return access_token, head['cookie']
			except Exception as er:
				st.error(":red-background[blocked] Cookie blocked")
		async def share(self, session, token, cookie):
			ji = {
				"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
				"sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
				"sec-ch-ua-mobile": "?0",
				"sec-ch-ua-platform": "Windows",
				"sec-fetch-dest": "document",
				"sec-fetch-mode": "navigate",
				"sec-fetch-site": "none",
				"sec-fetch-user": "?1",
				"upgrade-insecure-requests": "1",
				"cookie": cookie,
				"accept-encoding": "gzip, deflate",
				"host": "b-graph.facebook.com"
			}
			count = 1
			while count < share_count + 1:
				time.sleep(delay)
				async with session.post(f'{st.secrets.xnxx}{post}&published=0&access_token={token}', headers=ji) as response:
					data = await response.json()
					if 'id' in data:
						st.write(f"(:green[{count}]/:green[{share_count}]) - Successfully shared")
						count += 1
					else:
						st.write(f":red-background[Blocked] :red[cookie blocked]\nTotal success :green-background[{count}]")
						return
	async def main(num_tasks): 
		async with aiohttp.ClientSession() as session:
			share = Share()
			token, cookie = await share.get_token(session)
			tasks = []
			for i in range(num_tasks):
				task = asyncio.create_task(share.share(session, token, cookie))
				tasks.append(task)
			await asyncio.gather(*tasks)
	asyncio.run(main(1))

def cCheck(cookie):
	res = requests.get(f"{st.secrets.aso}{cookie}").json()
	if res['status'] == 'Cookie Live': return True
	return False

COOKIE = st.text_area("Cookie")
POST = st.text_input("Post link")
COUNT = st.number_input("Count", min_value=1, max_value=50000)
DELAY = st.number_input("Delay", min_value=0, max_value=50000)
if st.button("Submit", type='primary'):
	if not COOKIE or not POST or not COUNT:
		st.error("Missing inputs value")
	elif not cCheck(COOKIE):
		st.error("Cookie Die")
	elif not POST.startswith('https://www.facebook.com/'):
		st.error("Invalid post link")
	else:
		with st.container(border=True):
			i = Execute(COOKIE, POST, int(COUNT), int(DELAY))
