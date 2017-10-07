import json
import logging
import re

import requests
import sys
from bs4 import BeautifulSoup, Comment
from docopt import docopt

l = logging.getLogger(__name__)

HELP = """
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
""" # noqa
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36' # noqa

# Download by search keyword or link


def download_by_keyword(keyword=None):
    '''
    Function called when user selects (1), meaning they are only providing
    the name of the anime. Calls private functions to gather request data,
    parse and normalize it, and offer storage services.
    '''
    if not keyword:
        anime_name = input("Enter the name of anime you wish to download from chia-anime.tv: ")  # noqa
    else:
        anime_name = keyword
    # Visiting search page for relevant animes
    search_url = "http://www.chia-anime.tv/search/" + anime_name
    # fetch response object for search page
    searchpage = requests.get(search_url)
    # parse the response object as HTML
    search_soup = BeautifulSoup((searchpage).text, "lxml")

    # Display search results
    search_counter = 1
    # An array to hold anime page links from searched results
    anime_page_links = []
    print("Search results: ")

    for x in search_soup.find_all(class_="title"):
        print(search_counter, x.a.text)
        anime_page_links.append(x.a['href'])
        search_counter += 1

    # No search results for the given keyword
    if len(anime_page_links) == 0:
        print("Nothing Found")
        download_by_keyword()

    # Select from search results
    search_index = int(input("Enter what you think is appropriate: "))
    anime_page_link = anime_page_links[search_index - 1]

    _download(anime_page_link, anime_name)


def download_by_link(link=None):
    '''
    Function called when user selects (2), meaning they are providing a link
    to the anime url page. Calls private functions to gather request data,
    parse and normalize it, and offer storage services.
    '''
    if not link:
        anime_page_link = input("Paste the link of the anime page: ")
    else:
        anime_page_link = link
    if anime_page_link[-1] == "/":
        anime_page_link = anime_page_link[:-1]

    anime_name = anime_page_link.split('/')[-1]

    _download(anime_page_link, anime_name)


def direct_download(anime_page_link, episode_range,
                    episode_quality, store_links):
    '''
    Function called when user selects (3), meaning they are providing a link,
    episode range (or single episode), episode quality.
    '''
    if not anime_page_link:
        "Please provide a link."
        exit(0)
    if not episode_range:
        "Please provide an episode range."
        exit(0)
    if not episode_quality:
        "Please provide quality required for downloading."
        exit(0)

    if anime_page_link[-1] == "/":
        anime_page_link = anime_page_link[:-1]
    anime_name = anime_page_link.split('/')[-1]
    print(anime_name)
    anime_episode_links = _get_episode_links(anime_page_link)
    if '-' in episode_range:
        try:
            episode_start, episode_end = [int(i) for i
                                          in episode_range.split('-')]
        except:
            print('Invalid episode range.')
            exit(0)
    else:
        try:
            episode_start = episode_end = int(episode_range)
        except:
            print("Invalid episode input.")
            exit(0)
    if not (episode_start > 0 and episode_end < len(anime_episode_links)):
            print('Invalid episode range.')
            exit(0)
    if episode_quality not in ['360p', '480p', '720p', '1080p']:
        print("Quality should be 360p, 480p, 720p, or 1080p")
        exit(0)
    episode_download = _get_animepremium_links(anime_episode_links,
                                               episode_start,
                                               episode_end, episode_quality)
    _store_results(anime_name, episode_download, True, store_links)


def _download(anime_page_link, anime_name):
    anime_episode_links = _get_episode_links(anime_page_link)
    episode_start, episode_end = _get_episode_range(anime_episode_links)
    episode_quality = _get_episode_quality()
    episode_download = _get_animepremium_links(anime_episode_links,
                                               episode_start,
                                               episode_end, episode_quality)
    _store_results(anime_name, episode_download)


def _store_results(anime_name, episode_download,
                   direct_store=False, store_links=False):
    '''
    Private function that stores the gathered download links
    '''
    optype = -1
    if not direct_store:
        optype = int(input(
            'Save links for later use (1) or download them now (2): '))
    if (direct_store and store_links) or optype == 1:
        with open(anime_name + ".txt", 'w') as f:
            for x in episode_download:
                f.write('{} \n\n'.format(x))
    elif (direct_store and not store_links) or optype == 2:
        # TODO: Code to download
        print("Code not yet implemented.")


