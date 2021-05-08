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
    print("4: Attend Event")
    print("5: Check Item Availability")
    #Could be hidden from main menu or reject it if they're a customer
    print("6: Remove Item")
    print("7: Add Item")
    print("8: Send Overdue Notice")
    print("9: Send Event Notice")

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
    user_id = int(input("What is your user ID?"))
    pass_word = input("What is your password? ")
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
            if(isinstance(item_id,int) or row[0] == 0):
                print("We are very sorry but either the item id is invalid or the item is checked out")
            else:
                 sql = "INSERT INTO Item (id, genre, itemName, rating, Item_Aval, holder_id) VALUES (%s, %s, %s, %s, %s, %s)"
                 val = ('', '', '', '', 0, user_id)
                 mycursor.execute(sql,val)
                 mydb.commit()
                 print(mycursor.rowcount, "record inserted.")

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
                sql = "INSERT INTO Item (id, genre, itemName, rating, Item_Aval, holder_id) VALUES (%s, %s, %s, %s, %s, %s)"
                val = ('', '', '', '', 1, '')
                mycursor.execute(sql,val)
                mydb.commit()
                print(mycursor.rowcount, "record inserted.")

# "Done"
def AttendEvent():
    mycursor = mydb.cursor()
    eventID = int(input())
    userID = int(input())
    sql = 'INSERT INTO `Event` (`event_id`,`participant_id`,start_dt_time,end_dt_tm,notice) VALUES (%s, %s, %s, %s, %s)'
    print("You have been registered for the event!")
    val = (eventID, userID, "2017-07-23","2017-07-23", "2017-07-23")
    mycursor.execute(sql,val)
    mydb.commit()


# Works Correctly -- add error for invalid id
def CheckItemAvailable():
    itemID = int(input())
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
                print('Item with ID ' + str(row[0]) + ' is called ' + row[1] + '. It is rated ' + str(row[2]) +' by other customers!')
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
        print('Ranking items by times they have been checked out!')
        for row in result:
            if(count > numItems):
                break
            print('RANK ' + str(count) + ' ITEM')
            print('Name: ', row[2])
            print('Availability: ' + 'Available' if row[4] == True else 'Unavailable')
            print('Rating: ', str(row[3]))
            print('Times checked out: ', str(row[6]))
            count = count + 1
            print()

#Something
def runner_trackstar():
    displayMain()
    user_choice = int(input("Please choose one of the options: "))
    user_login = False
    #python doesn't have switch statements
    if(user_choice == 0):
        print("It's time to go buddy")
        quit()
    elif(user_choice == 1):
        user_login = user_sign_in()
        displayMain()
        anotha_one = int(input("Please choose another choice"))
    elif(user_choice == 2):
        check_out_item(user_login)
    elif(user_choice == 3):
        check_in_item(user_login)
    elif(user_choice == 4):
        AttendEvent()
    elif(user_choice == 5):
        CheckItemAvailable()
        getItemRating()
        getItemRanking()
    elif(user_choice == 6):
        remove_item()
    #elif(user_choice == 7):
#
    #elif(user_choice == 8):
        #
    #elif(user_choice == 9):
        #


if __name__ == "__main__":
    initDB()
    runner_trackstar()


