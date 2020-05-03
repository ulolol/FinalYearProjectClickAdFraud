import urllib.request
import requests

def ipaddr(ip):

    #urll='https://api.ipgeolocation.io/ipgeo?apiKey=6ef5bfce49c3412fb0849e8ecd8f7dcf&ip='+ip+'&fields=latitude,longitude,country_name,city,zipcode'
    #page=urllib.request.urlopen(urll).read().decode("utf-8")
    #return page


    r = requests.get("http://api.ipstack.com/" + ip + "?access_key=" + "cf3b74bea5cb6106fafa3a83d57f3266")
    json_response = r.json()
    page = ("{ip}, {city}, {region_name}, {country_name}, {location[country_flag_emoji]}, {latitude}, {longitude}".format(**json_response))
    return page

