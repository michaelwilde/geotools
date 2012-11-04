#! /usr/bin/python
#
# Copyright 2011 Splunk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

log = open("output.log", 'w')
import csv, sys, traceback, requests, json, fileinput


#> geonames1.py < ~/Desktop/myfile.out
#
#And it should work more or less the same.


#fout = open('/Users/mwilde/dev/csvtest.csv','rw')
sys.path.append("requests.egg")

try:
    from requests import requests
except:
    pass


def main():
    #reader = csv.DictReader(f)

    reader = csv.DictReader(sys.stdin)

    # Write header
    csv.writer(sys.stdout).writerow(reader.fieldnames)

    # Create dict writer
    writer = csv.DictWriter(sys.stdout, reader.fieldnames)

    #setup arguments to the get request.

    #make the request to geonames

    #convert the json in to a python data structure (dict)
    #responsejson = json.loads(r.content)


    #traverse the datastructure dict/list/dict down to the postal code
    ## i probably don't need this line, i assume as its redundant

    for line in reader:
       
        lat = line["latitude"]
        lng = line["longitude"]
        
        payload = {'lat':lat, 'lng':lng,'username':'splunkcto','maxRows':'1'}
        r = requests.get("http://api.geonames.org/findNearbyPostalCodesJSON", params=payload)
        responsejson = json.loads(r.content)
        postalCode = responsejson['postalCodes'][0]['postalCode']
        
        row = {
            "longitude": str(lat),
            "latitude": str(lng),
            "postalCode": str(postalCode)
            #"country_name": doc["country"]["name"],
            #"country_code": doc["country"]["iso"],
            #"region_name": doc["region"]["name"],
            #region_code": doc["region"]["code"],
            #"city_name": doc["name"]
        }
        #print reader.join(row)
        writer.writerow(row)
        
try:
    main()

except Exception as e:
    exc = traceback.format_exc()
    log.write(str(exc))
    raise e
