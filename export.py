import os
import bs4
import sys
import math
import subprocess
import urllib.request
from urllib import parse
from datetime import datetime
from colorthief import ColorThief
from time import gmtime, strftime
from PIL import Image, ImageDraw, ImageFont, ImageOps

subprocess.call('rm podcast.mp4', stderr = subprocess.DEVNULL)
subprocess.call('mkdir frames', stderr = subprocess.DEVNULL)

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'

url = sys.argv[1]
if url[:15] == 'https://aca.st/':
	try:
		req = urllib.request.Request(url)
		req.add_header('User-Agent', ua)
		with urllib.request.urlopen(req) as f:
			url_html = f.read().decode('utf-8')
		soup = bs4.BeautifulSoup(url_html, 'html5lib')
		seekUrl = soup.find('iframe')['src']
		startTime = int(round(float(parse.parse_qs(parse.urlparse(seekUrl).query)['seek'][0])))
	except:
		startTime = 0

if url[:15] == 'https://pca.st/':
	try:
		startTime = int(float(parse.parse_qs(parse.urlparse(url).query)['t'][0]))
	except:
		startTime = 0

elif url[:18] == 'https://player.fm/':
	if '#' in url:
		startTime = url.rsplit('#', 1)[1]
		h, m, s = startTime.split(':')
		startTime = int(h) * 3600 + int(m) * 60 + int(s)
	else:
		startTime = 0

elif url[:19] == 'https://castbox.fm/':
	if '_t=' in url:
		try:
			startTime = parse.parse_qs(parse.urlparse(url).query)['_t'][0]
			if startTime.count(':') == 1:
				startTime = startTime[:5]
				m, s = startTime.split(':')
				startTime = int(m) * 60 + int(s)
			else:
				h, m, s = startTime.split(':')
				startTime = int(h) * 3600 + int(m) * 60 + int(s)
		except:
			startTime = url[url.find('_t=') + 3:5]
			m, s = startTime.split(':')
			startTime = int(m) * 60 + int(s)
	else:
		startTime = 0

elif url[:20] == 'https://overcast.fm/':
	if url.count('/') > 3:
		startTime = url.rsplit('/', 1)[1]
		h, m, s = startTime.split(':')
		startTime = int(h) * 3600 + int(m) * 60 + int(s)
	else:
		startTime = 0

elif url[:20] == 'https://podcast.app/':
	if '#' in url:
		startTime = url.rsplit('#', 1)[1]
		h, m, s = startTime.split(':')
		startTime = int(h) * 3600 + int(m) * 60 + int(s)
	else:
		startTime = 0
elif url[:23] == 'https://www.podbean.com':
	if '#' in url:
		startTime = url.rsplit('#', 1)[1]
		h, m, s = startTime.split(':')
		startTime = int(h) * 3600 + int(m) * 60 + int(s)
	else:
		startTime = 0

elif url[:23] == 'https://radiopublic.com':
	if '#' in url:
		startTime = url.rsplit('#', 1)[1]
		h, m, s = startTime.split(':')
		startTime = int(h) * 3600 + int(m) * 60 + int(s)
	else:
		startTime = 0

elif url[:24] == 'https://deezer.page.link':
	if '#' in url:
		startTime = url.rsplit('#', 1)[1]
		h, m, s = startTime.split(':')
		startTime = int(h) * 3600 + int(m) * 60 + int(s)
	else:
		startTime = 0

elif url[:24] == 'https://www.stitcher.com':
	if '#' in url:
		startTime = url.rsplit('#', 1)[1]
		h, m, s = startTime.split(':')
		startTime = int(h) * 3600 + int(m) * 60 + int(s)
	else:
		startTime = 0

elif url[:25] == 'https://www.breaker.audio':
	if '#' in url:
		startTime = url.rsplit('#', 1)[1]
		h, m, s = startTime.split(':')
		startTime = int(h) * 3600 + int(m) * 60 + int(s)
	else:
		startTime = 0

elif url[:26] == 'https://castro.fm/episode/':
	if '#' in url:
		startTime = url.rsplit('#', 1)[1]
		if startTime.count(':') == 1:
			m, s = startTime.split(':')
			startTime = int(m) * 60 + int(s)
		else:
			h, m, s = startTime.split(':')
			startTime = int(h) * 3600 + int(m) * 60 + int(s)
	else:
		startTime = 0

