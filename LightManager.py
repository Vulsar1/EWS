from hue import Bridge, Light
import asyncio
from huesdk import Hue
import time
import urllib3

class LightManager():
    
    def __init__(self) -> None:
        
        urllib3.disable_warnings()
        self.user=0 #1 if anne is user, 0 if raaf is user
        self.ips =["192.168.2.1","192.168.178.43"] #ips for raaf and anne respectively
        self.usernames = ["BDvoeSA0fV0VI6xiw1LHLVvUOIj3OABQHUgekwZ8", "su6nCGMRrINN5z0snp9lCl5V3Lzx-n6tPzX889bA"] #usernames for raaf and anne respectively
        self.names = [['hue play raaf', 'plafondlamp'], ['anne top']]  # light names for raaf and anne respectively


        #Connect to hue bridge
        self.hue = Hue(bridge_ip=self.ips[self.user], username=self.usernames[self.user])
            
        #Retrieve lights
        self.lights = self.hue.get_lights()
        
        
    def toggleAllLights(self, on):
        time.sleep(0.5)    
        #If we want the lights to turn on, then loop through all the lights and turn them on
        if(on):
            for i in range(len(self.lights)):
                self.lights[i].on()
        #If we do not want to turn the lights on, we loop through all the lights and turn them off
        else:
            for i in range(len(self.lights)):
                self.lights[i].off()

    def listLights(self):
        lightNames = []
        #Print light names
        for i in range(len(self.lights)):
            lightNames.append(self.lights[i].name)

    def toggleLightsByName(self, on, names):

        #Change names to lowercase
        namesLowerCase = []
        for i in range(len(names)):
            namesLowerCase.append(names[i].lower())
            
        #If we want the lights to turn on, then loop through all the lights and turn them on
        if(on):
            for i in range(len(self.lights)):
                if(self.lights[i].name.lower() in namesLowerCase):
                    self.lights[i].on()
                    
        #If we do not want to turn the lights on, we loop through all the lights and turn them off
        else:
            for i in range(len(self.lights)):
                if(self.lights[i].name.lower() in namesLowerCase):
                    self.lights[i].off()

    #Turn all light on/off every 5 seconds
    def bullyFamily(self, timeBetweenSwitch):  
        time.sleep(0.5)    
                    
        count = 0
        while True:
            self.toggleAllLights(count%2==0)
            time.sleep(timeBetweenSwitch)  
            count+=1

    #Turn all lights matching names on/off every 5 seconds
    def bullyFamily_NameVersion(self, timeBetweenSwitch, names):
        count = 0
        while True:
            self.toggleLightsByName(count%2==0, names)
            time.sleep(timeBetweenSwitch)  
            count+=1

    def lightSwitch(self, names):

        #Change names to lowercase
        namesLowerCase = []
        for i in range(len(names)):
            namesLowerCase.append(names[i].lower())
            

        for i in range(len(self.lights)):
            if(self.lights[i].is_on):
                if(self.lights[i].name.lower() in namesLowerCase):
                    self.lights[i].off()
            else:
                if(self.lights[i].name.lower() in namesLowerCase):
                    self.lights[i].on()

#this is the trigger to the light switch function
# Create an instance of LightManager and call lightSwitch
#if __name__ == "__main__":
#    manager = LightManager()
#    manager.lightSwitch(names=manager.names[manager.user])
