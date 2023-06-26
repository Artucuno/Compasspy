from compasspy.client import Compass

# Your school subdomain is the start of the url that you use to visit compass (EG: xxxx (from xxxx.compass.education))
client = Compass('<School Subdomain>', '<Authentication Cookie>')
client.login()

staff = client.getStaff()
print("=== List of Staff ===")
for f in staff:
    print(f"{f.name} - {f.id}")