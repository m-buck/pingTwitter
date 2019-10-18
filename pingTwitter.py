import time
import datetime
import requests
import json
import io
import string
import re
from bs4 import BeautifulSoup
import urllib2
from pushover import Client

#pushover api
client = Client("<pushover client>", api_token="<api token>")
#add hosts to be checked
accts = ['account 1', 'account 2']

def main():
    msg=""
    timestamp = time.strftime("%Y-%m-%d %H:%M")
    print timestamp    
    error = 0
    while error == 0:
        try:
            with open('/home/pi/pingTwitter.json') as data_file:
                data = json.load(data_file)
                print "Reading JSON..."
                print data
        except Exception as e:
            print e
            print "Error reading pingTwitter.json"
        for acct in accts:
            try:    
                url="https://twitter.com/" + acct
                opener = urllib2.build_opener()
                ourUrl = opener.open(url).read()
                soup = BeautifulSoup(ourUrl,"html5lib")                
                opener.close()
                print "Acct: " + str(acct)

                if soup.find('span',{'class': 'ProfileNav-value'})['data-count']:
                    print "Found tweets..."
                    print str(soup.find('span',{'class': 'ProfileNav-value'})['data-count'])
                    if int(soup.find('span',{'class': 'ProfileNav-value'})['data-count']) == int(data[acct]):
                        print "Check account " + str(acct)
                        print "Tweets have not increased...something is wrong"
                        msg = msg + "\n" + str(acct) + " is down: no new tweets"                        
                    elif int(soup.find('span',{'class': 'ProfileNav-value'})['data-count']) > int(data[acct]):
                        print "Tweets have increased since last check"
                        print "status OK..."
                    else:
                        print "Tweets have decreased since last check"
                        print "status OK..."                    
                    data[acct] = str(soup.find('span',{'class': 'ProfileNav-value'})['data-count'])                    
                else:
                    print "Could not find number of tweets...something is wrong."
                    msg = msg + "\n" + str(acct) + " is down: can't update count"
                
                time.sleep(20)

                error = 1
            except Exception as e:
                print e
                print "Error, try again in 5 sec"
                time.sleep(5)
                pass
            json_data = json.dumps(data)
    print "Writing json data..."
    print json_data
    with open('/home/pi/pingTwitter.json', 'r+') as f:
        f.seek(0)
        f.write(json.dumps(data))
        f.truncate()
    print "Json data written successfully"
    if msg:
        client.send_message(msg, title="pingTwitter")
    print "All done..."
main()