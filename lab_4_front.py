import os
from bottle import run, request, route, Bottle, template, redirect, response
import pickle
import sys

import httplib2

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build



from autocorrect import spell


import random


import sqlite3 as lite


conn = lite.connect('example.db')


def get_auto_corrected_words(words):
	"""check each word in words to see if there is an autocorrect suggestion, then reutrn if there was an autocorrect, and the final"""
	autocorrected = False
	auto_corrected_words = []
	for word in words:
		if spell(word) != word:
			autocorrected = True
			auto_corrected_words.append(spell(word))
		else:
			auto_corrected_words.append(word)

	if autocorrected == False:
		return False

	else:
		return auto_corrected_words


#use THIS ONE
def Get_Results_List(db, page_number):
	"""test that the page number is within the db's limit.. use a num per page amount = 2 then build a list of dict() of the results in range"""
	AMOUNT_PER_PAGE = 2
	if len(db) % AMOUNT_PER_PAGE == 0:
		extra = 0
	else:
		extra = 1
	if len(db) / AMOUNT_PER_PAGE + extra <= page_number or page_number < 0:
		return 'ERROR PAGE OUT OF RANGE'
	
	return_list = []
	top_index = page_number + 1
	top_index *= AMOUNT_PER_PAGE
	if top_index > len(db) - 1:
		top_index = len(db)

	for i in range(page_number * AMOUNT_PER_PAGE,  top_index , 1):
		primary_key, url, rank, words = db[i]

		return_list.append({
			'url': url,
			'text': words,
			'title': rank
			})
		
	return return_list


def Get_Number_Of_Pages(db, number_per_page):
	"""Each row in db/number per page + the mod"""
	if len(db) == 0:
		return 0
	else:
		if len(db)%number_per_page == 0:
			extra = 0
		else:
			extra = 1

		return len(db)/number_per_page + extra

def Make_Url_Request(word):
	"""Make call to interface to backend to get a db object"""
	db = get_url_list_for_word(word) #can also check errors and stuff
	return db


def Make_Url_Request_For_All_Words(words):
	db = get_url_list(words, 50)
	return db










############# HERE ARE THE UPDATED FUNCTIONNNNNNNNSsss
def get_url_list(words, preview_length):
    """Returns a list of tuples. Tuples contain the URL that contained any space sperated word in 'words', as 
    well as other info. Changes rank, in returned the list, for a related URL if the URL contains more than
    one word from 'words'""" 

    all_words = words.split()
    final_res = []
    for word in all_words:
        # Get a list of results for each word in 'words'
        cur_res = get_url_list_for_word(word)
        for res in cur_res:
            # Check for if the current url entry is already in 'final_res'
            if res not in final_res:
                final_res.append(res)
            else:
                final_res.remove(res)
                # Updating rank of result if a url has more than one word from 'words'
                rep_res = (res[0],res[1],(res[2] + 1), res[3])
                final_res.append(rep_res)

    final = []
    for hit in final_res:
        preview = get_text_preview(words, hit[3], preview_length)
        final.append((hit[0], hit[1], hit[2], preview))
        
    return final

def get_text_preview(words, all_words, preview_length):
    """Returns a string, 'preview_text', of max length 'preview_length' 
    starting which word from 'words' that appears first in 'all_words'
    
    """
    search_words = words.split()
    index = len(all_words);
    # Find which word in 'words' occurs first
    for word in search_words:
        temp_index = all_words.find(word)
        if (temp_index < index):
            index = temp_index

    # Builds the preview_text
    if (index + preview_length) > len(all_words):
        preview_text = all_words[index:len(all_words)]
    else:
        preview_text = all_words[index:(index + preview_length)]
    return preview_text

#########################################################









def get_url_list_for_word(word):
    """Returns a list of tuples. Tuples contain the URL that contained 'word', as well as other info"""

    con = lite.connect("page_rank.db")
    cur = con.cursor()
    cur.execute('SELECT * FROM rankTable')
    search_res = []
    # Get entire table
    rows = cur.fetchall()
    for row in rows:
        # 'row[3]' is a single string of all the words at its given URL, they are space seperated
        all_words = row[3]
        all_split = all_words.split()
        # Adds row to 'search_res' if 'word' exists anywhere in 'all_words'
        if word in all_split:
            search_res.append((row[0], str(row[1]), row[2], str(row[3])))
    return search_res


