import requests
from bs4 import BeautifulSoup

choice = int(input("Enter 1 to search anime or 2 to download from link")) # Download by link or by name ?

# Download by search keyword
if choice==1:
	animename = input("Enter the name of anime you wish to download from chia-anime.tv ")
	search_url = "http://www.chia-anime.tv/search/"+animename	#Visiting search page for relevant animes
	searchpage = requests.get(search_url)	#fetch response object for search page
	search_soup = BeautifulSoup((searchpage).text,"lxml")	#parse the response object as HTML

	#Display search results
	search_counter = 1
	anime_page_links = []	# An array to hold anime page links from searched results
	print("Search results are as follows")
	for x in search_soup.find_all(class_="title"):
		print(search_counter,x.a.text)
		anime_page_links.append(x.a['href'])
		search_counter+=1

	# No search results for the given keyword
	if len(anime_page_links)==0:
		print("Nothing Found")
		exit(0)

	#Select from search results
	search_index = int(input("Enter what you think is appropriate: "))
	anime_page_link = anime_page_links[search_index-1]

else:
	anime_page_link = input("Paste the the link of anime page ")


print(anime_page_link)
anime_name = anime_page_link.split('/')[-2]
anime_episode_links = []	# list to store episode links scraped from anime page
animepagesoup = BeautifulSoup((requests.get(anime_page_link)).text,"lxml")
for x in animepagesoup.find_all('h3'):
	anime_episode_links.append(x.a['href'])

anime_episode_links.reverse()	# Reverse the links array since chia-anime stores links in reverse order

#print(anime_episode_links)

print("\n\nEnter the starting and ending episodes\n")
while(1):
	start = int(input("\nEnter starting episode: "))
	end = int(input("\nEnter ending episode: "))
	if(start>0 and start < len(anime_episode_links) and end>=1 and end<=len(anime_episode_links) and start<=end):
		break

#print(anime_episode_links[start-1:end])

while(1):
	quality = input("\n\nEnter the quality from 360p, 480p, 720p, 1080p : ")
	if(quality in {'360p', '480p', '720p', '1080p'}):
		break
	else: print("Invalid Quality")


# Grab animepremium links
episode_download = [] 
for episode_page in anime_episode_links[start-1:end]:
	episode_page_soup = BeautifulSoup(requests.get(episode_page).text,"lxml")
	for x in episode_page_soup.find_all(id="download"):
		#print(x['href'])
		animepremium_page_soup = BeautifulSoup((requests.get(x['href'])).text,"lxml")
		for y in animepremium_page_soup.find_all(rel="nofollow"):
			if(y.text==quality):
				episode_download.append(y['href'])

#print(episode_download)


# Handle the links
optype = int(input("\n\nSave the download links for later use (1) or download them now (2) ?\n"))

if optype == 1:
	with open(anime_name+".txt",'w') as f:
		for x in episode_download:
			f.write('{} \n\n'.format(x))


