import requests
from bs4 import BeautifulSoup

choice = int(input("Enter (1) to search anime or (2) to download from link: ")) # Download by link or by name ?

# Download by search keyword or link

def download_by_keyword():
	'''
	Function called when user selects (1), meaning they are only providing the name of the
	anime. Calls private functions to gather request data, parse and normalize it, and 
	offer storage services. 
	'''
	anime_name = input("Enter the name of anime you wish to download from chia-anime.tv: ")
	search_url = "http://www.chia-anime.tv/search/"+anime_name	#Visiting search page for relevant animes
	searchpage = requests.get(search_url)	#fetch response object for search page
	search_soup = BeautifulSoup((searchpage).text,"lxml")	#parse the response object as HTML
	
	#Display search results
	search_counter = 1
	anime_page_links = []	# An array to hold anime page links from searched results
	print("Search results:")
	
	for x in search_soup.find_all(class_="title"):
		print(search_counter,x.a.text)
		anime_page_links.append(x.a['href'])
		search_counter+=1

	# No search results for the given keyword
	if len(anime_page_links) == 0:
		print("Nothing Found")
		exit(0)
		
	#Select from search results
	search_index = int(input("Enter what you think is appropriate: "))
	anime_page_link = anime_page_links[search_index-1]
	
	anime_episode_links = _get_episode_links(anime_page_link)
	
	episode_start, episode_end = _get_episode_range(anime_episode_links)
	
	episode_quality = _get_episode_quality()
	
	episode_download = _get_animepremium_links(anime_episode_links, episode_start, episode_end, episode_quality)
	
	_store_results(anime_name, episode_download)

def download_by_link():
	'''
	Function called when user selects (2), meaning they are providing a link to the anime
	url page. Calls private functions to gather request data, parse and normalize it, and 
	offer storage services. 
	'''
	anime_page_link = input("Paste the link of the anime page:")
	
	anime_name = anime_page_link.split('/')[-2]
	
	anime_episode_links = _get_episode_links(anime_page_link)
	
	episode_start, episode_end = _get_episode_range(anime_episode_links)
	
	episode_quality = _get_episode_quality()
	
	episode_download = _get_animepremium_links(anime_episode_links, episode_start, episode_end, episode_quality)
	
	_store_results(anime_name, episode_download)

def _store_results(anime_name, episode_download):
	'''
	Private function that stores the gathered download links
	'''
	optype = int(input('Save links for later use (1) or download them now (2):'))
	if optype == 1:
		with open(anime_name+".txt",'w') as f:
			for x in episode_download:
				f.write('{} \n\n'.format(x))


def _get_animepremium_links(anime_episode_links, start, end, episode_quality):
	'''
	Private function that gets the animepremium download links
	'''
	episode_download = [] 
	for episode_page in anime_episode_links[start-1:end]:
		episode_page_soup = BeautifulSoup(requests.get(episode_page).text,"lxml")
		for x in episode_page_soup.find_all(id="download"):
			animepremium_page_soup = BeautifulSoup((requests.get(x['href'])).text,"lxml")
			for y in animepremium_page_soup.find_all(rel="nofollow"):
				if(y.text==episode_quality):
					episode_download.append(y['href'])
	return episode_download

def _get_episode_links(anime_page_link):
	'''
	Private function that aggregates episode links
	'''
	anime_name = anime_page_link.split('/')[-2] # get second last item
	anime_episode_links = []	# list to store episode links scraped from anime page
	animepagesoup = BeautifulSoup((requests.get(anime_page_link)).text,"lxml")
	for x in animepagesoup.find_all('h3'):
		anime_episode_links.append(x.a['href'])
	anime_episode_links.reverse()	# Reverse the links array since chia-anime stores links in reverse order
	return anime_episode_links
	
def _get_episode_range(anime_episode_links):
	'''
	Private function that gets the range of episodes
	'''
	while(True):
		episode_start = int(input('Entering starting episode:'))
		episode_end = int(input('Enter ending episode:'))
		if(episode_start > 0 and episode_start < len(anime_episode_links) and episode_end >= 1 and episode_end <= len(anime_episode_links) and episode_start <= episode_end):
			break
		else:
			print('Invalid episode selection, try again.')
	return episode_start, episode_end

def _get_episode_quality():
	'''
	Private function that gets the episode quality based on user input
	'''
	while(True):
		quality = input('Enter the quality of the episode (360p, 480p, 720p, 1080p):')
		if quality in ['360p', '480p', '720p', '1080p']:
			break
		else:
			print('Invalid quality input, try again.')
	return quality

if choice==1:
	download_by_keyword()
else:
	download_by_link()
