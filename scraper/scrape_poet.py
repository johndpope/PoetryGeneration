########################################################################################
# Author:   Kate Baumli
# Date:     06/27/2018
# Purpose:  This script scrapes all poems by a certain poet from poets.org
# Inputs:   Poet name and url to first page of search results for that poet on poets.org
#           Default poet/link: Robert Frost        
# Outputs:  TODO: Just leave it in dict for now, still need to decide what kind
#           of file to write to
########################################################################################

#########
# Imports
#########
from argparse import ArgumentParser 
import os
import requests
from bs4 import BeautifulSoup
import ast

#################################################
# Load command line args (just poet name and url)
#################################################
def load_args():
    print('Processing arguments...')
    parser = ArgumentParser()
    parser.add_argument('--poet', help='Name of the poet whos poems you want to\
                        scrape',required=False, default='Robert Frost')
    parser.add_argument('--url', help='url from which to scrape poetry.Example:\
                        https://www.poets.org/poetsorg/poems/45684', required=False, 
                        default='https://www.poets.org/poetsorg/poems/45684')
    # TODO: Make URL an ID # instead.. all URLS have the same format & ID is
    # easier to type
    return parser.parse_args()

###################################
# Scrape source code from a webpage
###################################
def get_page_source(url):
    try:    
        r = requests.get(url)
        # print(r.status_code) # If request granted should be 200
        html = r.text
    except:
        return None
    return BeautifulSoup(html, "lxml")

###############################################
# Get all pages from this poet's search results
###############################################
def get_search_page_links(soup):
    search_page_links = [args.url] # The first page is the one we were given
    base_link = 'https://www.poets.org'
    # Take all of the page links
    pages = soup.find_all("li", "pager-item")
    for page in pages:
        link = base_link + page.find('a').get('href')
        search_page_links.append(link)
    return search_page_links
    
    # NOTE: I don't  know if this will work when not all page numbers are
    # listed (when it's like 1 2 3 ... 24 or something) might need to rework
    # later if this becomes an issue

####################################################
# Get links to pages with poem text from search page
####################################################
def get_poem_links(page_links):
    poem_links = []
    base_link = 'https://www.poets.org'
    for page in page_links:
        print('Scraping all of {0} \'s poems from {1}'.format(args.poet,page))
        soup = get_page_source(page)
        all_poem_cells = soup.tbody.find_all("td", "views-field views-field-title")
        for poem in all_poem_cells:
            link = base_link + poem.find('a').get('href')
            poem_links.append(link)
    print("Found {0} poems by {1}.".format(len(poem_links),args.poet))
    return poem_links        

###############################
# Get poetry content from links
###############################
def get_poems(poem_links):
    poems = dict() # key = title value = poem text
    for link in poem_links:
        soup = get_page_source(link)
        soup_dict = ast.literal_eval(soup.head.script.string)
        title = soup_dict['headline']
        print('Retrieving', title)
        poem = soup_dict['description']
        poems[title] = poem
    return poems

############################
# CODE STARTS EXECUTION HERE
############################
args = load_args()
main_soup = get_page_source(args.url)
page_links = get_search_page_links(main_soup)
poem_links = get_poem_links(page_links)
poems = get_poems(poem_links)
for title, poem in poems.items():
    print(title,':\n', poem)