def Get_Nav_Info(page_number, number_per_page, query_string, db):
	nav_info = dict()
	if page_number > 0:
		# not the first, so show left arrow

		nav_info['previous_page_url'] = '/home/query/select_page?page_number=' + str(page_number-1) + '&query_string=' + query_string

	nav_info['current_page'] = page_number
	nav_info['number_of_pages'] = Get_Number_Of_Pages(db, number_per_page)

	if page_number < int(nav_info['number_of_pages'])-1:
		#not the last show next arrow
		nav_info['next_page_url'] = '/home/query/select_page?page_number=' + str(page_number+1) + '&query_string='+ query_string
	return nav_info
	

@route('/')
@route('/home')
@route('/home/')
def home():
	return template('THE_BUCKET_FRONT_TEMPLATE.tpl', errors = None, query_string = None, autocorrect = None, results = None, nav_info = None)

@route('/home/ajax_query')
def ajax_query():
	query_string = request.query.query_string
	words = query_string.split()
	
	final_words = get_auto_corrected_words(words)
	

	# word = query_string.split()[0]
	# db = Make_Url_Request(word)

	db = Make_Url_Request_For_All_Words(query_string)

	if len(db) < 1:
		return template('THE_BUCKET_AJAX_RESULTS_TEMPLATE.tpl', results = None)

	page_number = 0

	results = Get_Results_List(db, page_number)

	return template('THE_BUCKET_AJAX_RESULTS_TEMPLATE.tpl', results = results)



@route('/home/query')
def home_query():
	"""the user input query is sent to a non-logged-in home script and requests are made to the backend for the db info"""
	query_string = request.query.query_string

	words = query_string.split()

	final_words = get_auto_corrected_words(words)
	
	if final_words != False:
		autocorrect = ' '.join(final_words)
	else:
		autocorrect = None

	# word = query_string.split()[0]
	# db = Make_Url_Request(word)

	db = Make_Url_Request_For_All_Words(query_string)

	if len(db) < 1:
		errors = []
		errors.append('Sorry, There doesn\'t seem to be any found')
		return template('THE_BUCKET_FRONT_TEMPLATE.tpl', errors = errors, query_string = None, autocorrect = autocorrect, results = None, nav_info = None)

	page_number = 0

	results = Get_Results_List(db, page_number)

	nav_info = Get_Nav_Info(int(page_number), 2, query_string, db)


	return template('THE_BUCKET_FRONT_TEMPLATE.tpl', errors = None, query_string = query_string, autocorrect = autocorrect, results = results, nav_info = nav_info)





@route('/home/query/select_page')
def home_query_select():
	"""change the page for the query submitted"""
	query_string = request.query.query_string
	page_number = request.query.page_number

	word = query_string.split()
	final_words = get_auto_corrected_words(word)
	

	if final_words != False:
		autocorrect = ' '.join(final_words)

	else:
		autocorrect = None
	
	# word = query_string.split()[0]
	# db = Make_Url_Request(word)

	db = Make_Url_Request_For_All_Words(query_string)
	if len(db) < 1:
		errors = []
		errors.append('Sorry, There doesn\'t seem to be any found')
		return template('THE_BUCKET_FRONT_TEMPLATE.tpl', errors = errors, query_string = None, autocorrect = autocorrect, results = None, nav_info = None)
	results = Get_Results_List(db, int(page_number))
	nav_info = Get_Nav_Info(int(page_number), 2, query_string, db)

	if int(page_number) >= nav_info['number_of_pages']:
		#return str(page_number) + ' ' + str(nav_info['number_of_pages'])
		return template('THE_BUCKET_FRONT_TEMPLATE.tpl', errors = ['PAGE_OUT_OF_RANGE'], query_string = None, autocorrect = None, results = None, nav_info = None)



	return template('THE_BUCKET_FRONT_TEMPLATE.tpl', errors = None, query_string = query_string, autocorrect = autocorrect, results = results, nav_info = nav_info)


@route('/test0')
def choose():
	return template('testtemp0.tpl')

@route('/test1')
def test_template1():
	return template('testtemp1.tpl')

@route('/test2')
def test_template2():
	return template('testtemp2.tpl')

@route('/test3')
def test_template3():
	return template('testtemp3.tpl')

if __name__=="__main__":
	if len(sys.argv) < 2:
		ip_addr = 'localhost'
		port = 80

	elif len(sys.argv) == 2:
		ip_addr = sys.argv[1]
		port = 80
	else:
		ip_addr = sys.argv[1]
		port = int(sys.argv[2])

	run(host=ip_addr, port=port, debug=True)



