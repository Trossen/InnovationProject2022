import requests
import googlemaps
import math
google_api_key = 'AIzaSyDdOaN1K1GMwjxLv_x3EScqzWnJvyS-XTc'
openweathermap_api_key = 'b59487c37a2da0337444936e64b3cac9'
# home address input
home = input("Enter a home address\n") 
#home = 'Stationsvænget 2, 5260 Odense'

# work address input
work = input("Enter a work address\n") 
#work = 'Campusvej 55, 5230 Odense'

#Transport
transportnr = input("Enter a transport number.\n1: Car\n2: Public Transport\n3: Walking\n4: Bike\n")
transport = ''
if transportnr == 1:
    transport = 'driving'
elif transportnr == 2:
    transport = 'transit'
elif transportnr == 3:
    transport = 'walking'
elif transportnr == 4:
    transport = 'bicycling'

# base url
url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&"
#Test url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins=Stationsvænget 2, 5260 Odense&destinations=Campusvej 55, 5230 Odense&mode=bicycling&key=AIzaSyDdOaN1K1GMwjxLv_x3EScqzWnJvyS-XTc"
#"" + home + "&destinations=" + work + "&mode=" + transport + "&key=" + api_key
# get response
r = requests.get(url + "origins=" + home + "&destinations=" + work + "&mode=" + transport + "&key=" + google_api_key) 
 
# return time as text and as seconds
time = r.json()["rows"][0]["elements"][0]["duration"]["text"]       
seconds = r.json()["rows"][0]["elements"][0]["duration"]["value"]

print("\nThe total travel time from home to work is", time)


#Cardinal Directions
geoHome = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + home + "&key=" + google_api_key)
latHome = geoHome.json()["results"][0]["geometry"]["location"]["lat"]
lngHome = geoHome.json()["results"][0]["geometry"]["location"]["lng"]

geoWork = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + work + "&key=" + google_api_key)
latWork = geoWork.json()["results"][0]["geometry"]["location"]["lat"]
lngWork = geoWork.json()["results"][0]["geometry"]["location"]["lng"]

# calculate the angle in radians
angle = math.atan2(lngWork - lngHome, latWork - latHome)

# convert the angle from radians to degrees
angle_in_degrees = math.degrees(angle)

# determine which heading is closest
if (angle_in_degrees < -45 and angle_in_degrees >= 0) or (angle_in_degrees < 0 and angle_in_degrees >= 45):
  print("North at " + str(angle_in_degrees))

elif angle_in_degrees > 45 and angle_in_degrees <= 135:
  print("East at " + str(angle_in_degrees))

elif (angle_in_degrees < -135 and angle_in_degrees >= -180) or (angle_in_degrees <= 180 and angle_in_degrees > 135):
  print("South at " + str(angle_in_degrees))

elif angle_in_degrees >= -135 and angle_in_degrees <= -45:
  print("West at " + str(angle_in_degrees))
else:
  print("FIND ERROR at " + str(angle_in_degrees))

#Find Vindretning
print("Weather")
#openweathermap.org
#requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + home + "&key=" + google_api_key)
weatherCall = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=" + str(latWork) + "&lon=" + str(lngWork) + "&appid=" + openweathermap_api_key)
data = weatherCall.json()
#Udreng om det er med, mod eller sidevind

# extract wind.speed and wind.deg from the dictionary
weatherSpeed = data['wind']['speed']
weatherDeg = data['wind']['deg']
if weatherDeg > 180:
  weatherDeg = weatherDeg-360

# print the extracted values
print('wind.speed:', weatherSpeed)
print('wind.deg:', weatherDeg)

#Udregn hvor meget extra tid det tager (Rune)
#The closer the wind.deg and the traveling is to eachother, the more tailwind (medvind)

# Convert the angles to radians
angle1_rad = weatherDeg * (math.pi / 180)
angle2_rad = angle_in_degrees * (math.pi / 180)

# Calculate the difference in radians
diff_rad = abs(angle1_rad - angle2_rad)

# If the difference is greater than pi, we need to take the "short way" around the circle,
# which is the same as subtracting the difference from 2 * pi
if diff_rad > math.pi:
  diff_rad = 2 * math.pi - diff_rad
  
# Convert the difference back to degrees and return it
distance = diff_rad * (180 / math.pi)

# Test the function
print(distance)

if distance < 45:
  print("Tailwind")
elif distance >= 45 and distance < 135:
  print("Sidewind")
else:
  print("Headwind")

#Få Solopgang og solnedgang
