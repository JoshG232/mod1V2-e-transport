"""Importing splite3 and creating the database"""
import sqlite3 
conn = sqlite3.connect("database.db") #Connecting the database
c = conn.cursor() #Creating the cursor so that processes can be carried out

"""The objects are being imported from another file to 
   the help with structure and organisation"""

from objects import CargoOwner, Driver, TransportCompany, Order
"""Importing a libary of geopy so that a location can be found
   when someone puts in a city"""

from geopy.geocoders import Nominatim
import geopy.distance
"""Function to create the tables for the database
   if the tables have already been created the 
   the function wont be called if there is already tables """

def createTables():
    
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
    choice = int(input("Enter selection: "))
    if choice == 1:
        login(typeChoice)
    if choice == 2:
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
    
    username = input("Enter username: ")
    if typeChoice == 1:
        c.execute('SELECT * FROM cargoOwner WHERE username=:username', {"username":username})
        usernameSelected = c.fetchone()
        if usernameSelected == None:
            print("Username not in database please register")
            loginOrRegister(typeChoice)
        else:
            password = input("Enter password: ")
            if password == usernameSelected[1]:
                mainCargoOwner(usernameSelected)
            else:
                print("Password incorrect try again")
                loginOrRegister(typeChoice)
    if typeChoice == 2:
        c.execute('SELECT * FROM driver WHERE username=:username', {"username":username})
        usernameSelected = c.fetchone()
        if usernameSelected == None:
            print("Username not in database please register")
            loginOrRegister(typeChoice)
        else:
            password = input("Enter password: ")
            if password == usernameSelected[1]:
                mainDriver(usernameSelected)
            else:
                print("Password incorrect try again")
                loginOrRegister(typeChoice)
    if typeChoice == 3:
        c.execute('SELECT * FROM transportCompany WHERE username=:username', {"username":username})
        usernameSelected = c.fetchone()
        if usernameSelected == None:
            print("Username not in database please register")
            loginOrRegister(typeChoice)
        else:
            password = input("Enter password: ")
            if password == usernameSelected[1]:
                mainTransportCompany(usernameSelected)
            else:
                print("Password incorrect try again")
                loginOrRegister(typeChoice)

"""Registering the cargo owner with inputted data values from the
   user"""
def registerCargoOwner():
    
    username = input("Enter username: ")
    password = input("Enter password: ")
    tempObj = CargoOwner(username,password,"Cargo Owner")
    
    with conn:
        c.execute('INSERT INTO cargoOwner VALUES (:username,:password,:personType)',{"username":tempObj.username,"password":tempObj.password,"personType":tempObj.personType})
    
    loginOrRegister(1)

"""Registering the driver with inputted data values from the
   user"""
def registerDriver():
    
    username = input("Enter username: ")
    password = input("Enter password: ")
    lorryDetails = input("Enter lorry details: ")
    driverDetails = input("Enter driver details: ")
    company = input("Enter company name: ")
    tempObj = Driver(username,password,"Cargo Owner",lorryDetails,driverDetails,company)
    with conn:
        c.execute('INSERT INTO driver VALUES (:username,:password,:personType,:lorryDetails,:driverDetails,:company,:orderListDriver)',{"username":tempObj.username,"password":tempObj.password,"personType":tempObj.personType,"lorryDetails":tempObj.lorryDetails,"driverDetails":tempObj.driverDetails,"company":tempObj.company,"orderListDriver":tempObj.orderListDriver})
    
    loginOrRegister(2)

"""Registering the transport company with inputted data values from the
   user"""
def registerTransportCompany():
    
    username = input("Enter username: ")
    password = input("Enter password: ")
    tempObj = TransportCompany(username,password,"Transport Company")
    with conn:
        c.execute('INSERT INTO transportCompany VALUES (:username,:password,:personType,:orderList)',{"username":tempObj.username,"password":tempObj.password,"personType":tempObj.personType,"orderList":tempObj.orderList})
    
    loginOrRegister(3)

"""The main functionality for the cargo owner is done in this function
   so calculating the shipping price and sending the cargo to a transport
   company"""
