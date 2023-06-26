from compasspy.client import Compass

# Your school subdomain is the start of the url that you use to visit compass (EG: xxxx (from xxxx.compass.education))
client = Compass('<School Subdomain>', '<Authentication Cookie>', login=True)  # Skip having to use client.login()
