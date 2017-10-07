# chia-anime-downloader

Anime batch downloader for [chia-anime](https://chia-anime.tv)



### Features :
1. Search animes using the website search tool.
2. Generate download links and save in text files for later use.
3. Download using terminal (In Progress)


### Installation
1. `git clone https://github.com/anshumanv/chia-anime-downloader.git`
2. `cd chia-anime-downloader`
3. `python setup.py install`

### Usage :
1. `chia_anime_downloader` OR `python chia_anime_downloader.py` if you don't follow the installation guide OR Simply run the .bat file.  
2. Follow the onscreen instructions


### Issues/Problems :
1. Not able to grab links from pages which don't have resolution selector or contains japanese characters.
2. Need to add a check for verifying whether chosen quality is available or not and handle the unavailability scenarios.


#### Dependencies :
1. Requests
2. BeautifulSoup4

Run `pip install -r requirements.txt` for installing dependencies.
  
* PR's are well appreciated.

## License

MIT © [Anshuman Verma](https://twitter.com/Anshumaniac12)
