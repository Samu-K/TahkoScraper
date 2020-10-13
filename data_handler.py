# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 10:43:45 2020

@author: Samu Kaarlela

We'll use this to handle the data that we've scraped.
"""
#Import needed modules
import pandas as pd

file_path = "C:/Users/Oppilas/Google Drive/Lukio/Satunnainen/Scrape Project/TahkoScraper/TahkoScraper/spiders/scrape.json"

data = pd.read_json(file_path)

unique_counts = data.title.value_counts()

single_events = []
for indx,value in unique_counts.items():
	if value == 1:
		single_events.append(indx)
		
for indx in data.index:
	title = data['title'].loc[indx]
	
	if title in single_events:
		data.loc[indx,'Unique Event'] = True
	elif title not in single_events:
		data.loc[indx,'Unique Event'] = False
		
data.to_csv("final_data.csv",index=False)
print("Data Handling Successful")