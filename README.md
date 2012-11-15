geotools
========
This is a set of tools designed to augment events in Splunk with geospatial data.

Lookups:
	"geonamesGetPostalCode" - makes a call to GeoNames web service if you submit latitude and longitude and returns "postalCode" (a.k.a - Zip Code)

	 	Testing this lookup
	 	 1.  At command line interface (in *NIX operating systems) run this:
	 	 		cd $SPLUNK_HOME/etc/apps/geotools/
	 	 		$SPLUNK_HOME/bin/splunk cmd python bin/geonamesGetPostalCode.py ./test_at_CLI.csv

	 	 		What should come back will be a CSV structure that will look like this:

	 	 			longitude,latitude,postalCode
					40.762437,-73.988013,10019
					43.7029284,-79.3784065,M4G

		2.  In Splunk, do this:
			a. Index the following file: $SPLUNK_HOME/etc/apps/geotools/sample_csv_events.csv
			b. You can use the "csv" sourcetype that Splunk should naturally apply at index time.
			c. Go to the "GeoTools" app and use the search view.
			d. Search on this over all time:
				source=*sample_csv* | head 10 | lookup geonamesGetPostalCode latitude longitude OUTPUTNEW postalCode
			e. Events should have the postalCode attached to them (we hope)

