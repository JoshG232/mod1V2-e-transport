"Main class"
class Person:
    def __init__(self,username,password,personType):
        self.username = username
        self.password = password
        self.personType = personType

"Sub class of Person"   
class CargoOwner(Person):
    def __init_subclass__(self):
        return super().__init_subclass__()
    def placeOrder():
        print("Temp placeOrder")
    def calShipping():
        print("Temp calShipping")

"Sub class of Person"   
class Driver(Person):
    def __init__(self,username,password,personType,lorryDetails,driverDetails,company):
        super().__init__(username,password,personType)
        self.lorryDetails = lorryDetails
        self.driverDetails = driverDetails
        self.company = company
        self.orderListDriver = ""
    def viewOrders():
        print("Temp viewOrders")
    def acceptOrders():
        print("Temp acceptOrders")

"Sub class of Person"      
class TransportCompany(Person):
    def __init__(self,username,password,personType):
        super().__init__(username,password,personType)
        self.orderList = ""
    def showCustomerOrders():
        print("Temp showCustomerOrders")
    def sendOrder():
        print("Temp sendOrder")

"Class for Order, this class is so orders can be created easier"
class Order():
    def __init__(self,start,end,miles,weight,orderID):
        self.start = start
        self.end = end
        self.miles = miles
        self.weight = weight
        self.orderID = orderID
        self.accepted = "False"
        self.driverAccepted = "False"