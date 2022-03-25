#----------------- model with gspread
  # #here are two links that really did help
  # #https://www.youtube.com/watch?v=n2aQ6QOMJKE&ab_channel=SessionWithSumit
  # #

  # import gspread
  # #this module lets us enter data into the google spread sheet

  # gc = gspread.service_account(filename = "cred.json")
  # #this tells the gspread module where to look for the informations on our google sheet

  # sh = gc.open_by_key("1sCqJsDP_CWZCboWy9W5mDqxyuIjPqIP3MEFvw3276xs")
  # #this is part of the link for the google sheet that contains the spam messages

  # worksheet = sh.sheet1
  # # this tells the module which sheet that we want (because we only have one sheet, we can just write sheet #1)

  # def spam_update(message, analysed_rating):
  #   # this should change the value of the analysed_rating
  #   if analysed_rating == 'spam':
  #     worksheet.append_row(["ham", message])
  #     #this should add a row in the sheet
  #   else:
  #     worksheet.append_row(["spam", message])
  #   print("successfully added message and corrected error")

  # def add_message(message, verdict):
  #   if verdict == 'spam':
  #     worksheet.append_row(["spam", message])
  #     #this should add a row in the sheet

  #   else:
  #     worksheet.append_row(["ham", message])
  #   print("successfully added message")


  # #Test message:

#------------------------ version, when we use csv

import csv
import pandas as pd

FILENAME = "spam_messages.csv"
df = pd.read_csv(FILENAME)

def append_list_as_row(file_name, list_of_elem):
    with open(file_name, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)

            # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

def delete_message(message):
    df = pd.read_csv("spam_messages.csv")
    #this line basically recreated a new dataframe, by using all tha value EXCEPT the row that had the value of message
    df = df[df.message != message]

#this should replace the spam_messages.csv file with the new dataframe
    df.to_csv(FILENAME,index = False )
    

def spam_update(message, analysed_rating):
    #this will remove the old message that appeared before
    delete_message(message)

    if str(analysed_rating) == 'spam':
        append_list_as_row(FILENAME, ['ham', message])

    else:
        append_list_as_row(FILENAME, ['spam', message])
    print("successfully added message and corrected error")

def add_message(message, verdict):
    #this creates another dataframe, if the dataframe has a value, this means that the value has already appeared in the spam_messages.csv file, and i will thus not add it
    df2 = df[df.message == message]
    print(df2.head())
    if len(df2.index) == 0:
        if str(verdict) == 'spam':
            append_list_as_row(FILENAME, ['spam', message])

        else:
            append_list_as_row(FILENAME, ['ham', message])
        print("successfully added message")

    else:
        print("this message has already appeared in the database!")