elif url[:27] == 'https://podcasts.apple.com/':
	if '#' in url:
		startTime = url.rsplit('#', 1)[1]
		h, m, s = startTime.split(':')
		startTime = int(h) * 3600 + int(m) * 60 + int(s)
	else:
		startTime = 0

elif url[:27] == 'https://podcasts.google.com':
	if '#' in url:
		startTime = url.rsplit('#', 1)[1]
		h, m, s = startTime.split(':')
		startTime = int(h) * 3600 + int(m) * 60 + int(s)
	else:
		startTime = 0

clipDuration = int(sys.argv[2])
endTimestamp = sys.argv[3]
if clipDuration < 0:
	clipDuration = abs(clipDuration)
	startTime = startTime - clipDuration
if clipDuration == 0:
	h, m, s = endTimestamp.split(':')
	endTime = int(h) * 3600 + int(m) * 60 + int(s)
	if endTime > startTime:
		clipDuration = endTime - startTime
	else:
		clipDuration = startTime - endTime
		startTime = endTime
renderResolutionRatio = float(sys.argv[4])
videoFormat = sys.argv[5]
if videoFormat == 'square':
	fps = round(1100 / clipDuration, 2)
else:
	fps = round(700 / clipDuration, 2)
if fps > 20:
	fps = 20
colorTheme = sys.argv[6]

print('Getting metadata.')
req = urllib.request.Request(url)
req.add_header('User-Agent', ua)
with urllib.request.urlopen(req) as f:
	url_html = f.read().decode('utf-8')

soup = bs4.BeautifulSoup(url_html, 'html5lib')
if url[:15] == 'https://aca.st/':
	artworkUrl = 'http' + soup.find('meta', {'property': 'og:image'})['content'].rsplit('http', 1)[1]
	audioUrl = soup.find('meta', {'property': 'og:audio'})['content']
	podcastTitle = soup.find_all('h3')[1].find('span').string
	episodeTitle = soup.find('meta', {'property': 'og:title'})['content']
	episodeDate = ''

if url[:15] == 'https://pca.st/':
	artworkUrl = soup.find('div', id = 'artwork').find('img')['src']
	audioUrl = soup.find('audio')['src']
	episodeTitle = soup.find('h1').string
	podcastTitle = soup.find('title').string.replace(episodeTitle + ' - ', '')
	episodeDate = soup.find('div', id = 'episode_date').text.replace('  ', ' ').split(' ')
	episodeDate = episodeDate[2] + ' ' + episodeDate[1] + ', ' + episodeDate[3]

elif url[:18] == 'https://player.fm/':
	artworkUrl = soup.find('meta', {'property': 'og:image'})['content']
	audioUrl = soup.find('meta', {'name': 'twitter:player:stream'})['content'].replace('www.podtrac.com/pts/redirect.mp3/', '')
	episodeTitle = soup.find('meta', {'property': 'og:title'})['content']
	podcastTitle = soup.find('meta', {'property': 'og:site_name'})['content']
	episodeDate = soup.find('meta', {'property': 'og:updated_time'})['content'][:10]
	episodeDate = datetime.strptime(episodeDate, '%Y-%m-%d')
	episodeDate = episodeDate.strftime('%B %d, %Y')

elif url[:19] == 'https://castbox.fm/':
	artworkUrl = soup.find('meta', {'property': 'og:image'})['content']
	audioUrl = soup.find('audio').find('source')['src']
	episodeTitle = soup.find('meta', {'property': 'twitter:title'})['content']
	url_html = url_html.replace(',"name":"Channels"', '')
	podcastTitle = parse.unquote(url_html[url_html.find('","name":"') + 10:url_html.find('"', url_html.find('","name":"') + 10)])
	episodeDate = soup.find('span', {'class': 'item'}).text[-10:]
	episodeDate = datetime.strptime(episodeDate, '%Y-%m-%d')
	episodeDate = episodeDate.strftime('%B %d, %Y')

elif url[:20] == 'https://overcast.fm/':
	artworkUrl = soup.find('img', {'class': 'art fullart'})['src']
	audioUrl = soup.find('audio').find('source')['src']
	if '#' in audioUrl:
		audioUrl = audioUrl[:audioUrl.find('#')]
	episodeTitle = soup.find('h2').string
	podcastTitle = soup.find('h3').string
	episodeDate = soup.find('div', {'class': 'margintop0 lighttext'}).text.strip()

