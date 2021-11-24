"""Importing splite3 and creating the database"""
import sqlite3 
conn = sqlite3.connect("database.db") #Connecting the database
c = conn.cursor() #Creating the cursor so that processes can be carried out

"""The objects are being imported from another file to 
   the help with structure and organisation"""
from objects import CargoOwner, Driver, TransportCompany, Order


"""Function to create the tables for the database
   if the tables have already been created the 
   the function wont be called if there is already tables """

def createTables():
    #Creating the tables if they aren't already made
    c.execute(""" CREATE TABLE IF NOT EXISTS cargoOwner (
        username text,
        password text,
        personType text
    )
    """)
    c.execute(""" CREATE TABLE IF NOT EXISTS driver (
        username text,
        password text,
        personType text,
        lorryDetails text,
        driverDetails text,
        company text,
        orderListDriver text
    )
    """)
    c.execute(""" CREATE TABLE IF NOT EXISTS transportCompany (
        username text,
        password text,
        personType text,
        orderList text
    )
    """)
    c.execute(""" CREATE TABLE IF NOT EXISTS orders (
        start text,
        end text,
        miles real,
        weight real,
        orderID integer,
        accepted text,
        driverAccepted text,
        completed text
    )
    """)

"""After the user selects what type of user they are
   they are asked to login or register. Depending on
   on what they selected will be what function is run"""
def loginOrRegister(typeChoice):
    print("""
        1:Login
        2:Register
        3:Back
        """)
    try:
        choice = int(input("Enter selection: "))
    except:
        print("Invalid input.Try again")
        loginOrRegister(typeChoice)
    #checking if the user wants to login,register or exit
    if choice == 1:
        login(typeChoice)
    if choice == 2:
        #Depending on what type of user they are will be what function runs
        if typeChoice == 1:
            registerCargoOwner()
        if typeChoice == 2:
            registerDriver()
        if typeChoice == 3:
            registerTransportCompany()
    if choice == 3:
        main()

"""The user is asked for the username and password and checked
   if it is in the database and if they make up so the user can
   continue"""
def login(typeChoice):
    #System gets username off user
    username = input("Enter username: ")
    #Depending on the user type it checks a different table in the database
    
    if typeChoice == 1:
        #Gets user from database from inputted username
        c.execute('SELECT * FROM cargoOwner WHERE username=:username', {"username":username})
        usernameSelected = c.fetchone()
        #If the returned value is empty then the user isn't in the database
        if usernameSelected == None:
            print("Username not in database please register")
            loginOrRegister(typeChoice)
        #If the user is in the database it asks for the password
        else:
            password = input("Enter password: ")
            #Checks if the password is correct
            if password == usernameSelected[1]:
                mainCargoOwner(usernameSelected)
            else:
                print("Password incorrect try again")
                loginOrRegister(typeChoice)
    if typeChoice == 2:
        #Gets user from database from inputted username
        c.execute('SELECT * FROM driver WHERE username=:username', {"username":username})
        usernameSelected = c.fetchone()
        #If the returned value is empty then the user isn't in the database
        if usernameSelected == None:
            print("Username not in database please register")
            loginOrRegister(typeChoice)
        #If the user is in the database it asks for the password
        else:
            password = input("Enter password: ")
            #Checks if the password is correct
            if password == usernameSelected[1]:
                mainDriver(usernameSelected)
            else:
                print("Password incorrect try again")
                loginOrRegister(typeChoice)
    if typeChoice == 3:
        #Gets user from database from inputted username
        c.execute('SELECT * FROM transportCompany WHERE username=:username', {"username":username})
        usernameSelected = c.fetchone()
        #If the returned value is empty then the user isn't in the database
        if usernameSelected == None:
            print("Username not in database please register")
            loginOrRegister(typeChoice)
        #If the user is in the database it asks for the password
        else:
            password = input("Enter password: ")
            #Checks if the password is correct
            if password == usernameSelected[1]:
                mainTransportCompany(usernameSelected)
            else:
                print("Password incorrect try again")
                loginOrRegister(typeChoice)

"""Registering the cargo owner with inputted data values from the
   user"""
def registerCargoOwner():
    #User enters values
    username = input("Enter username: ")
    password = input("Enter password: ")
    #Object is created so it can be entered into database
    tempObj = CargoOwner(username,password,"Cargo Owner")
    #Connects to the database
    with conn:
        #Inserts the cargo owner into the database
        c.execute('INSERT INTO cargoOwner VALUES (:username,:password,:personType)',{"username":tempObj.username,"password":tempObj.password,"personType":tempObj.personType})
    
    loginOrRegister(1)

