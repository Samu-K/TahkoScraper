# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 11:53:15 2020

@author: Samu Kaarlela

This program will be used to easily look through the data on final_data.csv
"""

import pandas as pd
import math

filepath = "final_data.csv"
data = pd.read_csv(filepath)

welc_msg = "Hey,\nUse this to see what is happening at tahko.\nType options to see what you can do.\n"
date_msg = "Type a date in format day.month to see events that day"
event_msg = "Type 'All events' too see all different events happening"
unique_msg = "Type 'Unique events' to see all unique events."
options_msg = date_msg + "\n" + event_msg + "\n" + unique_msg

all_event_dates = {}
unique_events = []

for indx in data.index:
	event_time = data['time'].loc[indx]
	title = data['title'].loc[indx]
	
	try:
		if math.isnan(event_time) == True:
			continue
	except TypeError:
		pass
	
	split_time = str(event_time).split()
	date = split_time[2]
	all_event_dates[indx] = date
	
	if data['Unique Event'].loc[indx] == True:
		unique_events.append(indx)

print(welc_msg + "\nType 'exit' to exit")
inp = ''

commands = ['all events', 'unique events','options','exit']
while inp.lower() != 'exit':
	inp = input(':')
	
	if inp.lower() == 'options':
		inp = input( options_msg + "\n")
		continue
		
	if inp in all_event_dates.values():
		print("\n"+"Events that day are:")
		for indx,date in all_event_dates.items():
			if inp == date:
				event = data['title'].loc[indx]
				print(event)
				continue
				
	
	if inp.lower() == "unique events":
		for indx in unique_events:
			u_event = data['title'].loc[indx]
			u_time = data['time'].loc[indx]
			u_loc = data['loc'].loc[indx]
			
			print(u_event + "\n" + u_time + "\n" + u_loc+"\n")
			continue
	
	if inp.lower() == 'all events':
		all_events = data['title'].unique()
		for event in all_events:
			print(event+"\n")
		continue
	
	if inp.lower() not in commands:
		if inp.lower() not in all_event_dates.values():
			print("Unknown Command or invalid date")