import os
import bs4
import sys
import math
import subprocess
import urllib.request
from urllib import parse
from colorthief import ColorThief
from time import gmtime, strftime
from PIL import Image, ImageDraw, ImageFont, ImageOps

subprocess.call('rm podcast.mp4', stderr = subprocess.DEVNULL)
subprocess.call('mkdir frames', stderr = subprocess.DEVNULL)

url = sys.argv[1]
try:
	startTime = int(float(parse.parse_qs(parse.urlparse(url).query)['t'][0]))
except:
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
fps = round(700 / clipDuration, 2)
if fps > 20:
	fps = 20
resolution = int(sys.argv[4])

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'

print('Getting metadata.')
req = urllib.request.Request(url)
req.add_header('User-Agent', ua)
with urllib.request.urlopen(req) as f:
	url_html = f.read().decode('utf-8')

soup = bs4.BeautifulSoup(url_html, 'html5lib')
artworkUrl = soup.find('div', id='artwork').find('img')['src']
audioUrl = soup.find('audio')['src']
episodeTitle = soup.find('title').string.split(' - ')[0]
podcastTitle = soup.find('title').string.split(' - ')[1]

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

bgColor = '#0a0a0a'
lightGreyColor = '#dedede'
darkGreyColor = '#666666'
mainColor = ColorThief(artworkName).get_color(quality = 1)

W, H = 1000, 1000

print('Generating frames.')
for c in range(math.ceil(clipDuration * fps)):

	img = Image.new('RGB', (W, H), color = bgColor)
	
	artwork = Image.open(artworkName, 'r')
	artwork.thumbnail((370, 370), Image.ANTIALIAS)
	w, h = artwork.size
	
	rad = 15
	circle = Image.new('L', (rad * 2, rad * 2), 0)
	draw = ImageDraw.Draw(circle)
	draw.ellipse((0, 0, rad * 2, rad * 2), fill = 255)
	alpha = Image.new('L', artwork.size, 255)
	alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
	alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
	alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
	alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
	img.paste(artwork, ((W - w) // 2, 150), alpha)
	
	episodeTitleFont = ImageFont.truetype('Helvetica', 35)#Arial Rounded MT Bold
	podcastTitleFont = ImageFont.truetype('Helvetica', 30)
	d = ImageDraw.Draw(img)
	w, h = d.textsize(episodeTitle, font = episodeTitleFont)
	d.text(((W - w) // 2, 630), episodeTitle, font = episodeTitleFont, fill = lightGreyColor)
	w, h = d.textsize(podcastTitle, font = podcastTitleFont)
	d.text(((W - w) // 2, 700), podcastTitle, font = podcastTitleFont, fill = darkGreyColor)
	
	progressBar = Image.new('RGB', (700, 10), color = darkGreyColor)
	progressBarLeft = Image.new('RGB', (50, 100), color = bgColor)
	draw = ImageDraw.Draw(progressBarLeft)
	draw.pieslice((0, 0, 100, 100), start = 90, end = 270, fill = darkGreyColor)
	progressBarLeft.thumbnail((10, 10), Image.ANTIALIAS)
	progressBarRight = ImageOps.mirror(progressBarLeft)
	
	img.paste(progressBar, (150, 820))
	img.paste(progressBarLeft, (150, 820))
	img.paste(progressBarRight, (845, 820))
	
	progressedBar = Image.new('RGB', (round((700 / (clipDuration * fps)) * (c + 1)), 10), color = mainColor)
	progressedBarLeft = Image.new('RGB', (50, 100), color = bgColor)
	draw = ImageDraw.Draw(progressedBarLeft)
	draw.pieslice((0, 0, 100, 100), start = 90, end = 270, fill = mainColor)
	progressedBarLeft.thumbnail((10, 10), Image.ANTIALIAS)
	
	progressedBarRight = Image.new('RGB', (50, 100), color = darkGreyColor)
	draw = ImageDraw.Draw(progressedBarRight)
	draw.pieslice((0, 0, 100, 100), start = 90, end = 270, fill = mainColor)
	progressedBarRight.thumbnail((10, 10), Image.ANTIALIAS)
	progressedBarRight = ImageOps.mirror(progressedBarRight)
	
	img.paste(progressedBar, (150, 820))
	img.paste(progressedBarLeft, (150, 820))
	img.paste(progressedBarRight, (150 + round((700 / (clipDuration * fps)) * (c + 1)), 820))
	
	timerFont = ImageFont.truetype('Helvetica', 27)
	d = ImageDraw.Draw(img)
	w, h = d.textsize(strftime("%H:%M:%S", gmtime(round(startTime + (c / fps)))), font = timerFont)
	d.text((150, 840), strftime("%H:%M:%S", gmtime(round(startTime + (c / fps)))), font = timerFont, fill = darkGreyColor)
	
	d = ImageDraw.Draw(img)
	w, h = d.textsize(strftime("%M:%S", gmtime(clipDuration - c)), font = timerFont)
	d.text((850 - w, 840), strftime("%M:%S", gmtime(round(clipDuration - (c / fps)))), font = timerFont, fill = darkGreyColor)
	
	img = img.resize((resolution, resolution), Image.ANTIALIAS)
	# img.show()
	img.save('frames/frame_' + str(c).zfill(4) + '.bmp')

print('Merging frames.')
subprocess.call('ffmpeg -s ' + str(resolution) + 'x' + str(resolution) + ' -framerate ' + str(fps) + ' -i frames/frame_%04d.bmp -c:v libx264 -pix_fmt yuv420p video.mp4', stderr = subprocess.DEVNULL)
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