"""Registering the driver with inputted data values from the
   user"""
def registerDriver():
    #User enters values
    username = input("Enter username: ")
    password = input("Enter password: ")
    lorryDetails = input("Enter lorry details: ")
    driverDetails = input("Enter driver details: ")
    company = input("Enter company name: ")
    #Object is created so it can be entered into database
    tempObj = Driver(username,password,"Cargo Owner",lorryDetails,driverDetails,company)
    #Connects to the database
    with conn:
        #Inserts the driver into the database
        c.execute('INSERT INTO driver VALUES (:username,:password,:personType,:lorryDetails,:driverDetails,:company,:orderListDriver)',{"username":tempObj.username,"password":tempObj.password,"personType":tempObj.personType,"lorryDetails":tempObj.lorryDetails,"driverDetails":tempObj.driverDetails,"company":tempObj.company,"orderListDriver":tempObj.orderListDriver})
    
    loginOrRegister(2)

"""Registering the transport company with inputted data values from the
   user"""
def registerTransportCompany():
    #User enters values
    username = input("Enter username: ")
    password = input("Enter password: ")
    #Object is created so it can be entered into database
    tempObj = TransportCompany(username,password,"Transport Company")
    #Connects to the database
    with conn:
        #Inserts the driver into the database
        c.execute('INSERT INTO transportCompany VALUES (:username,:password,:personType,:orderList)',{"username":tempObj.username,"password":tempObj.password,"personType":tempObj.personType,"orderList":tempObj.orderList})
    
    loginOrRegister(3)

"""The main functionality for the cargo owner is done in this function
   so calculating the shipping price and sending the cargo to a transport
   company"""
def mainCargoOwner(user):
    #Creating the object for the user
    cargoOwner = CargoOwner(user[0],user[1],user[2])
    #Displaying menu
    print("""
        What would you like to do
        1: Calculate shipping rates
        2: Send cargo
        3: Check status of cargo
        4: Log out
        """)

    choice = int(input("Enter selection: "))
    #Choice 1 for getting a price for shipping rates
    if choice == 1:
        #Method "calShipping" is called to calculate the price of shipping
        cargoOwner.calShipping()

        #Function is called again to loop back
        mainCargoOwner(user)
    #Choice 2 for sending cargo off on an order
    if choice == 2:
        #Putting all the values into a list
        x = cargoOwner.placeOrder()
        
        #The orderID being a unique id from the list "x"(OrderID can never be the same)
        orderID = id(x)

        #Creating the temp object
        tempObj = Order(x[0],x[1],x[2],x[3],orderID)

        #Inserting the values into the table of orders
        with conn:
            c.execute('INSERT INTO orders VALUES (:start,:end,:miles,:weight,:orderID,:accepted,:driverAccepted,:completed)',{"start":tempObj.start,"end":tempObj.end,"miles":tempObj.miles,"weight":tempObj.weight,"orderID":tempObj.orderID,"accepted":tempObj.accepted,"driverAccepted":tempObj.driverAccepted,"completed":tempObj.completed})
        print("Order",orderID,"completed")
        mainCargoOwner(user)
    if choice == 3:
        #Getting the order number from the user
        try:
            userOrderId = int(input("What is the orderID number? "))
        except:
            print("Incorrect values inputted")
            mainCargoOwner(user)
        #Using the entered value the order is selected and then checked to see what stage it is at
        with conn:
            c.execute("SELECT accepted,driverAccepted,completed FROM orders WHERE orderID=:orderID",{"orderID":userOrderId})
            order = c.fetchone()
            #Order is being checked if values are set to true
            #Using elif because it only checks the if's once if it is true
            try:
                if order[2] == "True":
                    print("The order has been completed")
                elif order[1] == "True":
                    print("Order has been accepted by the driver")
                elif order[0] == "True":
                    print("Order has been accepted by the transport company")
                else:
                    print("Order hasn't been accepted")
            except:
                print("Incorrect order number. Try again")
        mainCargoOwner(user)
    if choice == 4:
        #Going back to the main function
        main()

