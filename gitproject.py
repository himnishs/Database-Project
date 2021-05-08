import mysql.connector
import os

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "root" #change this to whatever your sql password is
)

def initDB():
    mycursor = mydb.cursor()
    mycursor.execute('USE library_database') #Change this to whatever your schema is

def displayMain():
    print("-----Menu-----")
    print("0: Quit")
    print("1: Login (Sign-In)")
    print("2: Check-Out Item")
    print("3: Check-In Item")
    print("4: Add Event")
    print("5: Attend Event")
    print("6: View Event")
    print("7: Check Item Availability")
    print("8: Add Item")
    print("9: Remove Item")
    print("10: View Your Checked Out Items")
    print("11: Get Item Rating")
    print("12: Rank Items")

def user_sign_in():
    #Check to see if the user has signed up for the library
    mycursor = mydb.cursor()
    check_id = int(input("Have you made an account at the library? (1 -- yes, 0 -- no)"))
    user_check = True
    logged_in = False
    if(check_id):
         user_id = int(input("What is your user ID?"))
         pass_word = input("What is your password? ")
         select_customer_id_query = "SELECT id, passwd FROM Customer"
         #Looping with all the queries to check that the condition is true
         with mydb.cursor() as cursor:
             cursor.execute(select_customer_id_query)
             result = cursor.fetchall()
             for row in result:
                 if(row[0] == user_id and row[1] == pass_word):
                     logged_in = True
                     #Place Holder for the logged_in = true
         #Check if the ID exists into the database
    else:
        make_id = int(input("Would you like to make an account at the library? (1 -- yes, 0 --no)"))
        if(make_id):
            create_account()
        else:
            print("Alright, Have a nice day! We hope to see you at the library again!")
    return logged_in

