#Code using gspread:
    # import gspread
    # #import pandas as pd
    # #import pygsheets


    # def return_row_from_cell(cell_with_value):
    #     last_index = str(cell_with_value)[7:].find('C')
    #     row_value = str(cell_with_value)[7:7+last_index]
    #     return int(row_value)

    # def search_number(number):
    #     number = str(number)
    #     #the next few lines are basically just so that i can access the files
    #     gc = gspread.service_account(filename = "cred.json")
    #     sh = gc.open_by_key("1zGbjjH2ibHh6SEctWO_PYxvhkVinMK_0SJvYO4DXtDo")
    #     worksheet = sh.sheet1   
    #     # data = worksheet.get_all_values()

    # #this returns a list of all the instances of the value we are looking for
    #     cell_with_value = worksheet.findall(number, in_column = 1)

    #     #if there is such a value, then it will return the value of the frequence
    #     if cell_with_value != []:
    #         row_value = return_row_from_cell(cell_with_value[0])
    #         return int(worksheet.cell(row_value,  2).value)
    #     return 0
    #--------------------
#-------------------------------------------
#Code using pandas
import pandas as pd

def search_number(number_we_are_looking_for):
    data = pd.read_csv("unwanted_calls.csv")

    number_we_are_looking_for = int(number_we_are_looking_for)


    #print(data['Frequence'])
    # print(data.iloc[1,0])
        #The error I was making is that i used ":" instead of "row, column"

    #This line seems to be useless if we are using read_csv, as it will directly convert the csv data intro a pandas dataframe. Additionally, I already have the names of the columns written on top of the csv, so redeclaring "columns = [...]" isn't useful, it'll just keep the same thing
        #df = pd.DataFrame(data = data, columns = ["Number", "Frequence"])
        #         #The error i was getting was due to the fact that, in the csv file, the names of the columns had capitalization while i tried to force new names that didn't have capital letters!!! 
        # #proof it is useless:
        # print(df.iloc[0] == data.iloc[0])
        #     #>>True
        # print(df.iloc[1] == data.iloc[1])
        #     #>>True

    #the method that i will use later only accepts series. So here, I just converted the dataframe into a series.
        #numbers = pd.Series(data["Number"], dtype = int)
        
    #this is to search a sorted database, and give the position to insert the value, if a value was to be inserted.
        #https://pandas.pydata.org/docs/reference/api/pandas.Series.searchsorted.html
        #Here, i converted into a string before searching, or else, it would be 
            #Actually, do not convert into a string, as it wouldn't give the index in ascending order, but in alphabetical order. (like, they wouldn't consider if a number was smaller or bigger, but if the first digit of the number is smaller or bigger)
        #index = numbers.searchsorted((number_we_are_looking_for))

        #Ok, i realized something. This method returns the index where the value at the index is bigger than the value given, but the index before is smaller.
            #if instead, i am looking to compare a value, i have to manually compare the value they give.
            #ok, rage quit, ima write my own binary search algorithm

#---------
    # value = data.iloc[data.last_valid_index(), 0] == 100000000000000000000000
    # print(value)
    # #>>> returns false

#this gives us the last valid_index()
    upper = int(data.last_valid_index())
    down = 0

#THE WEIRD THING WITH THAT is that it skips the first and last value, like it doesn't take them into account, that's why i purposefully placed very random numbers at first and last
    while upper > down:
        #the // is for floor division
        middle = (upper + down ) // 2
        if int(data.iloc[middle, 0]) == number_we_are_looking_for:
            #I am returning the frequence
            print("the index found is at ", middle, " the number is ", data.iloc[middle, 0])
            return int(data.iloc[middle, 1])

        if int(data.iloc[middle, 0]) < number_we_are_looking_for:
            #I add one to the middle, cuz that if the middle isn't equal, then it should be included in the possibilities.
            down = middle + 1
        
        if int(data.iloc[middle, 0]) > number_we_are_looking_for:
            upper = middle - 1 

#if no value are in the database, return a frequence of 0
    return 0

#print(search_number(1999999990))


# if df[df.number == number_we_are_looking_for].empty == False:
    # #this means that there is a value that has the search value    
    #     return df.number
    # return 