elif url[:20] == 'https://podcast.app/':
	artworkUrl = soup.find('div', {'class': 'logo'}).find('img')['src']
	audioUrl = soup.find('audio').find('source')['src']
	episodeTitle = soup.find('h1').string
	podcastTitle = soup.find('p', {'class': 'subs'}).find('a').string.strip()
	episodeDate = soup.find('p', {'class': 'subs'}).text.strip()[:10]
	episodeDate = datetime.strptime(episodeDate, '%m.%d.%Y')
	episodeDate = episodeDate.strftime('%B %d, %Y')

elif url[:23] == 'https://www.podbean.com':
	artworkUrl = soup.find('meta', {'property': 'og:image'})['content']
	audioUrl = soup.find('div', {'title': 'click to play'}).find('iframe')['src']
	audioUrl = parse.unquote(audioUrl[48:audioUrl.find('&', 48)]).replace('dts.podtrac.com/redirect.mp3/', '')
	podcastTitle = soup.find('div', {'class': 'pod-top'}).find('img')['alt']
	episodeTitle = soup.find('meta', {'property': 'og:title'})['content']
	episodeDate = soup.find('div', {'class': 'time'}).text.strip()
	episodeDate = datetime.strptime(episodeDate, '%Y-%m-%d')
	episodeDate = episodeDate.strftime('%B %d, %Y')

elif url[:23] == 'https://radiopublic.com':
	artworkUrl = soup.find('meta', {'property': 'og:image'})['content']
	audioUrl = parse.unquote(url_html[url_html.find('enclosureUrl\\":\\"') + 17:url_html.find('\\"', url_html.find('enclosureUrl\\":\\"') + 17)])
	podcastTitle = soup.find('title').string.rsplit('from ', 1)[1].replace(' on RadioPublic', '')
	episodeTitle = soup.find('title').string.replace(' from ' + podcastTitle + ' on RadioPublic', '')
	episodeDate = soup.find('time').text.split(' ')
	episodeDate = episodeDate[0] + ' ' + episodeDate[1].replace('st', '').replace('nd', '').replace('rd', '').replace('th', '') + ' ' + episodeDate[2]

elif url[:24] == 'https://deezer.page.link':
	artworkUrl = soup.find('meta', {'property': 'og:image'})['content']
	audioUrl = url_html[url_html.find('"EPISODE_DIRECT_STREAM_URL":"') + 29:url_html.find('"', url_html.find('"EPISODE_DIRECT_STREAM_URL":"') + 29)].replace('\\', '')
	podcastTitle = soup.find('meta', {'property': 'og:description'})['content']
	episodeTitle = soup.find('meta', {'property': 'og:title'})['content']
	episodeDate = url_html[url_html.find('"EPISODE_PUBLISHED_TIMESTAMP":"') + 31:url_html.find('"', url_html.find('"EPISODE_PUBLISHED_TIMESTAMP":"') + 31)]
	episodeDate = datetime.strptime(episodeDate, '%Y-%m-%d %H:%M:%S')
	episodeDate = episodeDate.strftime('%B %d, %Y')

elif url[:24] == 'https://www.stitcher.com':
	artworkUrl = soup.find('meta', {'name': 'twitter:image'})['content']
	audioUrl = url_html[url_html.find('F.audio_url="') + 13:url_html.find('"', url_html.find('F.audio_url="') + 13)].replace('\\u002F', '/').replace('www.podtrac.com/pts/redirect.mp3/', '')
	podcastTitle = soup.find('meta', {'name': 'twitter:image:alt'})['content']
	episodeTitle = soup.find('title').text.replace(podcastTitle + ' - ', '')[:-12]
	episodeDate = url_html[url_html.find(';F.date_published=') + 18:url_html.find(';', url_html.find(';F.date_published=') + 18)]
	episodeDate = datetime.fromtimestamp(int(episodeDate))
	episodeDate = episodeDate.strftime('%B %d, %Y')

elif url[:25] == 'https://www.breaker.audio':
	artworkUrl = soup.find('meta', {'name': 'twitter:image'})['content']
	audioUrl = soup.find('meta', {'name': 'twitter:player:stream'})['content']
	podcastTitle = soup.find('meta', {'name': 'twitter:image:alt'})['content'].replace(' artwork', '')
	episodeTitle = soup.find('title').string.replace(' - ' + podcastTitle + ' | Breaker', '')
	episodeDate = ''

