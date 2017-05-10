# we import the Twilio client from the dependency we just installed
from twilio.rest import Client

# the following line needs your Twilio Account SID and Auth Token
client = Client("ACa849a726136e5f820facb11184d9d0de", "43ef7096906dfa3d94126afea4c013b3")

# change the "from_" number to your Twilio number and the "to" number
# to the phone number you signed up for Twilio with, or upgrade your
# account to send SMS to any phone number
client.messages.create(to="+16692121549", 
                       from_="+13343848263", 
                       body="01153656,4678745461,489797994,4979546416,497541616,798451218451,7989513212,97415121,4974513133,978784121")
