#!/usr/bin/python3.2
#Author: reddit_coder
#This software is under GPLv3, this is free to distribute, change and use.

import urllib.request as url
import json
import webbrowser
from time import sleep

handle = webbrowser.get()
try:	#self explanatory
	#subreddit = input("Please enter the subreddit you would like to look through: ")

	genre = input("Please enter what you are looking for: ").lower()

	pages = int(input("How many pages back do you want to look through?"))
except:
	print("Invalid input. Did you accidentally type a non-number for the page count?")

hdr = {'User-Agent' : 'genre parser by reddit_coder'}

after = ''
found = dict()
#if its the first page, leave 'after' parameter blank else use the 'after' value from previous page
#Go through all pages specified and if the title or flair matches criteria then add to a dictionary
while pages != 0:
	if after != '':
		req = url.Request('http://www.reddit.com/r/metal/.json?after=' + after, None, hdr)
	else:
		req = url.Request('http://www.reddit.com/r/metal/.json', None, hdr)

	info = url.urlopen(req).read()

	info = json.loads(info.decode("UTF-8"))

	for i in info['data']['children']:
		try:
			print(i['data']['title'].lower())
			if genre in i['data']['title'].lower():
				content = i['data']['media']['oembed']['url']
				found[i['data']['title']] = content
		
			if genre in i['data']['link_flair_text'].lower():
				content = i['data']['media']['oembed']['url']
				found[i['data']['title']] = content
		except:
			print('')
		
	pages -= 1
	after = info['data']['after']
	sleep(2)	#this is important, reddit api states the average number of calls should be one every 2 seconds

#allow the user to choose between opening all found links or just printing them
openNew = input("Would you like to open all the found links in new tabs? (y/n)").lower()
for k,v in found.items():
	if openNew == 'y':	
		handle.open_new_tab(v)
	else:
		print(v)
