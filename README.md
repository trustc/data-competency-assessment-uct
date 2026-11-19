
## Challenge
### Data
The data for this challenge is the City of Cape Town's service request (C3) dataset, published on the City's Open Data Portal (ArcGIS Hub):

https://odp-cctegis.opendata.arcgis.com/datasets/cctegis::service-requests-2023-until-06-october-2026-deprecated/explore

### Data Source and API Extraction
* Requested: Work out the API endpoint behind the dataset page above. ArcGIS Hub datasets are backed by a feature service that exposes a REST query interface. Document in your README how you found it.
1. The ArcGIS explore link allows the user to view the API resources,  from here two links which allows one to find the endpoint details
 
 * **Service Layer URL**:
 `https://services6.arcgis.com/nyYfO9SxHU2ChQd9/arcgis/rest/services/Service_Requests_2023_until_20_May_2026/FeatureServer/0`

 * **REST Query Endpoint**:
 `https://services6.arcgis.com/nyYfO9SxHU2ChQd9/arcgis/rest/services/Service_Requests_2023_until_20_May_2026/FeatureServer/0/query`

 * **Organisation ID** = nyYfO9SxHU2ChQd9

 * **Service Name** = Service_Requests_2023_until_20_May_2026

### Fields:
* Requested: Inspect the dataset's schema (field names and types) and record what you find.

Browing through `https://services6.arcgis.com/nyYfO9SxHU2ChQd9/arcgis/rest/services/Service_Requests_2023_until_20_May_2026/FeatureServer/0` allows to view the 14 field definations of which a subset is listed below:
1. Sub_Council (type: esriFieldTypeString, alias: Sub Council, SQL Type: sqlTypeNVarchar, length: 4000, nullable: true, editable: true)
2. Ward (type: esriFieldTypeString, alias: Ward, SQL Type: sqlTypeNVarchar, length: 256, nullable: true, editable: true)
3. Suburb (type: esriFieldTypeString, alias: Suburb, SQL Type: sqlTypeNVarchar, length: 4000, nullable: true, editable: true)
4. C3_Complaint_Type (type: esriFieldTypeString, alias: C3 Complaint Type, SQL Type: sqlTypeNVarchar, length: 4000, nullable: true, editable: true)
....
14. ObjectId (type: esriFieldTypeOID, alias: ObjectId, SQL Type: sqlTypeInteger, length: 0, nullable: false, editable: false)

The fields list allows identification of the dataset variable name with the respective alias. e.g variable name `Sub_Council` - `Sub Council` as alias.

* The schema also details two distinct data type for ArcGIS and SQL. 

* For example Sub_Council will have a string data type in ArGIS and have a nvarchar in SQL,

* Notable all fields are editable except the ObjectId which can not be nullable as well.


## Setup and Installation

1. **Install required packages**: We would need to install dependencies that are already included in the requirements file.
* To do this we use pip assuming python is already running/installed in the computer. If not please install python and pip

Change directory to **data-competency-assessment-uct/**  then run these commands:

python -m pip install --upgrade pip
pip install -r requirements.txt

2. **Test Run**: For the test version that will pull just 1000 rows from ArcGIS Hub REST API querry (just getting the csv)

cd code/

python fetch.py

3. **Output**: this will output test_date_extract_1000.csv located in data/test/ folder of the project.


## Main Assessment

4. Fetch all data as per requirement

* make sure you are code/ directory

python fetch_no_power_requests.py 

5. Fetch all data using cached files

* make sure you are code/ directory

python fetch_no_power_requests.py --from-cache

6. All the outfiles of interest will be located: cached json file will be here data/raw
 and csv file will be here 
  processed_csv = data/no_power_service_requests.csv.

7. Within the code have also computed the number of filtered records from the api side to compare to the records being returned by processing the raw data

8. The summary file is for grouped data as per request
* Requested: Aggregate the number of reports for each suburb and write the result to a CSV file (one row per suburb, with the suburb name and the report count), 
  sorted by count in descending order.

  The extracted suburb summary is here -> data/no_power_service_requests_sub_summary.csv 

9. Requested: Examine the suburb field for data quality problems (for example missing or blank values, inconsistent capitalisation, stray whitespace, or spelling 
  variants of the same suburb) and decide how to handle them. Document the decisions you made and why.

* From the 1000 rows returned from the summary:
1. 4 of the total returned suburbs names completely missing or specified as '#','9','0' or simple not indicated.
2. These totaled to 25 926 notifications. 
3. These will be labeled as Unknown or ignored as they can not be matched without triangulating with other variables where possible.
4. In any analysis I would drop these records.

10. For the mispelt Suburb name, I would map to a single name and recompute the total keeping track of the original name for validation 
* For example
 1. fish hoek, FISHOEK, FISHHOEK will all map to the same name say 'Fish Hoek'
 2. However, Masiphumelele FisH Hoek, MASIPHUMELELE - FISH HOEK, and SUNNYDALE MASIPHUMELELE FISH HOEK will map to Masiphumelele and Sunndale as these are not Fish Hoek areas
 3. Fuzzy matching can also be used to help identify near to perfect matches. A human eye will always be needed to check and validate the matches.

* NB: In order to do this efficiently there will be need look into other fields of interest like x_y_coordinates for example to help with the decision making.

11. Another important factor to consider is what is the question being answered?
* For example which area has the most notification? What type of notification are dominant in which area?
* These do necessitate the need to clean the data and make the allocation as precise.
* To facilitate this clean up as these suburbs are finite, creating a dictionary to align the matches will be ideal, to allow reproducibility and any validation as needed.

12. Request: Validate your result. At a minimum, check that the sum of the suburb counts reconciles to the total number of records extracted 
(accounting for any records with no suburb), and compare your total against the record count the API reports for the same filter.

* A validation step has also been included with the script and a messaged logged once the check is completed processed.




