# Podcast Video Exporter
This Shortcut and Python script combo allows you to export podcast excerpts as videos to be shared online, e.g. on Twitter.

See it in action [here](https://twitter.com/jankais3r/status/1363887846784917507).

![Demo](https://github.com/jankais3r/Podcast-Video-Exporter/blob/main/demo.png)

## Required apps
- [a-shell](https://apps.apple.com/us/app/a-shell/id1473805438)
- Any of the supported podcast apps:
  - [Apple Podcasts](https://apps.apple.com/us/app/apple-podcasts/id525463029)
  - [Pocket Casts](https://apps.apple.com/us/app/pocket-casts/id414834813)
  - [Castro](https://apps.apple.com/us/app/castro-podcast-player/id1080840241)
  - [Overcast](https://apps.apple.com/us/app/overcast/id888422857)
  - [Stitcher](https://apps.apple.com/us/app/stitcher-for-podcasts/id288087905)
  - [Google Podcasts](https://apps.apple.com/us/app/google-podcasts/id1398000105)
  - [Deezer](https://apps.apple.com/us/app/deezer-music-podcast-player/id292738169)
  - [Castbox](https://apps.apple.com/us/app/castbox-podcast-player/id1243410543)
  - [The Podcast App](https://apps.apple.com/us/app/the-podcast-app/id1199070742)
  - [Player FM](https://apps.apple.com/us/app/player-fm-podcast-app/id940568467)
  - [Breaker](https://apps.apple.com/us/app/breaker-the-social-podcast-app/id1215095006)
  - [Acast](https://apps.apple.com/us/app/acast-podcast-player/id925311796)
  - [RadioPublic](https://apps.apple.com/us/app/radiopublic-the-podcast-app/id1113752736)
  - [Podbean](https://apps.apple.com/us/app/podbean-podcast-app-player/id973361050)

### Shortcuts setup
- Install the following shortcut: [iCloud Link](https://www.icloud.com/shortcuts/6de71570cb6b44248ab981ca336e52e6)

The maximum export resolution is 1400x1400 for the square video format, and 1400x600 for the landscape video format. The default resolution is half that (700x700 and 700x300). Increasing the resolution increases the time it takes to generate the video.

To change the video resolution, edit this part of the Shortcut:
![Resolution](https://github.com/jankais3r/Podcast-Video-Exporter/blob/main/resolution.jpg)

### a-shell setup
- Install Python dependencies
```
pip install colorthief
pip install beautifulsoup4
```
- [Download](https://github.com/holzschu/a-Shell-commands/releases/tag/0.1) a pre-built `ffmpeg.wasm` binary and put it into `$HOME/Documents/bin/`
- Put `export.py` from this repo into `$HOME/Documents/`

## To-do
- [x] Initial release
- [x] Landscape video format
- [x] Color themes