"""The main driver functionality"""
def mainDriver(user):
    #Creating the object for the user
    driver = Driver(user[0],user[1],user[2],user[3],user[4],user[5])
    #Displaying the menu
    print("""
    1: View and accept orders
    2: Look at accepted orders
    3: Complete orders
    4: Log out
    """)
    try:
        choice = int(input("Enter selection: "))
    except:
        print("Incorrect selection. try again")
        mainDriver(user)
    #Choice 1 for viewing and accepting orders
    if choice == 1:
        #Getting the company from the user object
        company = user[5]
        #Getting the orders from the company they are with
        c.execute('SELECT orderList FROM transportCompany WHERE username=:username', {"username":company})
        array = c.fetchall()
        #Checking if there is any orders or not
        try:
            orderList = array[0]
        except:
            print("No orders")
            mainDriver(user)
        #calling the method for getting the orderlist ready
        driver.viewAndAcceptOrders(orderList)
        #Displaying the orders in the orderList
        for x in orderList:
            #Selects the order
            c.execute('SELECT * FROM orders WHERE orderID=:orderID AND driverAccepted=:driverAccepted', {"orderID":x,"driverAccepted":"False"})
            y = c.fetchone()
            #Checks if its blank or not
            if y == None:
                pass
            else:
                #Displays the order
                print("Order",x,y)
        print("""
        Type in the order number for selection or Type Exit to leave
        """)
        #Getting the user input
        selection = input("Enter selection: ")
        if selection == "Exit":
            print("Exit")
        else:
            #Getting username from user object
            username = user[0]
            #The order list from the driver is selected
            c.execute('SELECT orderListDriver FROM driver WHERE username=:username', {"username":username})
            listOfOrders = c.fetchone()
            #Checks if the list is empty 
            if listOfOrders[0] == "":
                #Order list is the selection made
                listOfOrders = selection
                #Connects to database
                with conn:
                    #Updates the order list for the driver
                    c.execute("""UPDATE driver SET orderListDriver = :orderListDriver
                            WHERE username = :username""",
                            {'username':username,'orderListDriver':listOfOrders}
                    )
            else:
                #Order list is updated with the selection  
                valueOrder = listOfOrders[0] + "," + str(selection)
                #Connects to database
                with conn:
                    #Updates the order list for the driver
                    c.execute("""UPDATE driver SET orderListDriver = :orderListDriver
                            WHERE username = :username""",
                            {'username':username,'orderListDriver':valueOrder}
                    )
            #Connects to database
            with conn:
                    #Updates status of order by showing the driver has accepted it
                    c.execute("""UPDATE orders SET driverAccepted = :driverAccepted
                            WHERE orderID = :orderID""",
                            {'orderID':selection,'driverAccepted':"True"}
                    )
            """Updating transport company orderList"""
            #Getting company that the driver works for
            company = user[5]
            #Connecting 
            with conn:
                #Getting the order list from the transport company that the driver works for
                c.execute("SELECT orderList FROM transportCompany WHERE username=:username",{"username":company})
                orderList = c.fetchone()
                #List is preped to be worked on
                orderList = list(orderList)
                orderListStr = orderList[0]
                orderListStr = orderListStr.split(",")
                #Selection made by the driver is removed from the list
                orderListStr.remove(selection)
                #List is then made so it can be put back into the database
                tempList = ""
                for x in orderListStr:
                    #The list needs to be in string format for it to be put in the database
                    tempList = tempList + str(x) + ","
                tempList = tempList[:-1]
                #Updates the order list for the transport company
                c.execute("""UPDATE transportCompany SET orderList= :orderList
                            WHERE username = :username""",
                            {'username':company,'orderList':tempList}
                    )
        mainDriver(user)
    if choice == 2:
        #Username is selected from user object
        username = user[0]
        #Order list for driver is selected from database
        c.execute("SELECT orderListDriver FROM driver WHERE username=:username", {"username":username})
        orderListDriver = c.fetchone()
        orderListDriver = orderListDriver[0]
        #Checking if the driver has no orders
        if orderListDriver == "":
            print("You have no orders")
            mainDriver(user)
        #Making the list ready so it can be displayed
        orderListDriverStr = "".join(orderListDriver)
        orderListDriver = orderListDriverStr.split(",")
        #Displaying all the items in the list
        for x in orderListDriver:
            c.execute('SELECT * FROM orders WHERE orderID=:orderID', {"orderID":x})
            selectedOrder = c.fetchone()
            print("Order ",x,selectedOrder)
        mainDriver(user)
    if choice == 3:
        #Getting the username from the user object
        username = user[0]
        #Getting the order list from the driver
        c.execute("SELECT orderListDriver FROM driver WHERE username=:username", {"username":username})
        orderListDriver = c.fetchone()
        #Making the list ready so it can be displayed
        orderListDriver = orderListDriver[0]
        orderListDriverStr = "".join(orderListDriver)
        orderListDriver = orderListDriverStr.split(",")
        #Displaying the orders
        for x in orderListDriver:
            c.execute('SELECT * FROM orders WHERE orderID=:orderID', {"orderID":x,})
            selectedOrder = c.fetchone()
            print("Order ",x,selectedOrder)
        selection = input("Enter order number for completion: ")
        #Connects to database
        with conn:
            #Updates the order to be complete 
            c.execute("""UPDATE orders SET completed = :completed
                    WHERE orderID = :orderID""",
                    {'orderID':selection,'completed':"True"}
            )
        #Removing the order from the order list from the driver
        try:
            orderListDriver.remove(selection)
        except:
            print("Entered value not in list")
            mainDriver(user)
        #Getting the list ready for the database.
        strOrderListDriver = ""
        for x in orderListDriver:
            strOrderListDriver += str(x)
        with conn:
            c.execute("""UPDATE driver SET orderListDriver= :orderListDriver
                        WHERE username = :username""",
                        {'username':username,'orderListDriver':strOrderListDriver}
            )
        mainDriver(user)
    if choice == 4:
        main()

