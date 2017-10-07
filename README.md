# chia-anime-downloader

Anime batch downloader for [chia-anime](https://chia-anime.tv). Supports downloading with varying qualities and can download episode ranges.

### Features :
1. Search animes using the website search tool.
2. Generate download links and save in text files for later use.
3. Download using terminal (In Progress)

### Installation

1. `git clone https://github.com/anshumanv/chia-anime-downloader.git`
2. `cd chia-anime-downloader`
3. `python setup.py install` (_May require admin privileges on Windows or_ `sudo` _in Linux/Mac_)

### Usage :

1. `python chia_anime_downloader.py` from the `chia-anime-downloader` directory. **(All OS)**
   *OR*
1. `chia_anime_downloader` from any directory. **(Linux and Mac, only if step 3 is done in installation)**
2. Follow the onscreen instructions. See below for available options -

```
Usage: chia-anime-downloader.py (search | -s) <keyword> [options]
       chia-anime-downloader.py (download | -d) <link> [options]
       chia-anime-downloader.py (direct | -D) <link> <episode-range> <quality> [options]
       chia-anime-downloader.py (interactive | -i) [options]

Options:
    -h --help          Show this help message and exit
    -v, --verbose      Print debug logging
    -l, --store-links  Using this option will store links instead of downloading. ONLY FOR DIRECT DOWNLOADING.

Arguments:
    keyword           Anime keyword/name to search
    link              Link to anime page on chia-anime.tv
    episode-range     Range of episodes(Example: 1-8) or a single episode(Example: 12)
    quality           Quality of episodes to be downloaded. Must be one of the following: 360p, 480p, 720p, 1080p.
```

### Issues/Problems :
1. Not able to grab links from pages which don't have resolution selector or contains japanese characters.
2. Need to add a check for verifying whether chosen quality is available or not and handle the unavailability scenarios.

#### Dependencies :
1. Requests
2. BeautifulSoup4
3. LXML
4. Docopts

Run `pip install -r requirements.txt` for installing dependencies.
  
* PR's are well appreciated.

## License

MIT © [Anshuman Verma](https://twitter.com/Anshumaniac12)
