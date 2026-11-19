
## Challenge
### Data
The data for this challenge is the City of Cape Town's service request (C3) dataset, published on the City's Open Data Portal (ArcGIS Hub):

https://odp-cctegis.opendata.arcgis.com/datasets/cctegis::service-requests-2023-until-06-october-2026-deprecated/explore

### Data Source and API Extraction
* Request: Work out the API endpoint behind the dataset page above. ArcGIS Hub datasets are backed by a feature service that exposes a REST query interface. Document in your README how you found it.
1. The ArcGIS explore link allows the user to view the API resources,  from here two links which allows one to find the endpoint details
 ***Service Layer URL:**`https://services6.arcgis.com/nyYfO9SxHU2ChQd9/arcgis/rest/services/Service_Requests_2023_until_20_May_2026/FeatureServer/0`
 ***REST Query Endpoint:**`https://services6.arcgis.com/nyYfO9SxHU2ChQd9/arcgis/rest/services/Service_Requests_2023_until_20_May_2026/FeatureServer/0/query`






### Fields:
* Request: Inspect the dataset's schema (field names and types) and record what you find.
Browing through **`https://services6.arcgis.com/nyYfO9SxHU2ChQd9/arcgis/rest/services/Service_Requests_2023_until_20_May_2026/FeatureServer/0` allows to view the 14 field defination of which
a subset is listed below:
1. Sub_Council (type: esriFieldTypeString, alias: Sub Council, SQL Type: sqlTypeNVarchar, length: 4000, nullable: true, editable: true)
2. Ward (type: esriFieldTypeString, alias: Ward, SQL Type: sqlTypeNVarchar, length: 256, nullable: true, editable: true)
3. Suburb (type: esriFieldTypeString, alias: Suburb, SQL Type: sqlTypeNVarchar, length: 4000, nullable: true, editable: true)
4. C3_Complaint_Type (type: esriFieldTypeString, alias: C3 Complaint Type, SQL Type: sqlTypeNVarchar, length: 4000, nullable: true, editable: true)
....
14. ObjectId (type: esriFieldTypeOID, alias: ObjectId, SQL Type: sqlTypeInteger, length: 0, nullable: false, editable: false)

The fields list allows identification of the dataset variable name with the respective alias. e.g variable name Sub_Council - "Sub Council" as alias.

The schema also details two distinct data type for ArcGIS and SQL. 

For example Sub_Council will have a string data type in ArGIS and have a nvarchar in SQL,

Notable all fields are editable except the ObjectId which can not be nullable as well.


## Setup and Installation

1. **Install required packages: We would need to install dependencies that are already included in the requiremnts file.
To do this we use pip assuming python is already running/installed in the computer, run this command

python -m pip install --upgrade pip
pip install -r requirements.txt

2. **Run: For the test version that will pull just 1000 rows from ArcGIS Hub REST API querry (just getting the csv)
python fetch.py

3. ** Output: this will output test_date_extract_1000.csv located in /date/test/ foolder of the project.


## Main Assessment

4. **Fetch all data as per requirement

python fetch_no_power_requests.py 

5. **Fetch all data using cashed files

python fetch_no_power_requests.py --from-cache

6. ** The fin

