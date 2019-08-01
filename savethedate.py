
# -*- coding: UTF-8 -*-
import json
import time
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials
from twilio.rest  import Client

#Message your attendees from a spreadsheet

json_key = json.load(open('client_secret.json'))#add file name for the json created for the spread sheet
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open("GREEBLIST") #add your workbook name here
wks_attendees = wks.get_worksheet(0) #attendees worksheet

ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN'] 

client = Client(ACCOUNT_SID, AUTH_TOKEN) 
     
for num in range(215,219):  #to iterate between guests, amend this based on your total
    print("sleeping for 2 seconds")
    time.sleep(2) #adding a delay to avoid filtering
    
    guest_number = wks_attendees.acell('B' +str(num)).value
    guest_name = wks_attendees.acell('A'+str(num)).value
    
    if not guest_number:
        print (guest_name + ' telephone number empty not messaging')
        wks_attendees.update_acell('E'+str(num), '0') #set number to 0
    
    else:
        
        print ('Sending message to ' + guest_name)
        client.messages.create(
            to="+1" + guest_number, 
            from_="+1 9292544392", #your twilio number here
            #body= "Hey Party People!" + "\n\n" + u"\u2764" + u"\U0001F389" + u"\U0001F37E"  + "\n\nHere is some information about Stephanie and Mark's wedding: venue, directions, registry etc! Check out http://greeb.wedding and book your accommodations! We've been working on the website for some time so we hope you enjoy it! Also instead of replying (remember, I'm a dumb robot) please email greebwedding@gmail.com for questions or comments!\n" + u"\U0001f63b" + u"\U0001F525" + u"\U0001F63D",  
            #body = "Hi Friends and Family!" + "\n\n" +  "Steph and Mark's wedding robot again! Just wanted to drop a line and tell you about our family engagement party this past weekend! Check out http://bit.ly/greeb-engagement for some amazing photos by our friend Nicki! Also remember to check out http://greeb.wedding for info about our hotel and directions. Don't forget to book your room! Email greebwedding@gmail.com if you need to ask us anything else important\n" +  u"\u2764" + u"\U0001F389" + u"\U0001F37E" + u"\U0001F63D",
            body  = "Save The Date! "+"\n\n" +u"\u2764" + u"\u2728" + u"\U0001f63b"  + u"\U0001F389" + u"\U0001F37E" + u"\U0001F525" + u"\U0001F63D"+ u"\u2764" + "\n\nThe Marvelous Marriage of Stephanie Gross and Mark Kleback\n\nSaturday November 23rd 2019. \n\nSenate Garage,\nKingston NY\n\nThe Ceremony begins in the late afternoon. We'll send more details in the coming weeks!\n\nPlease text YES if you are saving the date and can join us or text NO if sadly, you won't be able to be with us.\n\nNo babies or kids. This event is 21+ "u"\U0001f618" + "\n" + u"\u2764" + u"\u2728" + u"\U0001f63b"  + u"\U0001F389" + u"\U0001F37E" + u"\U0001F525" + u"\U0001F63D"+ u"\u2764",
            #  body ="Hello you lovely people, tomorrow is the big day!!\n\nPost code for the venue: CM6 1RQ\n\nArrival time one thirty for a two o'clock ceremony.\n\nIt is a cash bar, so please bring sufficient money with you as there is no nearby cash machine.\n\nIt might be raining at some point in the day, so an umbrella might be required.\n\nThe venue is non smoking, due to the thatched buildings.\n\nWe could not be more excited that you are joining us for our special day and looking forward to sharing great food and good times!\n\nTom & Lauren",
        )
        wks_attendees.update_acell('E'+str(num), int(wks_attendees.acell('E' +str(num)).value) + 1) #increment the message count row
else:                  # else part of the loop
   print ('finished')
