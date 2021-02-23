# PocketCasts Video Exporter
This Shortcut and Python script combo allows to render excerpts of podcasts as videos to be shared online, e.g. on Twitter.

See it in action [here](https://twitter.com/jankais3r/status/1363887846784917507).


## Required apps
- [Pocket Casts](https://apps.apple.com/us/app/pocket-casts/id414834813)
- [a-shell](https://apps.apple.com/us/app/a-shell/id1473805438)

### Shortcuts setup
- Install the following shortcut: [iCloud Link](https://www.icloud.com/shortcuts/64fa0bddb6a14e90a29820c79f3143da)

### a-shell setup
- Install Python dependencies
```
pip install colorthief
pip install beautifulsoup4
```
- [Download](https://github.com/holzschu/a-Shell-commands/releases/tag/0.1) a pre-built `ffmpeg.wasm` binary and put it into `$HOME/Documents/bin/`
- Put `export.py` from this repo into `$HOME/Documents/`

![Demo](https://github.com/jankais3r/PocketCasts-Video-Exporter/blob/main/demo.png)

## To-do
- [x] Initial release
- [x] Landscape video format
- [ ] Color themes