"""The main transport company functionality is done in this function. This would
   be viewing orders for there drives(orders they have selected) and then viewing
   available orders that have been sent by cargo owners """
def mainTransportCompany(user):
    #Creating object for transport company 
    transportCompany = TransportCompany(user[0],user[1],user[2])
    #Displaying menu 
    print("""
        1: View orders for drivers
        2: View available orders
        3: Log out
        """)
    #Getting selection from user
    try:
        choice = int(input("Enter selection: "))
    except:
        print("Invaild selection")
        mainTransportCompany(user)
    if choice == 1:
        print("    Viewing orders")
        #Username from user object
        username = user[0]
        #Connecting to database
        with conn:
            #Selecting all the drivers but only there username and order list
            c.execute("SELECT username,orderListDriver FROM driver WHERE company=:company",{"company":username})
            driverList = c.fetchall()
            #Method for showing the drivers orders
            transportCompany.showDriverOrders(driverList)
        mainTransportCompany(user)
    if choice == 2:

        print("Displaying orders")
        #Getting all the orders that cargo owners have sent out
        c.execute("SELECT start,end,miles,weight,orderID FROM orders WHERE accepted=:accepted AND driverAccepted=:driverAccepted",{"accepted":"False","driverAccepted":"False"})
        listOfOrders = c.fetchall()
        #Method for displaying the orders
        transportCompany.displayOrder(listOfOrders)
        #Selcting the order that the transport company wants
        try:
            orderSelect = int(input("Select orderID : "))
            acceptingOrder(orderSelect,user)
        except:
            print("Invalid input")
            mainTransportCompany(user)
    if choice == 3:
        main()
        
"""Once an order has been selected it needs to be updated in the database
   This function is where it is updated"""

def acceptingOrder(orderSelect,user):  
    #Username from user object
    username = user[0]
    #Getting the order list from the transport company
    c.execute('SELECT orderList FROM transportCompany WHERE username=:username', {"username":username})
    listOfOrders = c.fetchone()
    #Checking if the list is empty or not
    if listOfOrders[0] == "":
        listOfOrders = orderSelect
        #Connecting to database
        with conn:
            #Updating the list with the selected order
            c.execute("""UPDATE transportCompany SET orderList = :orderList
                    WHERE username = :username""",
                    {'username':username,'orderList':listOfOrders}
            )
    else:
        #Add the selected orderID to the list when there are already values
        valueOrder = listOfOrders[0] + "," + str(orderSelect)
        #Conncting to database
        with conn:
            #Updating the list with the seleced order list
            c.execute("""UPDATE transportCompany SET orderList = :orderList
                    WHERE username = :username""",
                    {'username':username,'orderList':valueOrder}
            
            )
    
    with conn:
        #Updating the "accepted" value in the table so the cargo knows the status
        c.execute("""UPDATE orders SET accepted = :accepted
                WHERE orderID = :orderID""",
                {'orderID':orderSelect,'accepted':"True"}
        
        )
    mainTransportCompany(user)
