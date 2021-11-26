"""Importing a libary of geopy so that a location can be found
   when someone puts in a city"""
from geopy.geocoders import Nominatim
import geopy.distance

"Main class"
class Person:
    #Creating the Person class with all the attributes needed
    def __init__(self,username,password,personType):
        self.username = username
        self.password = password
        self.personType = personType

"Sub class of Person"   
class CargoOwner(Person):
    #CargoOwner class is the super class of Person
    def __init_subclass__(self):
        
        return super().__init_subclass__()
    """placeOrder method for CargoOwner"""
    def placeOrder(self):
        #Using Nominatim service to get the locations for entered cities
        geolocator = Nominatim(user_agent="etransport")
        #user enters start and end location
        start = input("Enter start city: ")
        end = input("Enter end city : ")
        #loc1 and loc2 are the postion of the city 
        loc1 = geolocator.geocode(start+","+"Uk")
        loc2 = geolocator.geocode(end+","+"Uk")
        #coords1 and coords2 get the lag and long of the postion
        coords1 = (loc1.latitude,loc1.longitude)
        coords2 = (loc2.latitude,loc2.longitude)
        weight = int(input("Enter weight(kg): "))
        #Miles are calculated for the distance between the 2 sets of postions
        miles = geopy.distance.distance(coords1, coords2).miles
        #Miles is rounded up
        miles = round(miles)
        #Method returns the start and end city, distance in miles and weight of parcel
        return [start,end,miles,weight]
    """calShipping method for CargoOwner"""
    def calShipping(self):
        try:
            #User enters information to get an estimate for the price
            miles = int(input("Enter miles: "))
            weight = int(input("Enter weight(kg): "))
            totalPrice = miles * weight
            print("The estimate for the cargo is £",totalPrice)
        except:
            print("Incorrect values inputted")

"Sub class of Person"   
class Driver(Person):
    """Driver is a sub-class of person and takes the attributes of it as well"""
    def __init__(self,username,password,personType,lorryDetails,driverDetails,company):
        super().__init__(username,password,personType)
        self.lorryDetails = lorryDetails
        self.driverDetails = driverDetails
        self.company = company
        self.orderListDriver = ""
    """viewAndAcceptOrders method for driver"""
    def viewAndAcceptOrders(self,orderList):
        #Takes the list and joins them together into a string
        orderListStr = "".join(orderList)
        #String is split with commas  
        orderList = orderListStr.split(",")
        #Returns the list
        return orderList
    """completeOrder method for driver"""
    def completeOrder(self,orderListDriver):
        #Takes the list and joins them together into a string
        orderListDriver = orderListDriver[0]
        orderListDriverStr = "".join(orderListDriver)
        #String is split with commas  
        orderListDriver = orderListDriverStr.split(",")
        #Returns the list
        return orderListDriver

"Sub class of Person"      
class TransportCompany(Person):
    """Transport company is a sub-class of person and takes the attributes of it as well"""
    def __init__(self,username,password,personType):
        super().__init__(username,password,personType)
        self.orderList = ""
    """Showing the orders that the drivers have"""
    def showDriverOrders(self,driverList):
        #Listing through all the items in the list
        for x in driverList:
            #Checking the driver has any order or not
            if x[1] == "":
                print("Driver",x[0],"has no orders")
            else:
                print("Driver",x[0],"has orders",x[1])
    """Displaying the orders """
    def displayOrder(self,listOfOrders):
        #Displaying all the orders in the list
        for i in listOfOrders:
                print("Order",i[4],", Start city:",i[0],", End city:",i[1],", Distance(miles):",i[2],", Weight(kg):",i[3])
                
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