import re
import sys
import urllib.request

usage = "Run the script: python ip_lkup.py IPAddress you dumdum :P"

if len(sys.argv)!=2:
    print(usage)
    sys.exit(0)

if len(sys.argv) > 1:
    ipaddr = sys.argv[1]


urll='https://api.ipgeolocation.io/ipgeo?apiKey=6ef5bfce49c3412fb0849e8ecd8f7dcf&ip='+ipaddr+'&fields=latitude,longitude'

page=urllib.request.urlopen(urll).read().decode("utf-8")
#page=response.decode('utf-8')
print(type(page))
print(page)