elif url[:26] == 'https://castro.fm/episode/':
	artworkUrl = soup.find('div', id = 'artwork-container').find('img')['src']
	audioUrl = soup.find('audio').find('source')['src']
	episodeTitle = soup.find('h1').string
	podcastTitle = soup.find_all('h2')[0].string
	episodeDate = soup.find_all('h2')[1].string

elif url[:27] == 'https://podcasts.apple.com/':
	NOPRINT_LIST = {i: None for i in range(0, sys.maxunicode + 1) if not chr(i).isprintable()}
	episodeTitle = soup.find('h1').find('span', {'class': 'product-header__title'}).text.strip()
	episodeTitle = episodeTitle.translate(NOPRINT_LIST)
	podcastTitle = soup.find('h1').find('span', {'class': 'product-header__identity podcast-header__identity'}).text.strip()
	podcastId = url[url.find('/id') + 3:url.find('?', url.find('/id'))]
	
	req = urllib.request.Request('https://itunes.apple.com/lookup?id=' + podcastId)
	req.add_header('User-Agent', ua)
	with urllib.request.urlopen(req) as f:
		url_html = f.read().decode('utf-8')
	feedUrl = url_html[url_html.find('"feedUrl":"') + 11:url_html.find('"', url_html.find('"feedUrl":"') + 11)]
	
	req = urllib.request.Request(feedUrl)
	req.add_header('User-Agent', ua)
	with urllib.request.urlopen(req) as f:
		url_html = f.read().decode('utf-8')
	
	soup = bs4.BeautifulSoup(url_html, 'html5lib')
	artworkUrl = soup.find('itunes:image')['href']
	episodes = []
	for episode in soup.find_all('item'):
		try:
			iTunesTitle = episode.find('itunes:title').text.strip()
		except:
			iTunesTitle = ''
		metadata = { 
			'episodeTitle': episode.title.text.strip(),
			'iTunesTitle': iTunesTitle,
			'episodeDate': episode.pubdate.text.strip(),
			'audioUrl': episode.enclosure['url'],
		}   
		episodes.append(metadata)
	
	for episode in episodes:
		if (episode['iTunesTitle'] == episodeTitle) or (episodeTitle in episode['episodeTitle']):
			episodeTitle = episode['episodeTitle']
			episodeDate = episode['episodeDate']
			episodeDate = datetime.strptime(episodeDate, '%a, %d %b %Y %H:%M:%S %z')
			episodeDate = episodeDate.strftime('%B %d, %Y')
			audioUrl = episode['audioUrl']
			break

elif url[:27] == 'https://podcasts.google.com':
	mainDiv = soup.find('div', attrs={'jscontroller': True, 'jsmodel': True, 'jsdata': True, 'jsaction': True, 'jsname': True, 'class': True})
	artworkUrl = mainDiv.find('img')['src']
	audioUrl = mainDiv['jsdata'].split(';')[1]
	podcastTitle = soup.find('meta', {'itemprop': 'author'})['content']
	episodeTitle = soup.find('meta', {'property': 'og:title'})['content'][len(podcastTitle) + 3:]
	episodeDate = ''

print('Downloading artwork.')
req = urllib.request.Request(artworkUrl)
req.add_header('User-Agent', ua)
with urllib.request.urlopen(req) as f:
	artworkData = f.read()
filename, fileExt = os.path.splitext(artworkUrl)
artworkName = 'artwork' + fileExt
with open(artworkName, 'wb') as f:
	f.write(artworkData)

print('Downloading audio.')
req = urllib.request.Request(audioUrl)
req.add_header('User-Agent', ua)
with urllib.request.urlopen(req) as f:
	audioData = f.read()
filename, fileExt = os.path.splitext(audioUrl)
if '?' in fileExt:
	fileExt = fileExt.split('?')[0]
audioName = 'audio' + fileExt
with open(audioName, 'wb') as f:
	f.write(audioData)

if colorTheme == 'light':
	bgColor = '#fafafa'
	lightColor = '#060606'
	darkColor = '#777777'
	progressBarColor = '#dedede'
elif colorTheme =='dark':
	bgColor = '#0a0a0a'
	lightColor = '#dedede'
	darkColor = '#666666'
	progressBarColor = '#666666'
contrastColor = ColorThief(artworkName).get_color(quality = 1)

