# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 14:22:26 2020

@author: Samu Kaarlela
"""

import scrapy

class TahkoScraper(scrapy.Spider):
	name = "tahko_events"

	start_urls=["https://www.tahko.com/fi/tapahtumat/"]

	def parse(self,response):
		
		#Scrape all the tables
		tables = response.xpath('//*[@class="table table-stripefd"]')
		
		for table in tables:
			#Scrape the rows from the table
			rows = table.xpath('tr')
			
			#We set a list of all weekdays shortened in finnish
			#This is used later to see if we're handling a time or date
			days = ["ma","ti","ke","to","pe","la","su"]
			
			#We set a placeholder value for date, so we get not errors
			date = ""
			backup_time = "N/A"
			
			#Iterate over the rows of the table
			for row in rows:
				#Start by checking if the tabledata(td) is empty
				if row.xpath('td//text()') == []:
					#if it is we skip the rest of the code and go to next row
					continue
				
				#We get the link to the event
				link = row.xpath('td[2]/h4/a/@href').extract_first()
				
				#We get the first element in the tabledata
				#Returns a list with the time as the 0:th element
				time = row.xpath('td[1]//text()').extract()
				
				#Make sure the time isn't empty
				#Avoids IndexError
				if time:
					#We split the time into elements to see if we have a date
					time_split = time[0].split()
					if time_split[0].lower() in days:
						#If we determine a date, we set the date and skip the rest
						#Rows with dates don't have any event data
						date = time[0]
						continue
					
					#Set the original time and add the determined date to it
					time = time[0] + " " + date
					
					#We also setup a backup time
					#This will be used to fill if we have sequential events
					backup_time = time
					
				else:
					#If the time is empty, we can assume that event is sequential
					time = backup_time
					
				#Second element in the td is a list of different attributes
				attr_list = row.xpath('td[2]//text()').extract()
				
				#Make sure the list isn't empty
				#Avoids IndexError
				if attr_list:
					#Normal and bolded events need different handling
					#Check notes.txt
					if attr_list[0].rstrip() != "":
						title = attr_list[0]
					else:
						title = attr_list[1]
						
					loc = attr_list[3]
					
					try:
						firm = attr_list[4]
					except IndexError:
						firm = "N/A"
				else:
					#If the data is empty we set all to nothing
					title = ""
					loc = ""
					firm = ""
					
				#Returns a dict with the below values
				yield {
						'time':time,
						'title':title.title().rstrip(),
						'loc':loc.rstrip(),
						'firm':firm,
						'link':link
						}