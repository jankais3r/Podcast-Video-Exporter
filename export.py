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
renderResolutionRatio = float(sys.argv[4])
videoFormat = int(sys.argv[5])

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
episodeDate = soup.find('div', id='episode_date').text.replace('  ', ' ').split(' ')
episodeDate = episodeDate[2] + ' ' + episodeDate[1] + ', ' + episodeDate[3]

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
lightColor = '#dedede'
darkColor = '#666666'
contrastColor = ColorThief(artworkName).get_color(quality = 1)

if videoFormat == 1:
	W, H = 1000, 1000
	
	print('Generating frames.')
	for c in range(math.ceil(clipDuration * fps)):
	
		img = Image.new('RGB', (W, H), color = bgColor)
		
		artwork = Image.open(artworkName, 'r')
		artwork = artwork.resize((400, 400), Image.ANTIALIAS)
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
		img.paste(artwork, ((W - w) // 2, 100), alpha)
		
		episodeTitleFont = ImageFont.truetype('Helvetica', 38)
		podcastTitleFont = ImageFont.truetype('Helvetica', 32)
		timerFont = ImageFont.truetype('Helvetica', 32)
		
		d = ImageDraw.Draw(img)
		w, h = d.textsize(episodeTitle, font = episodeTitleFont)
		d.text(((W - w) // 2, 600), episodeTitle, font = episodeTitleFont, fill = lightColor)
		w, h = d.textsize(podcastTitle, font = podcastTitleFont)
		d.text(((W - w) // 2, 680), podcastTitle, font = podcastTitleFont, fill = darkColor)
		w, h = d.textsize(episodeDate, font = podcastTitleFont)
		d.text(((W - w) // 2, 740), episodeDate, font = podcastTitleFont, fill = darkColor)
		
		progressBar = Image.new('RGB', (800, 16), color = darkColor)
		progressBarLeft = Image.new('RGB', (80, 160), color = bgColor)
		draw = ImageDraw.Draw(progressBarLeft)
		draw.pieslice((0, 0, 160, 160), start = 90, end = 270, fill = darkColor)
		progressBarLeft.thumbnail((16, 16), Image.ANTIALIAS)
		progressBarRight = ImageOps.mirror(progressBarLeft)
		
		img.paste(progressBar, (100, 840))
		img.paste(progressBarLeft, (100, 840))
		img.paste(progressBarRight, (895, 840))
		
		progressedBar = Image.new('RGB', (round((800 / (clipDuration * fps)) * (c + 1)), 16), color = contrastColor)
		progressedBarLeft = Image.new('RGB', (80, 160), color = bgColor)
		draw = ImageDraw.Draw(progressedBarLeft)
		draw.pieslice((0, 0, 160, 160), start = 90, end = 270, fill = contrastColor)
		progressedBarLeft.thumbnail((16, 16), Image.ANTIALIAS)
		
		if c + 1 == math.ceil(clipDuration * fps):
			progressedBarRight = Image.new('RGB', (80, 160), color = bgColor)
		else:
			progressedBarRight = Image.new('RGB', (80, 160), color = darkColor)
		draw = ImageDraw.Draw(progressedBarRight)
		draw.pieslice((0, 0, 160, 160), start = 90, end = 270, fill = contrastColor)
		progressedBarRight.thumbnail((16, 16), Image.ANTIALIAS)
		progressedBarRight = ImageOps.mirror(progressedBarRight)
		
		img.paste(progressedBar, (100, 840))
		img.paste(progressedBarLeft, (100, 840))
		img.paste(progressedBarRight, (100 + round((800 / (clipDuration * fps)) * (c + 1)), 840))
		
		d = ImageDraw.Draw(img)
		w, h = d.textsize(strftime("%H:%M:%S", gmtime(round(startTime + (c / fps)))), font = timerFont)
		d.text((100, 870), strftime("%H:%M:%S", gmtime(round(startTime + (c / fps)))), font = timerFont, fill = darkColor)
		
		d = ImageDraw.Draw(img)
		w, h = d.textsize('-' + strftime("%M:%S", gmtime(clipDuration - c)), font = timerFont)
		d.text((900 - w, 870), '-' + strftime("%M:%S", gmtime(round(clipDuration - (c / fps)))), font = timerFont, fill = darkColor)
		
		img = img.resize((math.ceil(round(W * renderResolutionRatio) / 2) * 2, round(H * renderResolutionRatio)), Image.ANTIALIAS)
		# img.show()
		img.save('frames/frame_' + str(c).zfill(4) + '.bmp')

elif videoFormat == 2:
	W, H = 1778, 1000
	print('Generating frames.')
	for c in range(math.ceil(clipDuration * fps)):
	
		img = Image.new('RGB', (W, H), color = bgColor)
		
		artwork = Image.open(artworkName, 'r')
		artwork = artwork.resize((600, 600), Image.ANTIALIAS)
		w, h = artwork.size
		
		rad = 35
		circle = Image.new('L', (rad * 2, rad * 2), 0)
		draw = ImageDraw.Draw(circle)
		draw.ellipse((0, 0, rad * 2, rad * 2), fill = 255)
		alpha = Image.new('L', artwork.size, 255)
		alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
		alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
		alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
		alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
		img.paste(artwork, (100, 200), alpha)
		
		episodeTitleFont = ImageFont.truetype('Helvetica', 42)
		podcastTitleFont = ImageFont.truetype('Helvetica', 38)
		timerFont = ImageFont.truetype('Helvetica', 38)
		
		d = ImageDraw.Draw(img)
		w, h = d.textsize(episodeTitle, font = episodeTitleFont)
		d.text((800 + ((878 - w) // 2), 360), episodeTitle, font = episodeTitleFont, fill = lightColor)
		w, h = d.textsize(podcastTitle, font = podcastTitleFont)
		d.text((800 + ((878 - w) // 2), 460), podcastTitle, font = podcastTitleFont, fill = darkColor)
		w, h = d.textsize(episodeDate, font = podcastTitleFont)
		d.text((800 + ((878 - w) // 2), 520), episodeDate, font = podcastTitleFont, fill = darkColor)
		
		progressBar = Image.new('RGB', (878, 16), color = darkColor)
		progressBarLeft = Image.new('RGB', (80, 160), color = bgColor)
		draw = ImageDraw.Draw(progressBarLeft)
		draw.pieslice((0, 0, 160, 160), start = 90, end = 270, fill = darkColor)
		progressBarLeft.thumbnail((16, 16), Image.ANTIALIAS)
		progressBarRight = ImageOps.mirror(progressBarLeft)
		
		img.paste(progressBar, (800, 650))
		img.paste(progressBarRight, (1670, 650))
		
		progressedBar = Image.new('RGB', (round((870 / (clipDuration * fps)) * (c + 1)), 16), color = contrastColor)
		progressedBarLeft = Image.new('RGB', (80, 160), color = bgColor)
		draw = ImageDraw.Draw(progressedBarLeft)
		draw.pieslice((0, 0, 160, 160), start = 90, end = 270, fill = contrastColor)
		progressedBarLeft.thumbnail((16, 16), Image.ANTIALIAS)
		
		if c + 1 == math.ceil(clipDuration * fps):
			progressedBarRight = Image.new('RGB', (80, 160), color = bgColor)
		else:
			progressedBarRight = Image.new('RGB', (80, 160), color = darkColor)
		draw = ImageDraw.Draw(progressedBarRight)
		draw.pieslice((0, 0, 160, 160), start = 90, end = 270, fill = contrastColor)
		progressedBarRight.thumbnail((16, 16), Image.ANTIALIAS)
		progressedBarRight = ImageOps.mirror(progressedBarRight)
		
		img.paste(progressedBar, (800, 650))
		img.paste(progressedBarLeft, (800, 650))
		img.paste(progressedBarRight, (800 + round((870 / (clipDuration * fps)) * (c + 1)), 650))
		
		d = ImageDraw.Draw(img)
		w, h = d.textsize(strftime("%H:%M:%S", gmtime(round(startTime + (c / fps)))), font = timerFont)
		d.text((800, 680), strftime("%H:%M:%S", gmtime(round(startTime + (c / fps)))), font = timerFont, fill = darkColor)
		
		d = ImageDraw.Draw(img)
		w, h = d.textsize('-' + strftime("%M:%S", gmtime(clipDuration - c)), font = timerFont)
		d.text((1678 - w, 680), '-' + strftime("%M:%S", gmtime(round(clipDuration - (c / fps)))), font = timerFont, fill = darkColor)
		
		img = img.resize((math.ceil(round(W * renderResolutionRatio) / 2) * 2, round(H * renderResolutionRatio)), Image.ANTIALIAS)
		# img.show()
		img.save('frames/frame_' + str(c).zfill(4) + '.bmp')

print('Merging frames.')
subprocess.call('ffmpeg -s ' + str(int(math.ceil(round(W * renderResolutionRatio) / 2) * 2)) + 'x' + str(int(round(H * renderResolutionRatio))) + ' -framerate ' + str(fps) + ' -i frames/frame_%04d.bmp -c:v libx264 -pix_fmt yuv420p video.mp4', stderr = subprocess.DEVNULL)
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