def mainCargoOwner(user):
    
    cargoOwner = CargoOwner(user[0],user[1],user[2])
    
    print("""
        What would you like to do
        1: Calculate shipping rates
        2: Send cargo
        3: Check status of cargo
        4: Log out
        """)

    choice = int(input("Enter selection: "))
    if choice == 1:
        #Method "calShipping" is called to calculate the price of shipping
        cargoOwner.calShipping()

        #Function is called again to loop back
        mainCargoOwner(user)

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
    driver = Driver(user[0],user[1],user[2],user[3],user[4],user[5])
    #Displaying the main functions 
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
    if choice == 1:
        company = user[5]
        c.execute('SELECT orderList FROM transportCompany WHERE username=:username', {"username":company})
        array = c.fetchall()
        try:
            orderList = array[0]
        except:
            print("No orders")
            mainDriver(user)
        driver.viewAndAcceptOrders(orderList)
        
        for x in orderList:
            c.execute('SELECT * FROM orders WHERE orderID=:orderID AND driverAccepted=:driverAccepted', {"orderID":x,"driverAccepted":"False"})
            y = c.fetchone()
            if y == None:
                pass
            else:
                print("Order",x,y)
        print("""
        Type in the order number for selection or Type Exit to leave
        """)
        selection = input("Enter selection: ")
        if selection == "Exit":
            print("Exit")
            
            

        else:
            
            username = user[0]
            c.execute('SELECT orderListDriver FROM driver WHERE username=:username', {"username":username})
            listOfOrders = c.fetchone()
            
            if listOfOrders[0] == "":
                listOfOrders = selection
                with conn:
                    c.execute("""UPDATE driver SET orderListDriver = :orderListDriver
                            WHERE username = :username""",
                            {'username':username,'orderListDriver':listOfOrders}
                    )
            else:
                
                valueOrder = listOfOrders[0] + "," + str(selection)
                with conn:
                    c.execute("""UPDATE driver SET orderListDriver = :orderListDriver
                            WHERE username = :username""",
                            {'username':username,'orderListDriver':valueOrder}
                    
                    )
                
            with conn:
                    c.execute("""UPDATE orders SET driverAccepted = :driverAccepted
                            WHERE orderID = :orderID""",
                            {'orderID':selection,'driverAccepted':"True"}
                    
                    )
            """Updating transport company orderList"""
            company = user[5]
            
            with conn:
                c.execute("SELECT orderList FROM transportCompany WHERE username=:username",{"username":company})
                orderList = c.fetchone()
                orderList = list(orderList)
                orderListStr = orderList[0]
                orderListStr = orderListStr.split(",")
                print(orderListStr)
                
                orderListStr.remove(selection)
                print(orderListStr)
                tempList = ""
                for x in orderListStr:
                    tempList = tempList + str(x) + ","
                tempList = tempList[:-1]
                print(tempList)
                c.execute("""UPDATE transportCompany SET orderList= :orderList
                            WHERE username = :username""",
                            {'username':company,'orderList':tempList}
                    )


        mainDriver(user)
    if choice == 2:
        
        username = user[0]
        c.execute("SELECT orderListDriver FROM driver WHERE username=:username", {"username":username})
        orderListDriver = c.fetchone()

        orderListDriver = orderListDriver[0]
        if orderListDriver == "":
            print("You have no orders")
            mainDriver(user)
        
        orderListDriverStr = "".join(orderListDriver)
        orderListDriver = orderListDriverStr.split(",")
        
        for x in orderListDriver:
            c.execute('SELECT * FROM orders WHERE orderID=:orderID', {"orderID":x})
            selectedOrder = c.fetchone()
            print("Order ",x,selectedOrder)
        mainDriver(user)
    if choice == 3:

        username = user[0]
        c.execute("SELECT orderListDriver FROM driver WHERE username=:username", {"username":username})
        orderListDriver = c.fetchone()
        orderListDriver = orderListDriver[0]
        orderListDriverStr = "".join(orderListDriver)
        orderListDriver = orderListDriverStr.split(",")
        for x in orderListDriver:
            c.execute('SELECT * FROM orders WHERE orderID=:orderID', {"orderID":x,})
            selectedOrder = c.fetchone()
            print("Order ",x,selectedOrder)
        selection = input("Enter order number for completion: ")
        with conn:
                c.execute("""UPDATE orders SET completed = :completed
                        WHERE orderID = :orderID""",
                        {'orderID':selection,'completed':"True"}
                )
        try:
            orderListDriver.remove(selection)
        except:
            print("Entered value not in list")
            mainDriver(user)

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
    transportCompany = TransportCompany(user[0],user[1],user[2])
    print("""
        1: View orders for drivers
        2: View available orders
        3: Log out
        """)
    try:
        choice = int(input("Enter selection: "))
    except:
        print("Invaild selection")
        mainTransportCompany(user)
    if choice == 1:
        print("    Viewing orders")
        username = user[0]
        with conn:
            c.execute("SELECT username,orderListDriver FROM driver WHERE company=:company",{"company":username})
            driverList = c.fetchall()
            transportCompany.showCustomerOrders(driverList)
        mainTransportCompany(user)
    if choice == 2:
        print("Displaying orders")
        c.execute("SELECT start,end,miles,weight,orderID FROM orders WHERE accepted=:accepted AND driverAccepted=:driverAccepted",{"accepted":"False","driverAccepted":"False"})
        listOfOrders = c.fetchall()
        transportCompany.sendOrder(listOfOrders)
        try:
            orderSelect = int(input("Select orderID : "))
            acceptingOrder(orderSelect,user)
        except:
            mainTransportCompany(user)
    if choice == 3:
        main()
        
"""Once an order has been selected it needs to be updated in the database
   This function is where it is updated"""

def acceptingOrder(orderSelect,user):  
    
    username = user[0]
    c.execute('SELECT orderList FROM transportCompany WHERE username=:username', {"username":username})
    listOfOrders = c.fetchone()
    
    
    if listOfOrders[0] == "":
        
        listOfOrders = orderSelect
        with conn:
            c.execute("""UPDATE transportCompany SET orderList = :orderList
                    WHERE username = :username""",
                    {'username':username,'orderList':listOfOrders}
            )
    else:
        valueOrder = listOfOrders[0] + "," + str(orderSelect)
        with conn:
            c.execute("""UPDATE transportCompany SET orderList = :orderList
                    WHERE username = :username""",
                    {'username':username,'orderList':valueOrder}
            
            )
    with conn:
            c.execute("""UPDATE orders SET accepted = :accepted
                    WHERE orderID = :orderID""",
                    {'orderID':orderSelect,'accepted':"True"}
            
            )
    mainTransportCompany(user)
"""Main function to start the program and find out what type of 
   user they are"""               
def main():
    print("""
        Select type of user
        1:Cargo Owner
        2:Driver
        3:Transport Company
        4:Exit
        """)
    typeChoice = int(input("Enter selection: "))
    if typeChoice == 1:
        loginOrRegister(typeChoice)
    elif typeChoice == 2:
        loginOrRegister(typeChoice)
    elif typeChoice == 3:
        loginOrRegister(typeChoice)
    elif typeChoice == 4:
        exit()
        
    else:
        print("Invalid input, try again")
        main()



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
