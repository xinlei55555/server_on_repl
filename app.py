#!/usr/bin/python3

#before starting to use these, the best is to create a virtual env using
  #py -m venv give-a-name-to-your-virtual-environment
#to activate the virtual env
  # name\scripts\activate
#to install all the modules from requirements
  #pip install -r requirements.txt

from flask import Flask, jsonify, render_template
from flask import request
from call_location import call_location
from add_number import add_num
from spam_update import add_message, spam_update
from sms_testing import message_rating
#from search_number import search_number

#recognize()
#FOR RATING: 3 possibilities: spam, ham, empty string
#empty string = cannot find location or invalid number, dont return any icon in flutter
#for flutter: verify sender's number with phonenumber call_location module

app = Flask(__name__)

#running this thing on repl: https://docs.replit.com/tutorials/06-github-and-run-button
  #The .replit file as well as what is inside is SUPER IMPORTANT!!!

@app.route("/")
def home():
  return 'title: HELOOOO'
  # data = {"title": "HELOOO"}
  # return jsonify(data)

#this gives the location of the phonenumber passed in the url as well as the rating of the phonenumber
@app.route("/phonenumber") #take number as variable
def send_number():
  code = 0
  number = request.args.get('number') #between () is name of variable
  result = call_location(number)    #call location returns a list with title being result, rating being ham, spam or empty string
  print(result)
  #result[1] is the number of users that have already marked the number as spam!
  if int(result[1]) != 0:
    code = 2
  #number was never marked
  else:
    code = 1
  send_number = {'message_num': result[0], 'rating_num': code, 'was_marked': int(result[1])}
  return jsonify(send_number)

#this gives the rating of the message that was passed (spam or ham)
@app.route("/message")
def send_message():
  code_num = 0
  code_sms = 0
  sms = request.args.get('sms')
  number = request.args.get('number')
  result_num = call_location(number) 
  result_sms = message_rating(sms)

  #number was already marked, so spam
  if result_num[1] != 0:
    code_num = 2
  #number was never marked
  else:
    code_num = 1

  if result_sms[1] == 'spam':
    code_sms = 2
  elif result_sms[1] == 'ham':
    code_sms = 1
  else:
    code_sms = 0

  send_message = {'message_num': result_num[0], 'rating_num': code_num, 'message_sms': result_sms[0], 'rating_sms': code_sms, 'was_marked': int(result_num[1])}
  return jsonify(send_message)

#this should be used to add a message if the app got the prediction right
@app.route("/addmessage")
#Example
  #http://127.0.0.1:5000/addmessage?sms=hola%20wenhe&rating=ham
  #should return: {"title":"hola wenhe was successfully added as ham"}
def receive_add_message():
  sms = request.args.get('sms')
  rating = request.args.get('rating')
  add_message(sms, rating)
  message_add = {'title': sms + ' was successfully added as ' + rating}
  return jsonify(message_add)

#this must be used if the app has got the prediction wrong and we want to save it as the other way around the prediction
@app.route("/spamupdate")
def receive_spam_update():
  sms = request.args.get('sms')
  rating = request.args.get('rating')
  spam_update(sms, rating)
  if rating == "spam":
    message_add = {'title': sms + ' was successfully added as ham'}
  else:
    message_add = {'title': sms + ' was successfully added as spam'}
  return jsonify(message_add)


#this adds a phonenumber to the list of all the spam phonenumbers
@app.route("/addphonenumber")
def phonenumber_add():
#example:
  #http://127.0.0.1:5000//addphonenumber?number=4387654255
  #returns {"title":"4387654255 was successfully added"}
  number = request.args.get('number')
  add_num(str(number))
  phonenumber_add = {'title': number + ' was successfully added'}
  return jsonify(phonenumber_add)
  
# i just realized that all i have written rn is just copied from call-location.py, so lemme directly modify from there
  # #this should look for if a number that is given is already in the spam database
  # @app.route("/searchphonenumber")
  # def search_phonenumber():
  #   number = request.args.get("number")
  #   verdict = search_number(number)
  #   if verdict == True:
  #     console = {'title': number + " is spam"}
  #   console = {'title': number + " is ham"}
  #   return jsonify(console)

if __name__ == "__main__":
#this line is quite important!!!
  app.run(host='0.0.0.0', port=8080)
