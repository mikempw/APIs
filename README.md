# Discovering APIs via syslog, through an iRule. Parsing the data to generate OpenAPI 3.0 and data visualization

### Instructions
     ###instructions###
     Place the Telemetry iRule on the BIG-IP
     Create a pool on the BIG-IP that references separate syslog servers we will be sending traffic to
     Ensure this location is a server that will just receive this traffic - please don't intermingle regular syslog traffic with this collector
     Add the iRule to all Virtual Servers you want to capture web traffic 
     ###instructions###
## As per the iRule instructions
    ###User-Edit Variables start###
    set z1_http_content_type logging-pool ; #Name of LTM pool to use for receiving this data
    set z1_remoteLogProtocol UDP ; #UDP or TCP
    set z1_globalStringLimit 100 ; #How many characters to collect from user-supplied HTTP values like HTTP host, version, referrer. 
    set z1_uriStringLimit 600 ; #How many characters to collect from HTTP value of URI
    ###User-Edit Variables end###



### To generate a .CSV file
####  Run the syslog-to-csv.py on a syslog.log file - this will generate a f5_api_data.csv
 ##### Example:
    ###command###
     syslog-to-csv.py syslog.log
    ###command###

##### Example syslog.log to f5_api_data.csv output:
![image](https://github.com/user-attachments/assets/c86adc8f-0691-4472-9740-34dc4e9192d0)

### To generate an overview of APIs, Status Code etc..
  #### Run the api-summary-generator.py on the f5_api_data.csv file created above
 ##### Example:
    ###command###
     api-summary-generator.py f5_api_data.csv
    ###command###
    
##### Example API Summary
![image](https://github.com/user-attachments/assets/728ebc0f-a832-44be-a74b-be382b485871)


 ### To generate an OpenAPI schema
 #### Run the syslog-to-openapi.py on a syslog.log file
 #####   Example: 
     ###command###
     syslog-to-openapi.py syslog.log
     ###command###

##### Example OpenAPI schema output:
 
![image](https://github.com/user-attachments/assets/a8bdf63c-65c5-483b-a413-09509a5de00a)