if videoFormat == 'square':
	W, H = 1400, 1400
	
	print('Generating frames.')
	for c in range(math.ceil(clipDuration * fps)):
	
		img = Image.new('RGB', (W, H), color = bgColor)
		
		artwork = Image.open(artworkName, 'r')
		artwork = artwork.resize((560, 560), Image.ANTIALIAS)
		w, h = artwork.size
		
		rad = 20
		circle = Image.new('L', (rad * 2, rad * 2), 0)
		draw = ImageDraw.Draw(circle)
		draw.ellipse((0, 0, rad * 2, rad * 2), fill = 255)
		alpha = Image.new('L', artwork.size, 255)
		alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
		alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
		alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
		alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
		img.paste(artwork, ((W - w) // 2, 140), alpha)
		
		episodeTitleFont = ImageFont.truetype('Helvetica', 55)
		podcastTitleFont = ImageFont.truetype('Helvetica', 50)
		timerFont = ImageFont.truetype('Helvetica', 50)
		
		d = ImageDraw.Draw(img)
		w, h = d.textsize(episodeTitle, font = episodeTitleFont)
		if w > 1000:
			mid = len(episodeTitle) // 2
			break_at = mid + min(-episodeTitle[mid::-1].index(' '), episodeTitle[mid:].index(' '), key = abs)
			w, h = d.textsize(episodeTitle[:break_at], font = episodeTitleFont)
			d.text(((W - w) // 2, 800), episodeTitle[:break_at], font = episodeTitleFont, fill = lightColor)
			w, h = d.textsize(episodeTitle[break_at:], font = episodeTitleFont)
			d.text(((W - w) // 2, 875), episodeTitle[break_at:], font = episodeTitleFont, fill = lightColor)
		else:
			d.text(((W - w) // 2, 845), episodeTitle, font = episodeTitleFont, fill = lightColor)
		w, h = d.textsize(podcastTitle, font = podcastTitleFont)
		d.text(((W - w) // 2, 1010), podcastTitle, font = podcastTitleFont, fill = darkColor)
		w, h = d.textsize(episodeDate, font = podcastTitleFont)
		d.text(((W - w) // 2, 1090), episodeDate, font = podcastTitleFont, fill = darkColor)
		
		progressBar = Image.new('RGB', (1100, 16), color = progressBarColor)
		img.paste(progressBar, (150, 1230))
		
		progressedBar = Image.new('RGB', (round((1100 / (clipDuration * fps)) * (c + 1)), 16), color = contrastColor)		
		img.paste(progressedBar, (150, 1230))
		
		end = Image.new('RGB', (16, 16), color = bgColor)
		circle = Image.new('L', (16, 16), 255)
		draw = ImageDraw.Draw(circle)
		draw.ellipse((0, 0, 16, 16), fill = 0)
		alpha = Image.new('L', end.size, 255)
		alpha.paste(circle.crop((0, 0, 8, 16)), (8, 0))
		img.paste(end, (142, 1230), alpha)
		img.paste(end, (1242, 1230), ImageOps.mirror(alpha))
		
		d = ImageDraw.Draw(img)
		w, h = d.textsize(strftime("%H:%M:%S", gmtime(round(startTime + (c / fps)))), font = timerFont)
		d.text((150, 1265), strftime("%H:%M:%S", gmtime(round(startTime + (c / fps)))), font = timerFont, fill = darkColor)
		
		d = ImageDraw.Draw(img)
		w, h = d.textsize('-' + strftime("%M:%S", gmtime(clipDuration - c)), font = timerFont)
		d.text((1250 - w, 1265), '-' + strftime("%M:%S", gmtime(round(clipDuration - (c / fps)))), font = timerFont, fill = darkColor)
		
		img = img.resize((math.ceil(round(W * renderResolutionRatio) / 2) * 2, round(H * renderResolutionRatio)), Image.ANTIALIAS)
		img.save('frames/frame_' + str(c).zfill(4) + '.bmp')

elif videoFormat == 'landscape':
	W, H = 1400, 600
	print('Generating frames.')
	for c in range(math.ceil(clipDuration * fps)):
	
		img = Image.new('RGB', (W, H), color = bgColor)
		
		artwork = Image.open(artworkName, 'r')
		artwork = artwork.resize((400, 400), Image.ANTIALIAS)
		w, h = artwork.size
		
		rad = 25
		circle = Image.new('L', (rad * 2, rad * 2), 0)
		draw = ImageDraw.Draw(circle)
		draw.ellipse((0, 0, rad * 2, rad * 2), fill = 255)
		alpha = Image.new('L', artwork.size, 255)
		alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
		alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
		alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
		alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
		img.paste(artwork, (100, 100), alpha)
		
		episodeTitleFont = ImageFont.truetype('Helvetica', 40)
		podcastTitleFont = ImageFont.truetype('Helvetica', 35)
		timerFont = ImageFont.truetype('Helvetica', 35)
		
		d = ImageDraw.Draw(img)
		w, h = d.textsize(episodeTitle, font = episodeTitleFont)
		if w > 700:
			mid = len(episodeTitle) // 2
			break_at = mid + min(-episodeTitle[mid::-1].index(' '), episodeTitle[mid:].index(' '), key = abs)
			w, h = d.textsize(episodeTitle[:break_at], font = episodeTitleFont)
			d.text((600 + ((700 - w) // 2), 130), episodeTitle[:break_at], font = episodeTitleFont, fill = lightColor)
			w, h = d.textsize(episodeTitle[break_at:], font = episodeTitleFont)
			d.text((600 + ((700 - w) // 2), 180), episodeTitle[break_at:], font = episodeTitleFont, fill = lightColor)
		else:
			d.text((600 + ((700 - w) // 2), 165), episodeTitle, font = episodeTitleFont, fill = lightColor)
		w, h = d.textsize(podcastTitle, font = podcastTitleFont)
		d.text((600 + ((700 - w) // 2), 260), podcastTitle, font = podcastTitleFont, fill = darkColor)
		w, h = d.textsize(episodeDate, font = podcastTitleFont)
		d.text((600 + ((700 - w) // 2), 310), episodeDate, font = podcastTitleFont, fill = darkColor)
		
		progressBar = Image.new('RGB', (700, 16), color = progressBarColor)
		img.paste(progressBar, (600, 410))
		
		progressedBar = Image.new('RGB', (round((700 / (clipDuration * fps)) * (c + 1)), 16), color = contrastColor)
		img.paste(progressedBar, (600, 410))
		
		end = Image.new('RGB', (16, 16), color = bgColor)
		circle = Image.new('L', (16, 16), 255)
		draw = ImageDraw.Draw(circle)
		draw.ellipse((0, 0, 16, 16), fill = 0)
		alpha = Image.new('L', end.size, 255)
		alpha.paste(circle.crop((0, 0, 8, 16)), (8, 0))
		img.paste(end, (592, 410), alpha)
		img.paste(end, (1292, 410), ImageOps.mirror(alpha))
		
		d = ImageDraw.Draw(img)
		w, h = d.textsize(strftime("%H:%M:%S", gmtime(round(startTime + (c / fps)))), font = timerFont)
		d.text((600, 440), strftime("%H:%M:%S", gmtime(round(startTime + (c / fps)))), font = timerFont, fill = darkColor)
		
		d = ImageDraw.Draw(img)
		w, h = d.textsize('-' + strftime("%M:%S", gmtime(clipDuration - c)), font = timerFont)
		d.text((1300 - w, 440), '-' + strftime("%M:%S", gmtime(round(clipDuration - (c / fps)))), font = timerFont, fill = darkColor)
		
		img = img.resize((math.ceil(round(W * renderResolutionRatio) / 2) * 2, round(H * renderResolutionRatio)), Image.ANTIALIAS)
		img.save('frames/frame_' + str(c).zfill(4) + '.bmp')

print('Merging frames.')
subprocess.call('ffmpeg -s ' + str(int(math.ceil(round(W * renderResolutionRatio) / 2) * 2)) + 'x' + str(int(round(H * renderResolutionRatio))) + ' -framerate ' + str(fps) + ' -patern_type glob -i "frames/*.bmp" -c:v libx264 -pix_fmt yuv420p video.mp4', stderr = subprocess.DEVNULL)
print('Trimming audio.')
subprocess.call('ffmpeg -ss ' + str(startTime) + ' -t ' + str(clipDuration) + ' -i ' + audioName + ' -map a trimmed.aac', stderr = subprocess.DEVNULL)
print('Exporting.')
subprocess.call('ffmpeg -i video.mp4 -i trimmed.aac -c copy -shortest podcast.mp4', stderr = subprocess.DEVNULL)
print('Cleaning up.')
subprocess.call('rm -rf frames')
subprocess.call('rm video.mp4')
subprocess.call('rm trimmed.aac')
subprocess.call('rm ' + audioName)
subprocess.call('rm ' + artworkName)
subprocess.call('play podcast.mp4')
subprocess.call('open podcast.mp4')
