import nltk
import urllib
import re as regexp
import requests
import os
from bs4 import BeautifulSoup
import csv
import json

def getComments(songpage):
    '''
    takes as input a songmeanings html page and returns lists of beautifulsoup objectscomments, upvotes and the comment types
    '''
    print('*************************************************************************************************')
    print('************************                Getting Comments               **************************')
    print('*************************************************************************************************')
    #print(songpage)
    songpagesoup = BeautifulSoup(songpage,"lxml")
    for div in songpagesoup.find_all("div",{'class':'text'}):
        for div in div(class_='title'):
            div.extract()
    for div in songpagesoup.find_all("div", {'class':'sign'}):
        div.decompose()
    for div in songpagesoup.find_all("ul", {'class':'answers'}):
        div.replace_with("")
    song_meaning = songpagesoup.find_all('div' ,class_='text', id_='')
    find_upvotes = songpagesoup.find_all('strong' , class_='numb')
    comment_type = songpagesoup.find_all('strong', class_='title', id ='')
    return  song_meaning, find_upvotes, comment_type

fo=open('songnamesrem.txt','r', encoding="utf8")
ln=fo.readlines()
for il  in ln[:]:
    songpageadress=il.split(";")[0]
    songname = il.split(";")[1]
    print(songpageadress, songname)
    # songpage=urllib.request.urlopen('http:'+songpageadress)
    # songpagehtml=songpage.read()
    # songpagetext=songpagehtml.decode('utf-8')
    # comments,upvotes,comment_types = getComments(songpagetext)
    data = {}
    comment_counter = 0
    
    for j in range(1,50):
        print(' Page ' + str(j))        
        payload = {'command': 'loadComments', 'sortable': 'DESC', 'orderby': 'int_rating', 'commenttypes':'all', 'page':str(j), 'specific_com': 'undefined'} # 'key2': 'value2' and so on (comma delimited)
        r = requests.post('https:'+songpageadress, data=payload)
        #url = 'https://songmeanings.com/songs/view/5727/'
        #payload = {'command': 'loadComments', 'sortable': 'DESC', 'orderby': 'int_rating', 'commenttypes':'all', 'page':str(j), 'specific_com': 'undefined'}
        #r = requests.post(url, data=payload)
        comments,upvotes,comment_types = getComments(r.text)
        

        if len(comments)==0:
            print('NO MORE COMMENTS. MOVING TO THE NEXT SONG')
            break            
            #print(r.text)
        else:
            print('TOTAL NO OF COMMENTS :' + str(len(comments)))
            #print(comments[0])
                 
            #rows = zip(comments,upvotes,comment_types)
            comment_index = 0
            #for row in rows:
            for comment in comments:
                #print(comment)
                #print('TOTAL NO OF COMMENTS :' + str(len(comments)))
                #print(row)
                #print(comments[0])
                data['comment_' + str(comment_counter)] = comment.text
                #print(data['comment_' + str(comment_counter)])
                comment_index = comment_index+1
                comment_counter = comment_counter+1  
                #row_dict = {'comment':comments[row], 'upvotes' : upvotes[row], 'comment_type': comment_types[row]}
                                
                #data[str(comment_counter)] = row_dict                
            #print(data)
    with open('data/' + songname.rstrip() +'.json', 'w') as fp:
        json.dump(data, fp)
                     
            
    
            

