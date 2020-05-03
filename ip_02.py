import sys
import urllib.request

usage = "Run the script: ./geolocate.py IPAddress"

if len(sys.argv)!=2:
    print(usage)
    sys.exit(0)

if len(sys.argv) > 1:
    ipaddr = sys.argv[1]

# specify our connection website
geody = "http://www.geody.com/geolook.php?q="+ ipaddr
html_page = urllib.request.urlopen(geody).read() # this is just a big string

# find where the webpage head specifies the lat and long data
str_to_find = 'meta name="ICBM" content=""'

# find the start and finish indexes
data_index_start = html_page.index(str_to_find) + len(str_to_find)
data_index_stop = html_page.index('" />', data_index_start)

# extract the data from the string of html
data = html_page[data_index_start:data_index_stop]
latlong = data.split(',')

# Print the results to the screen
print ("IP address is locataed at Latitude %s and Longitude %s" %(latlong[0], latlong[1]))