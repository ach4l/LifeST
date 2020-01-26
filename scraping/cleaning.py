#############      Creating a CSV File. Also Cleaning the comments.      #############
import glob
import json
import csv
import pandas as pd


comment_list = []
song_number_list = []
song_index = 0
for filepath in glob.iglob('data/*.json'):
    #print(filepath)
    
    comment_string = ''
    with open(filepath) as f:
        
        data = json.load(f)
        for comment in data.values():
            comment_string = comment_string + comment
    songname = filepath.split('\\')[1]
    comment_list.append([songname,comment_string])
    song_number_list.append([song_index,songname])
    song_index = song_index + 1
header = ['song', 'comments']
comments_df = pd.DataFrame(data = comment_list, columns = header)
song_index_df = pd.DataFrame(data = song_number_list, columns = ['index','songname'])
print(comments_df.head())
print(song_index_df.head())
comments_df.to_csv('SM_1000.csv')
song_index_df.to_csv('SM_1000_index.csv')