def create_account():
    mycursor = mydb.cursor()
    make_user_id = input("What would you like your username to be?")
    #Possible interaction with other user ids to make sure that they don't match
    make_user_psswd = input("What would you like your password to be?")
    sql = "INSERT INTO Customer (email, customerFName, customerLName,id, passwd) VALUES (%s, %s, %s, %s, %s)"
    val = ('', '', '', make_user_id, make_user_psswd)
    mycursor.execute(sql,val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

def librarian_sign_in():
    #Check to see if the user has signed up for the library
    mycursor = mydb.cursor()
    librarian_check = False
    check_id = int(input("Have you made an adminstrative account at the library? (1 -- yes, 0 -- no)"))
    user_check = True
    if(check_id):
         user_id = int(input("What is your user ID?"))
         pass_word = input("What is your password? ")
         select_customer_id_query = "SELECT id, passwd FROM Librarian"
         #Looping with all the queries to check that the condition is true
         with mydb.cursor() as cursor:
             cursor.execute(select_customer_id_query)
             result = cursor.fetchall()
             for row in result:
                 if(row[0] == user_id and row[1] == pass_word):
                     print("This works broski")
                     librarian_check = True
    else:
        make_id = int(input("Would you like to make an adminstrative account at the library? (1 -- yes, 0 --no)"))
        if(make_id):
            create_librarian()
        else:
            print("Alright, Have a nice day! Let me know if you want to make an adminstrative account!")
    
    return librarian_check

def create_librarian():
    mycursor = mydb.cursor()
    make_user_id = input("What would you like your username to be?")
    #Possible interaction with other user ids to make sure that they don't match
    make_user_psswd = input("What would you like your password to be?")
    sql = "INSERT INTO Librarian (id, passwd, librarianFName, librarianLName, Salary, Hours_Worked, Librarian_Email) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (make_user_id, make_user_psswd, '', '', '', '', '')
    mycursor.execute(sql,val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

def check_librarian_id():
    user_id = int(input("What is your Librarian ID?"))
    pass_word = input("What is your Librarian password? ")
    librarian_check = False
    select_customer_id_query = "SELECT id, passwd FROM Librarian"
    #Looping with all the queries to check that the condition is true
    with mydb.cursor() as cursor:
        cursor.execute(select_customer_id_query)
        result = cursor.fetchall()
        for row in result:
            if(row[0] == user_id and row[1] == pass_word):
                #print("This works broski")
                librarian_check = True
    return librarian_check

def check_out_item(user_login):
    mycursor = mydb.cursor()
    if(user_login == False):
        print("You may not check out!")
        quit()
    user_id = int(input("Please enter your user id: "))
    item_id = int(input("Please enter the item id: "))
    select_item_id_query = "SELECT Item_Aval FROM Item"
    with mydb.cursor() as cursor:
        cursor.execute(select_item_id_query)
        result = cursor.fetchall()
        for row in result:
            if(not isinstance(item_id,int) or row[0] == None):
                print("We are very sorry but either the item id is invalid or the item is checked out")
                quit()
            else:
                 sql = "UPDATE Item SET Item_Aval =%s, holder_id =%s WHERE id =%s" % (0, user_id, item_id)
                 #val = (item_id, '', '', None, 0, user_id)
                 mycursor.execute(sql)
                 mydb.commit()
                 
        print("Congrats you've checked out the item!")

def check_in_item(user_login):
    mycursor = mydb.cursor()
    if(user_login == False):
        print("You may not check out!")
        quit()
    user_id = int(input("Please enter your user id: "))
    item_id = int(input("Please enter the item id: "))
    select_item_id_query = "SELECT holder_id FROM Item"
    #Check if the user is the person that checked out the Item
    with mydb.cursor() as cursor:
        cursor.execute(select_item_id_query)
        result = cursor.fetchall()
        for row in result:
            if(row[0] == user_id):
                sql = "UPDATE Item SET Item_Aval =%s, holder_id =%s WHERE id =%s" % (1, 0, item_id)
                #val = ('', '', '', '', 1, '')
                mycursor.execute(sql)
                mydb.commit()
        print("Congrats you've checked in an item!")

# "Done"
def AttendEvent():
    mycursor = mydb.cursor()
    eventID = int(input("What is the event ID? "))
    userID = int(input("What is your user ID? "))
    
    select_event_time_query = "SELECT event_id, start_dt_time FROM Event"
    with mydb.cursor() as cursor:
        cursor.execute(select_event_time_query)
        result = cursor.fetchall()
        for row in result:
            if(eventID == row[0]):
                print("This event will start at:" + row[1])
    sql = 'INSERT INTO `Event` (`event_id`,`participant_id`,start_dt_time) VALUES (%s, %s, %s)'
    val = (None, userID, '')
    mycursor.execute(sql,val)
    mydb.commit()
    print("You have been registered for the event!")

# "Done"
def AddEvent():
    mycursor = mydb.cursor()
    make_event_id = input("What would you like the event ID to be?")
    make_event_time = input("What time is the event starting?")
    #Possible interaction with other user ids to make sure that they don't match
    sql = 'INSERT INTO `Event` (`event_id`,`participant_id`,start_dt_time) VALUES (%s, %s, %s)'
    val = (make_event_id, None, make_event_time)
    mycursor.execute(sql,val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")


# Works Correctly -- add error for invalid id
def CheckItemAvailable():
    itemID = int(input("What is the item id you're looking for? "))
    select_item_id_query = "SELECT id, Item_Aval, itemName FROM Item"
    with mydb.cursor() as mycursor:
        mycursor.execute(select_item_id_query)
        result = mycursor.fetchall()
        for row in result:
            if(row[0] == itemID):
                if(row[1] == True):
                    print(row[2] + ' is available! Ask one of our librarians if you would like help finding it!')
                else:
                    print(row[2] + ' is checked out, sorry!')

#This Works
def remove_item():
    mycursor = mydb.cursor()
    libcheck = check_librarian_id()
    if libcheck == True:
        print("State the Item ID you would like to remove: ", end='')
        itemID = int(input())
        sql = 'DELETE FROM `Item` WHERE id=%s' % (itemID)
        mycursor.execute(sql)
        print("Item has been removed.")
    else:
        print("Only librarians may remove items.")
    mydb.commit()

#------------ Aggregate Functions -----------------#
# Can't do it until andrew does add item -- error checking with invalid item ids
def getItemRating():
    print('Input the item ID you\'d like to see the rating of: ', end='')
    itemID = int(input())
    select_item_id_query = "SELECT id, itemName, rating FROM Item"
    with mydb.cursor() as mycursor:
        mycursor.execute(select_item_id_query)
        result = mycursor.fetchall()
        for row in result:
            if(row[0] == itemID):
                print('\nItem with ID ' + str(row[0]) + ' is called ' + row[1] + '. It is rated ' + str(row[2]) +'/100 by other customers!\n')

#Works Cureently
def getItemRanking():
    print('What number of items would you like to see ranked? ', end = '')
    numItems = int(input())
    select_item_id_query = 'SELECT * FROM `Item` ORDER BY rating DESC'
    #sql = 'ORDER BY rating'
    with mydb.cursor() as mycursor:
        mycursor.execute(select_item_id_query)
        result = mycursor.fetchall()
        count = 1
        print('\nRanking items by their item rating!')
        for row in result:
            if(count > numItems):
                break
            print('RANK ' + str(count) + ' ITEM')
            print('Name: ', row[2])
            print('Availability: Available' if row[4] == True else 'Availability: Unavailable')
            print('Rating: ', str(row[3]))
            count = count + 1
            print()

def addItem() :
    mycursor = mydb.cursor()
    make_librarian = check_librarian_id()
    sql = ''
    val = None
    if(make_librarian):

        itemID = input("Please enter the items unique ID: ")
        itemName = input("Please enter the items name: ")
        itemGenre = input("Please enter the items genre: ")
        itemType = input("Please enter the items type: ")


        if itemType == "Book" :
            sql = 'INSERT INTO Item (id,genre, itemName, rating, Item_Aval, holder_id) VALUES (%s,%s, %s, %s, %s, %s)'
            val = (itemID, itemGenre, itemName, None, 1, None)
        elif itemType == "Magazine" :
            sql = 'INSERT INTO Item (id,genre, itemName, rating, Item_Aval, holder_id) VALUES (%s,%s, %s, %s, %s, %s)'
            val = (itemID, itemGenre, itemName, None, 1, None)
        elif itemType == "Album" :
            sql = 'INSERT INTO Item (id,genre, itemName, rating, Item_Aval, holder_id) VALUES (%s,%s, %s, %s, %s, %s)'
            val = (itemID, itemGenre, itemName, None, 1, None)
        elif itemType == "Movie" :
            sql = 'INSERT INTO Item (id,genre, itemName, rating, Item_Aval, holder_id) VALUES (%s,%s, %s, %s, %s, %s)'
            val = (itemID, itemGenre, itemName, None, 1, None)
        else:
            print("The is no item type " + itemType + ". This function is aborting. Please try again.")
            quit()
        print("Item has been added sucessfully!")
        mycursor.execute(sql, val)
        mydb.commit()
    else:
        print("You are not a librarian!")
        quit()

def viewItems() :
    mycursor = mydb.cursor()
    uID = input("Please enter the users id.")

    sql = 'SELECT id, itemName FROM Item WHERE holder_id=%s' % (uID)

    mycursor.execute(sql)
    records = mycursor.fetchall()

    print("\nItems you have checked out:")
    for row in records :
        print("Item ID: ", row[0])
        print("Name: ", row[1])
        print("\n")

def viewEvent():
    mycursor = mydb.cursor()
    eID = input("Please enter the event id.")

    sql = 'SELECT start_dt_time FROM Event WHERE event_id=%s' % (eID)
    #val = (eID)
    mycursor.execute(sql)
    row = mycursor.fetchall()
    
    print("The event start time is", row[0])

def choice_person(user_login):
    user_choice = int(input("Please choose one of the options: "))
    if(user_choice == 0):
        print("\nThanks for coming to the library! We hope you enjoyed your stay!")
        quit()
    elif(user_choice == 1):
        user_login = user_sign_in()
    elif(user_choice == 2):
        check_out_item(user_login)
    elif(user_choice == 3):
        check_in_item(user_login)
    elif(user_choice == 4):
        AddEvent()
    elif(user_choice == 5):
        AttendEvent()
    elif(user_choice == 6):
        viewEvent()
    elif(user_choice == 7):
        CheckItemAvailable()
    elif(user_choice == 8):
        addItem()
    elif(user_choice == 9):
        remove_item()
    elif(user_choice == 10):
        viewItems()
    elif(user_choice == 11):
        getItemRating()
    elif(user_choice == 12):
        getItemRanking()
        
    return user_login,user_choice
#Something
def runner_trackstar():
    #displayMain()
   
    user_login = False
    choice_user = 1
    while(True):
        if(choice_user != 0):
            displayMain()
            user_login,choice_user = choice_person(user_login)
        else:
            quit()
            break



if __name__ == "__main__":
    initDB()
    runner_trackstar()