"""Main function to start the program and find out what type of 
   user they are"""               
def main():
    #Displaying menu
    print("""
        Select type of user
        1:Cargo Owner
        2:Driver
        3:Transport Company
        4:Exit
        """)
    #Getting valid input for selection
    try:
        typeChoice = int(input("Enter selection: "))
    except:
        print("Invalid input try again")
        main()
    if typeChoice == 1:
            loginOrRegister(typeChoice)
    if typeChoice == 2:
        loginOrRegister(typeChoice)
    if typeChoice == 3:
        loginOrRegister(typeChoice)
    if typeChoice == 4:
        exit()  
    else:
        print("Invalid input try again")
        main()



#Runing the main function and creating the tables if needed
createTables()
main()



































































































































































# """This function takes the user input and selects if they want to login
#    or register, while also taking the value of "typeChoice" to see if 
#    they are a Cargo Owner,Driver or Transport company"""

# def loginOrRegister(typeChoice):
#     print("""
#         1:Login
#         2:Register
#         """)
#     choice = int(input("Enter selection: "))
#     if choice == 1:
#         login(typeChoice)
#     if choice == 2:
#         if typeChoice == 1:
#             registerCargoOwner()
#         if typeChoice == 2:
#             registerDriver()
#         if typeChoice == 3:
#             registerTransportCompany()

# def login(typeChoice):
#     global loggedIn
    
#     loggedIn = input("Do you want to login")
#     if loggedIn == "Yes":
#         loggedIn = True
#         if typeChoice == 1:
#             mainCargoOwner()
#         if typeChoice == 2:
#             print(2)
#             #mainTransportCompany()
#         if typeChoice == 3:
#             mainTransportCompany()

#     else:
#         loggedIn = False
        
# def registerCargoOwner():
#     username = input("Enter username")
#     password = input("Enter password")
#     tempObj = CargoOwner(username,password,"Cargo Owner")
#     tempObj = vars(tempObj)
    
# def registerDriver():
#     username = input("Enter username")
#     password = input("Enter password")
#     lorryDetails = input("Enter Lorry details")
#     driverDetails = input("Enter driver details")
#     company = input("Enter what company you work for:")
#     tempObj = Driver(username,password,"Driver",driverDetails,lorryDetails,company)
#     tempObj = vars(tempObj)
    

# def registerTransportCompany():
#     username = input("Enter username")
#     password = input("Enter password")
#     tempObj = TransportCompany(username,password,"Transport Company")
#     tempObj = vars(tempObj)
    


# def mainCargoOwner():
#     print("""
#         What would you like to do
#         1: Calculate shipping rates
#         2: Send cargo
#         """)
#     choice = int(input("Enter selection: "))
#     if choice == 1:
#         #Add python locaiton api to help shipping rates
#         try:
#             length = int(input("Enter length: "))
#             width = int(input("Enter width: "))
#             weight = int(input("Enter weight: "))
#             totalPrice = length * width * weight
#             print("The estimate for the cargo is £",totalPrice)
#         except:
#             print("Incorrect values inputted")
#         mainCargoOwner()
#     if choice == 2:
#         start = input("Enter start location: ")
#         end = input("Enter end location: ")
#         weight = int(input("Enter weight: "))
#         miles = int(input("How many miles: "))
#         orderID = int(input("OrderID: "))
#         tempObj = Order(start,end,miles,weight,orderID)
#         tempObj = vars(tempObj)
        

# def mainTransportCompany():
#     print("""
#         1:View orders for drivers
#         2:View available orders)
#         """)
    
#     choice = int(input("Enter selection: "))
#     if choice == 1:
#         print("Choice 1")
#     if choice == 2:
#         print("Displaying orders")
        

# """Main function"""

# def main():
#     print("""
#         Select type of user
#         1:Cargo Owner
#         2:Driver
#         3:Transport Company
#         """)
#     typeChoice = int(input("Enter selection: "))
#     if typeChoice == 1:
#         loginOrRegister(typeChoice)
#     elif typeChoice == 2:
#         loginOrRegister(typeChoice)
#     elif typeChoice == 3:
#         loginOrRegister(typeChoice)
#     else:
#         print("Invalid input, try again")
#         main()
# main()
