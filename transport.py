"""Importing splite3 and creating the database"""
import sqlite3 
conn = sqlite3.connect("database.db")
c = conn.cursor() #Creating the cursor so that processes can be carried out

from objects import CargoOwner, Driver, TransportCompany, Order

"""Function to create the tables for the database
   if the tables have already been created the 
   the function wont be called if there is already tables """
def createTables():
    c.execute(""" CREATE TABLE cargoOwner (
        username text,
        password text,
        personType text
    )
    """)
    c.execute(""" CREATE TABLE driver (
        username text,
        password text,
        personType text,
        lorryDetails text,
        driverDetails text,
        company text,
        orderListDriver text
    )
    """)
    c.execute(""" CREATE TABLE transportCompany (
        username text,
        password text,
        personType text,
        orderList text
    )
    """)
    
    c.execute(""" CREATE TABLE orders (
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
 
"""The user is asked for the username and password and checked
   if it is in the database and if they make up so the user can
   continue"""
def login(typeChoice):
    print("Login")
    username = input("Enter username: ")
    if typeChoice == 1:
        c.execute('SELECT * FROM cargoOwner WHERE username=:username', {"username":username})
        usernameSelected = c.fetchone()
        if usernameSelected == None:
            print("Username not in database please register")
        else:
            password = input("Enter password: ")
            if password == usernameSelected[1]:
                mainCargoOwner(usernameSelected)
            else:
                print("Password incorrect try again")
                login(typeChoice)
    if typeChoice == 2:
        c.execute('SELECT * FROM driver WHERE username=:username', {"username":username})
        usernameSelected = c.fetchone()
        if usernameSelected == None:
            print("Username not in database please register")
        else:
            password = input("Enter password: ")
            if password == usernameSelected[1]:
                mainDriver(usernameSelected)
            else:
                print("Password incorrect try again")
                login(typeChoice)
    if typeChoice == 3:
        c.execute('SELECT * FROM transportCompany WHERE username=:username', {"username":username})
        usernameSelected = c.fetchone()
        if usernameSelected == None:
            print("Username not in database please register")
        else:
            password = input("Enter password: ")
            if password == usernameSelected[1]:
                mainTransportCompany(usernameSelected)
            else:
                print("Password incorrect try again")
                login(typeChoice)

"""Registering the cargo owner with inputted data values from the
   user"""
def registerCargoOwner():
    print("registerCargoOwner")
    username = input("Enter username: ")
    password = input("Enter password: ")
    tempObj = CargoOwner(username,password,"Cargo Owner")
    with conn:
     c.execute('INSERT INTO cargoOwner VALUES (:username,:password,:personType)',{"username":tempObj.username,"password":tempObj.password,"personType":tempObj.personType})
    
    loginOrRegister(1)

"""Registering the driver with inputted data values from the
   user"""
def registerDriver():
    print("registerDriver")
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
    print("registerTransportCompany")
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

    print("mainCargoOwner")
    print("""
        What would you like to do
        1: Calculate shipping rates
        2: Send cargo
        """)
    choice = int(input("Enter selection: "))
    if choice == 1:
        #Add python locaiton api to help shipping rates
        try:
            length = int(input("Enter length: "))
            width = int(input("Enter width: "))
            weight = int(input("Enter weight: "))
            totalPrice = length * width * weight
            print("The estimate for the cargo is £",totalPrice)
        except:
            print("Incorrect values inputted")
        mainCargoOwner(user)
    if choice == 2:
        start = input("Enter start location: ")
        end = input("Enter end location: ")
        weight = int(input("Enter weight: "))
        miles = int(input("How many miles: "))
        orderID = int(input("OrderID: "))
        tempObj = Order(start,end,miles,weight,orderID)
        with conn:
            c.execute('INSERT INTO orders VALUES (:start,:end,:miles,:weight,:orderID,:accepted,:driverAccepted,:completed)',{"start":tempObj.start,"end":tempObj.end,"miles":tempObj.miles,"weight":tempObj.weight,"orderID":tempObj.orderID,"accepted":tempObj.accepted,"driverAccepted":tempObj.driverAccepted,"completed":tempObj.completed})
        
        mainCargoOwner(user)
"""The main driver functionality"""

def mainDriver(user):
    print("mainDriver")
    print("""
    1:View and accept orders
    2:Look at accepted orders
    3:Complete orders
    """)
    choice = int(input("Enter selection: "))
    if choice == 1:
        company = user[5]
        c.execute('SELECT orderList FROM transportCompany WHERE username=:username', {"username":company})
        array = c.fetchall()
        orderList = array[0]
        orderListStr = "".join(orderList)
        orderList = list(orderListStr)
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
            print("else")
            username = user[0]
            c.execute('SELECT orderListDriver FROM driver WHERE username=:username', {"username":username})
            listOfOrders = c.fetchone()
            print(listOfOrders)
            if listOfOrders == None:
                listOfOrders = selection
                with conn:
                    c.execute("""UPDATE driver SET orderListDriver = :orderListDriver
                            WHERE username = :username""",
                            {'username':username,'orderListDriver':listOfOrders}
                    )
            else:
                print("Here")
                valueOrder = listOfOrders[0] + str(selection)
                with conn:
                    c.execute("""UPDATE driver SET orderListDriver = :orderListDriver
                            WHERE username = :username""",
                            {'username':username,'orderListDriver':valueOrder}
                    
                    )
                print(listOfOrders)
            with conn:
                    c.execute("""UPDATE orders SET driverAccepted = :driverAccepted
                            WHERE orderID = :orderID""",
                            {'orderID':selection,'driverAccepted':"True"}
                    
                    )
            #Updating transport company orderList
            company = user[5]
            
            with conn:
                c.execute("SELECT orderList FROM transportCompany WHERE username=:username",{"username":company})
                orderList = c.fetchone()
                orderList = list(orderList)
                orderList = list(orderList[0])
                print(orderList)
                orderList.remove(selection)
                strOrderList = ""
                for x in orderList:
                    strOrderList += str(x)

                c.execute("""UPDATE transportCompany SET orderList= :orderList
                            WHERE username = :username""",
                            {'username':company,'orderList':strOrderList}
                    )


        mainDriver(user)
    if choice == 2:
        
        username = user[0]
        c.execute("SELECT orderListDriver FROM driver WHERE username=:username", {"username":username})
        orderListDriver = c.fetchone()
        orderListDriver = list(orderListDriver)
        orderListDriver = orderListDriver[0]
        orderListDriver = list(orderListDriver)
        print(orderListDriver)
        for x in orderListDriver:
            c.execute('SELECT * FROM orders WHERE orderID=:orderID', {"orderID":x})
            selectedOrder = c.fetchone()
            print("Order ",x,selectedOrder)
    if choice == 3:
        username = user[0]
        c.execute("SELECT orderListDriver FROM driver WHERE username=:username", {"username":username})
        orderListDriver = c.fetchone()
        orderListDriver = list(orderListDriver)
        orderListDriver = orderListDriver[0]
        orderListDriver = list(orderListDriver)
        print(orderListDriver)
        for x in orderListDriver:
            c.execute('SELECT * FROM orders WHERE orderID=:orderID AND completed=:completed', {"orderID":x,"completed":"False"})
            selectedOrder = c.fetchone()
            print("Order ",x,selectedOrder)
        selection = input("Enter order number for completion: ")
        with conn:
                c.execute("""UPDATE orders SET completed = :completed
                        WHERE orderID = :orderID""",
                        {'orderID':selection,'completed':"True"}
                )
        mainDriver()
"""The main transport company functionality is done in this function. This would
   be viewing orders for there drives(orders they have selected) and then viewing
   available orders that have been sent by cargo owners """
def mainTransportCompany(user):
    print("mainTransportCompany")
    print("""
        1:View orders for drivers
        2:View available orders)
        """)
    
    choice = int(input("Enter selection: "))
    if choice == 1:
        print("Viewing orders")
        mainTransportCompany()
    if choice == 2:
        count = 0
        print("Displaying orders")
        c.execute("SELECT start,end,miles,weight,orderID FROM orders WHERE accepted=:accepted AND driverAccepted=:driverAccepted",{"accepted":"False","driverAccepted":"False"})
        listOfOrders = c.fetchall()
        for i in listOfOrders:
            print("Order",i[4],":",i)
            count += 1
        orderSelect = int(input("Select orderID : "))
        acceptingOrder(orderSelect,user)
        mainTransportCompany(user)
"""Once an order has been selected it needs to be updated in the database
   This function is where it is updated"""
def acceptingOrder(orderSelect,user):  
    print("acceptingORder")
    username = user[0]
    c.execute('SELECT orderList FROM transportCompany WHERE username=:username', {"username":username})
    listOfOrders = c.fetchone()
    print(listOfOrders)
    if listOfOrders == None:
        listOfOrders = orderSelect
        with conn:
            c.execute("""UPDATE transportCompany SET orderList = :orderList
                    WHERE username = :username""",
                    {'username':username,'orderList':listOfOrders}
            )
    else:
        print("Here")
        valueOrder = listOfOrders[0] + str(orderSelect)
        with conn:
            c.execute("""UPDATE transportCompany SET orderList = :orderList
                    WHERE username = :username""",
                    {'username':username,'orderList':valueOrder}
            
            )
        print(listOfOrders)
    with conn:
            c.execute("""UPDATE orders SET accepted = :accepted
                    WHERE orderID = :orderID""",
                    {'orderID':orderSelect,'accepted':"True"}
            
            )

"""Main function to start the program and find out what type of 
   user they are"""               
def main():
    print("""
        Select type of user
        1:Cargo Owner
        2:Driver
        3:Transport Company
        """)
    typeChoice = int(input("Enter selection: "))
    if typeChoice == 1:
        loginOrRegister(typeChoice)
    elif typeChoice == 2:
        loginOrRegister(typeChoice)
    elif typeChoice == 3:
        loginOrRegister(typeChoice)
    else:
        print("Invalid input, try again")
        main()

# main()
# mainDriver()
# mainCargoOwner()
# mainTransportCompany()




createTables()



































































































































































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
