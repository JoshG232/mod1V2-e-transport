import sqlite3
conn = sqlite3.connect("database.db")
c = conn.cursor()
from objects import CargoOwner, Driver, TransportCompany, Order


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
        accepted text
    )
    """)

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
                mainCargoOwner()
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
                mainDriver()
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
                mainTransportCompany()
            else:
                print("Password incorrect try again")
                login(typeChoice)

def registerCargoOwner():
    print("registerCargoOwner")
    username = input("Enter username: ")
    password = input("Enter password: ")
    tempObj = CargoOwner(username,password,"Cargo Owner")
    c.execute('INSERT INTO cargoOwner VALUES (:username,:password,:personType)',{"username":tempObj.username,"password":tempObj.password,"personType":tempObj.personType})
    conn.commit()
    conn.close()

def registerDriver():
    print("registerDriver")
    username = input("Enter username: ")
    password = input("Enter password: ")
    lorryDetails = input("Enter lorry details: ")
    driverDetails = input("Enter driver details: ")
    company = input("Enter company name: ")
    tempObj = Driver(username,password,"Cargo Owner",lorryDetails,driverDetails,company)
    c.execute('INSERT INTO driver VALUES (:username,:password,:personType,:lorryDetails,:driverDetails,:company,:orderListDriver)',{"username":tempObj.username,"password":tempObj.password,"personType":tempObj.personType,"lorryDetails":tempObj.lorryDetails,"driverDetails":tempObj.driverDetails,"company":tempObj.company,"orderListDriver":tempObj.orderListDriver})
    conn.commit()
    conn.close()

def registerTransportCompany():
    print("registerTransportCompany")
    username = input("Enter username: ")
    password = input("Enter password: ")
    tempObj = TransportCompany(username,password,"Transport Company")
    c.execute('INSERT INTO transportCompany VALUES (:username,:password,:personType,:orderList)',{"username":tempObj.username,"password":tempObj.password,"personType":tempObj.personType,"orderList":tempObj.orderList})
    conn.commit()
    conn.close()
 
def mainCargoOwner():
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
        mainCargoOwner()
    if choice == 2:
        start = input("Enter start location: ")
        end = input("Enter end location: ")
        weight = int(input("Enter weight: "))
        miles = int(input("How many miles: "))
        orderID = int(input("OrderID: "))
        tempObj = Order(start,end,miles,weight,orderID)
        c.execute('INSERT INTO orders VALUES (:start,:end,:miles,:weight,:orderID,:accepted)',{"start":tempObj.start,"end":tempObj.end,"miles":tempObj.miles,"weight":tempObj.weight,"orderID":tempObj.orderID,"accepted":tempObj.accepted})
        conn.commit()
        conn.close()

def mainDriver():
    print("mainDriver")

def mainTransportCompany():
    print("mainTransportCompany")
    print("""
        1:View orders for drivers
        2:View available orders)
        """)
    
    choice = int(input("Enter selection: "))
    if choice == 1:
        print("Viewing orders")
    if choice == 2:
        count = 0
        print("Displaying orders")
        c.execute("SELECT start,end,miles,weight,orderID FROM orders WHERE accepted=:accepted",{"accepted":"False"})
        listOfOrders = c.fetchall()
        for i in listOfOrders:
            print("Order",i[4],":",i)
            count += 1
        orderSelect = int(input("Select orderID : "))
        acceptingOrder(orderSelect)

def acceptingOrder(orderSelect):
    print("acceptingORder")
    username = input("Enter company name: ")
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

main()
# mainTransportCompany()

# username = "JoshTransportCompany"


# listOfOrders = "2"
# with conn:
#         c.execute("""UPDATE transportCompany SET orderList = :orderList
#                 WHERE username = :username""",
#                 {'username':username,'orderList':listOfOrders}
        
#         )










































































































































































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
