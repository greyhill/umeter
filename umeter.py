from flask import Flask, make_response, Response
import json
import requests

key = open('apikey.txt', 'r').read().strip()
url = 'https://api.forecast.io/forecast/%s/%0.3f,%0.3f'

orders = [ 'fucking', 'fuckity', 'jesus-fucking' ]

app = Flask(__name__)

def convert(temp):
    print 'in convert', temp
    us = abs(temp - 65) // 10
    us = int(us)
    if us == 0:
        return "eh."
    else:
        tr = []
        if us > 2:
            tr.append(orders[0])
            us -= 2
        if us > 2:
            tr.append(orders[1])
            us -= 2
        if us > 2:
            tr.append(orders[2])
            us -= 2
        remainder = "".join(['f'] + ['u']*us + ['ck'])
        print tr + [remainder]
        return " ".join(tr + [remainder])

@app.route('/at/<lat>,<long>')
def get_weather(lat, long):
    lat = float(lat)
    long = float(long)
    geturl = url % (key, lat, long)
    r = requests.get(geturl)
    payload = json.loads(r.text)

    temp = float(payload['currently']['apparentTemperature'])
    tr = convert(temp)

    return "The current temperature <i>feels like</i>: %s" % tr

@app.route('/')
def root():
    return \
'''
<html>

<div id="display">Getting location...</div>

<script>
    navigator.geolocation.getCurrentPosition(getLoc);

    function getLoc(position) {
        var x = document.getElementById("display");
        var lat = position.coords.latitude;
        var long = position.coords.longitude;

        xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            x.innerHTML = xmlhttp.responseText;
        };
        xmlhttp.open("GET", "at/" + lat + "," + long, true);
        xmlhttp.send();
    }
</script>

</html>
'''

if __name__ == '__main__':
    app.run(port=2788, host='0.0.0.0')

