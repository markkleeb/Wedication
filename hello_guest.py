from flask import Flask,render_template, url_for, request, redirect, make_response
#from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.messaging_response import MessagingResponse
import time
import json
import gspread
#from oauth2client.client import SignedJwtAssertionCredentials
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

app = Flask(__name__,static_folder='app/static')

json_key = json.load(open('client_secret.json')) #add file name for the json created for the spread sheet
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
#credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
gc = gspread.authorize(credentials)
wks = gc.open("GREEBLIST") #add your workbook name here
wks_attendees = wks.get_worksheet(0) #attendees worksheet
wks_food = wks.get_worksheet(1) #food responses worksheet


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')
@app.route("/venue", methods=['GET', 'POST'])
def returnVenue():
    return render_template('venue.html')
@app.route("/food", methods=['GET'])
def returnFood():
    return render_template('food.html')
@app.route("/contact", methods=['GET', 'POST'])
def returnContact():
    return render_template('contact.html')
@app.route("/gifts", methods=['GET', 'POST'])
def returnGifts():
    return render_template('gifts.html')
@app.route("/faq", methods=['GET', 'POST'])
def returnFAQ():
    return render_template('faq.html')
@app.errorhandler(500)
def internal_error(error):
    return "500 error"
    return "!!!!"  + repr(error)
@app.route("/messages", methods=['GET', 'POST'])
def hello_guest():
    
    resp = MessagingResponse() 
    from_number = request.values.get('From', None)
    from_body = request.values.get('Body', None)
    number = from_number
    body_strip = from_body.lower()
    clean_number = number.strip("+")
    
    #all of these values depend on how many guests are at your wedding

    #attendance variables
    guest_confirmed = wks_attendees.acell('C257').value
    guest_unconfirmed = wks_attendees.acell('C258').value
    guest_no_response = wks_attendees.acell('C259').value
    guest_acceptance = wks_attendees.acell('C260').value
    
    #meal total variables
    #guest_meals_confirmed = wks_attendees.acell('C261').value 
    #guest_meals_unconfirmed = wks_attendees.acell('262').value
    
    #meal options (name/amount)
    #starter_option_1 = wks_food.acell('G2').value
    #starter_option_1_amount = wks_food.acell('H2').value
    
    #starter_option_2 = wks_food.acell('G3').value
    #starter_option_2_amount = wks_food.acell('H3').value

    #starter_option_3 = wks_food.acell('G4').value
    #starter_option_3_amount = wks_food.acell('H4').value
    
    #main_option_1 = wks_food.acell('G5').value
    #main_option_1_amount = wks_food.acell('H5').value
    
    #main_option_2 = wks_food.acell('G6').value
    #main_option_2_amount = wks_food.acell('H6').value
    
    #main_option_3 = wks_food.acell('G7').value
    #main_option_3_amount = wks_food.acell('H7').value
    
    #dessert_option_1 = wks_food.acell('G8').value
    #dessert_option_1_amount = wks_food.acell('H8').value
    
    #dessert_option_2 = wks_food.acell('G9').value
    #dessert_option_2_amount = wks_food.acell('H9').value

    guest_confirmation_cell = wks_attendees.find(str(clean_number).strip()) 
    
    if "yes" in from_body.lower(): 
        #We have a keeper! Find the attendee and update their confirmation_status
        wks_attendees.update_acell("F" + str(guest_confirmation_cell.row), 'Accepted') #update the status to accepted for that guest
        wks_attendees.update_acell("C261", wks_attendees.acell("A" + str(guest_confirmation_cell.row)).value)
        resp.message(u"\u2665" + "Thanks! We can't wait to see you. More information will be on the way soon! " + u"\u2665")  #respond to the guest with a confirmation! 
        #resp.message("Thanks! We can't wait to see you. More information will be on the way soon!")  #respond to the guest with a confirmation! 

    elif "no" in from_body.lower(): #no! 
       #update the confirmation_status row to declined for that guest
        wks_attendees.update_acell("F" + str(guest_confirmation_cell.row), 'Declined')  
        wks_attendees.update_acell("C261", wks_attendees.acell("A" + str(guest_confirmation_cell.row)).value)
        resp.message("Sorry to hear that, we still love you!") #respond to the user confirming the action 
    
    elif "numbers" in from_body.lower(): #return statistics (total guests, food choices list)   
        resp.message("R.S.V.P update:\n\nTotal Accepted: " + guest_confirmed +
         "\n\nTotal declined: " + guest_unconfirmed + "\n\nTotal no response: " +
        guest_no_response + "\n\nTotal acceptance rate: " + guest_acceptance) 

    elif "food" in body_strip.strip():   #respond with the current food totals and the meal choices  

        resp.message("Guest meals decided:" + guest_meals_confirmed + 
        "\nGuest meals undecided: " + guest_meals_unconfirmed +
        "\n\nMenu breakdown:\n\n" + starter_option_1 +": " +
        starter_option_1_amount + "\n" + starter_option_2 +": " +
        starter_option_2_amount + "\n" + starter_option_3 +": " +
        starter_option_3_amount + "\n" + main_option_1 +": " +
        main_option_1_amount + "\n" + main_option_2 +": " + main_option_2_amount +
        "\n" + main_option_3 +": " + main_option_3_amount + "\n" +
        dessert_option_1 + ": " + dessert_option_1_amount + "\n" + dessert_option_2
        + ": " + dessert_option_2_amount)

    else: #respond with invalid keyword
        resp.message("I am Steph and Mark's wedding robot, and do not understand what you said. We need a YES or a NO, you sent: " +
        from_body)
    return str(resp)
 
if __name__ == "__main__":
    app.run(debug=True)
