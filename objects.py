from geopy.geocoders import Nominatim
import geopy.distance
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
    def placeOrder(self):
        geolocator = Nominatim(user_agent="my_user_agent")
        start = input("Enter start city: ")
        end = input("Enter end city :")
        loc1 = geolocator.geocode(start+","+"Uk")
        loc2 = geolocator.geocode(end+","+"Uk")
        coords1 = (loc1.latitude,loc1.longitude)
        coords2 = (loc2.latitude,loc2.longitude)
        weight = int(input("Enter weight(kg): "))
        miles = geopy.distance.distance(coords1, coords2).miles
        miles = round(miles)
        return [start,end,miles,weight]
    def calShipping(self):
        try:
            miles = int(input("Enter miles: "))
            weight = int(input("Enter weight(kg): "))
            totalPrice = miles * weight
            print("The estimate for the cargo is £",totalPrice)
        except:
            print("Incorrect values inputted")

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
        self.completed = "False"