import requests
from bs4 import BeautifulSoup

choice = int(input("Enter 1 to search anime or 2 to download from link")) #Download by link or by name ?

#Download by name
if choice==1:
	animename = input("Enter the name of anime you wish to download from chia-anime.tv ")
	search_url = "http://www.chia-anime.tv/search/"+animename	#Visiting search page for relevant animes
	searchpage = requests.get(search_url)	#fetch response object for search page
	search_soup = BeautifulSoup(searchpage.text,"lxml")	#parse the response object as HTML

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
	search_index = int(input("Enter what you think is appropriate"))
	anime_link = anime_page_links[search_index-1]
	print(anime_link) 

else:
	anime_link = input("Paste the the link of anime page ")

