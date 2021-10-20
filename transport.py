import json
import ast
class Person:
    def __init__(self,username,password,personType):
        self.username = username
        self.password = password
        self.personType = personType
    
    

class CargoOwner(Person):
    def __init_subclass__(self):
        return super().__init_subclass__()
    def placeOrder():
        print("Temp placeOrder")
    def calShipping():
        print("Temp calShipping")

class Driver(Person):
    def __init__(self,username,password,personType,lorryDetails,driverDetails,company):
        super().__init__(username,password,personType)
        self.lorryDetails = lorryDetails
        self.driverDetails = driverDetails
        self.company = company
    def viewOrders():
        print("Temp viewOrders")
    def acceptOrders():
        print("Temp acceptOrders")
    
class TransportCompany(Person):
    def __init__(self,username,password,personType):
        super().__init__(username,password,personType)
        self.orderList = []
    def showCustomerOrders():
        print("Temp showCustomerOrders")
    def sendOrder():
        print("Temp sendOrder")

class Order():
    def __init__(self,start,end,miles,weight,orderID):
        self.start = start
        self.end = end
        self.miles = miles
        self.weight = weight
        self.orderID = orderID

"""This function takes the user input and selects if they want to login
   or register, while also taking the value of "typeChoice" to see if 
   they are a Cargo Owner,Driver or Transport company"""

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
    global loggedIn
    # file = "transport.json"
    # data = json.loads(open(file).read())
    # username = input("Enter username ")
    # userList = data["Cargo Owners"][0]
    loggedIn = input("Do you want to login")
    if loggedIn == "Yes":
        loggedIn = True
        if typeChoice == 1:
            mainCargoOwner()
        if typeChoice == 2:
            print(2)
            #mainTransportCompany()
        if typeChoice == 3:
            mainTransportCompany()

    else:
        loggedIn = False
        
def registerCargoOwner():
    username = input("Enter username")
    password = input("Enter password")
    tempObj = CargoOwner(username,password,"Cargo Owner")
    tempObj = vars(tempObj)
    y = json.dumps(tempObj)
    writingToJson(y,"Cargo Owners")
    
def registerDriver():
    username = input("Enter username")
    password = input("Enter password")
    lorryDetails = input("Enter Lorry details")
    driverDetails = input("Enter driver details")
    company = input("Enter what company you work for:")
    tempObj = Driver(username,password,"Driver",driverDetails,lorryDetails,company)
    tempObj = vars(tempObj)
    y = json.dumps(tempObj)
    writingToJson(y,"Drivers")

def registerTransportCompany():
    username = input("Enter username")
    password = input("Enter password")
    tempObj = TransportCompany(username,password,"Transport Company")
    tempObj = vars(tempObj)
    y = json.dumps(tempObj)
    writingToJson(y,"Transport Company")

def writingToJson(y,typeOf):
    with open("transport.json","r+") as f:
        fData = json.load(f)
        fData[typeOf].append(y)
        f.seek(0)
        json.dump(fData,f, indent=4)
        for i in fData[typeOf]:
            print(i)
        
def mainCargoOwner():
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
        tempObj = vars(tempObj)
        y = json.dumps(tempObj)
        writingToJson(y,"Orders")

def mainTransportCompany():
    print("""
        1:View orders for drivers
        2:View available orders)
        """)
    username = "EON"
    choice = int(input("Enter selection: "))
    if choice == 1:
        with open("transport.json","r") as f:
            fData = json.load(f)
            
    if choice == 2:
        print("Displaying orders")
        with open("transport.json","r+") as f:
            fData = json.load(f)
            count = 1
            for x in fData["Orders"]:
                print("Order number",count,": ",x)
                count += 1
            orderChoice = int(input("Select order: "))
            x = fData["Orders"][orderChoice-1]
            y = json.loads(x)
            orderID = y["orderID"]
            print(orderID)
            dicCompany = fData["Transport Company"][orderID]
            json_acceptable_string = dicCompany.replace("'", "\"")
            z = json.loads(json_acceptable_string)
            print(z)
            orderList = z["orderList"]
            orderList.append(orderChoice)
            abc = {"orderList":orderList}
            z.update(abc)
            print(z)
            fData["Transport Company"].append(z)
            print(fData)
            json.dump(fData,f, indent=4)
            # print(orderList)
            # abc = {"orderList":orderList}
            # print(fData["Transport Company"][1][3])
            
# def updateOrderList()
#     with open("transport.json","w") as f:

"""Main function"""

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
mainTransportCompany()