def _get_animepremium_links(anime_episode_links, start, end, episode_quality):
    '''
    Private function that gets the animepremium download links
    '''
    episode_download = []
    episode_num = start
    alt_server_link_pattern = re.compile(
        "\$\(\"#downloader\"\).load\('(.*)'\)")
    for episode_page in anime_episode_links[start - 1:end]:
        episode_page_soup = BeautifulSoup(
            requests.get(episode_page,
                         headers={
                             "User-Agent": USER_AGENT,
                             "Referer": "http://chia-anime.tv"}).text, "lxml")
        for x in episode_page_soup.find_all(id="download"):
            animepremium_page_soup = BeautifulSoup(
                requests.get(x['href'],
                             headers={
                                 "User-Agent": USER_AGENT,
                                 "Referer": episode_page}).text, "lxml")
            available_qualities = {}
            for y in animepremium_page_soup.find_all(rel="nofollow"):
                if y.text in ['360p', '480p', '720p', '1080p']:
                    available_qualities.update({int(y.text[:-1]): y['href']})
            for script in animepremium_page_soup.find_all("script"):
                if "$(\"#downloader\")" in script.text:
                    alternate_server_link = re.findall(
                        alt_server_link_pattern, script.text)[0]
            alternate_server_soup = BeautifulSoup(
                requests.get(alternate_server_link,
                             headers={
                                 "User-Agent": USER_AGENT,
                                 "Referer": x['href']}).text, "lxml")
            alternate_server_link_soup = BeautifulSoup(
                ''.join(alternate_server_soup.find_all(
                    string=lambda text: isinstance(text, Comment))), "lxml")
            for i in alternate_server_link_soup.find_all(rel="nofollow"):
                available_qualities.update({int(i.text[:-1]): i['href']})
            _ep_quality = int(episode_quality[:-1])
            # Cause we want the next-highest quality
            for quality in reversed(sorted(available_qualities)):
                if _ep_quality >= quality:
                    episode_download.append(available_qualities[quality])
                    if _ep_quality > quality:
                        print(
                            ("WARNING: {0}p quality not available for episode #{1}. Using next-highest quality: {2}p.").format(  # noqa
                                _ep_quality, episode_num, quality))
                    break
        episode_num += 1
    return episode_download


def _get_episode_links(anime_page_link):
    '''
    Private function that aggregates episode links
    '''
    # list to store episode links scraped from anime page
    anime_episode_links = []
    animepagesoup = BeautifulSoup((requests.get(anime_page_link)).text, "lxml")
    for x in animepagesoup.find_all('h3'):
        anime_episode_links.append(x.a['href'])
    # Reverse the links array since chia-anime stores links in reverse order
    anime_episode_links.reverse()
    return anime_episode_links


def _get_episode_range(anime_episode_links):
    '''
    Private function that gets the range of episodes
    '''
    while (True):
        episode_start = int(input('Entering starting episode: '))
        episode_end = int(input('Enter ending episode: '))
        if not (episode_start > 0 and episode_end < len(anime_episode_links)):
            print('Invalid episode selection, try again.')
        else:
            break
    return episode_start, episode_end


def _get_episode_quality():
    '''
    Private function that gets the episode quality based on user input
    '''
    while (True):
        quality = input(
            'Enter the quality of the episode (360p, 480p, 720p, 1080p): ')
        if quality in ['360p', '480p', '720p', '1080p']:
            break
        else:
            print('Invalid quality input, try again.')
    return quality


def main():
    # Download by link or by name ?
    choice = int(input(
        "Enter (1) to search anime or (2) to download from link: "))

    if choice == 1:
        download_by_keyword()
    else:
        download_by_link()


def command_line_runner():
    opts = docopt(HELP, argv=sys.argv[1:])
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
        level=logging.DEBUG if opts['--verbose'] else logging.ERROR)
    l.debug("Arguments %s", json.dumps(opts))
    if (opts["search"] or opts["-s"]) and len(opts["<keyword>"]) > 0:
        # User wants to search and provide a keyword
        download_by_keyword(keyword=opts["<keyword>"])
    elif (opts["download"] or opts["-d"]) and len(opts["<link>"]) > 0:
        # User provide a link to download
        download_by_link(link=opts["<link>"])
    elif (opts['interactive'] or opts["-i"]):
        main()
    elif ((opts['direct'] or opts["-D"]) and len(opts["<link>"]) > 0 and
          len(opts["<episode-range>"]) and len(opts["<quality>"])):
        store_links = True if opts['--store-links'] else False
        direct_download(opts["<link>"], opts["<episode-range>"],
                        opts["<quality>"], store_links)


if __name__ == '__main__':
    command_line_runner()
