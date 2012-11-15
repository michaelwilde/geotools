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
# making sure changes captured

log = open("output.log", 'w')

log.write("STARTED\n")
log.flush()

import csv, sys, traceback, json, fileinput

log.write("IMPORTED\n")
log.flush()

sys.path.append("requests.egg")
#to accomodate splunk versions that do not include uuid module.
sys.path.append("uuid-1.30")

import requests

class dotdict(dict):
    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__


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


    for line in reader:
       
        lat = line["latitude"]
        lng = line["longitude"]
        
        
       

       
        
        payload = {'lat':lat, 'lng':lng,'username':'splunkcto','maxRows':'1'}
        r = requests.get("http://api.geonames.org/findNearbyPostalCodesJSON", params=payload)
        responsejson = json.loads(r.content)
        dot_responsejson = dotdict(responsejson)
        #postalCode = responsejson['postalCodes'][0]['postalCode']
        for x in dot_responsejson.postalCodes:
            x_dot = dotdict(x)
       
        
            row = {
                "longitude": str(lat),
                "latitude": str(lng),
                "postalCode": str(x_dot.postalCode)
                #"country_name": doc["country"]["name"],
                #"country_code": doc["country"]["iso"],
                #"region_name": doc["region"]["name"],
                #region_code": doc["region"]["code"],
                #"city_name": doc["name"]
            }
            #print row
            writer.writerow(row)

        
try:
    main()

except Exception as e:
    exc = traceback.format_exc()
    log.write(str(exc))
    raise e
