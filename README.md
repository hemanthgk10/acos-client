# acos-client
Acos client to get a particular aflex file from A10 Server, to upload bunch of aflex files from the data directory and also to download the aflex files from the server. It has dry run mode to compare the files or in dry run false mode it will update the file in the server.

How To Execute: python A10Client.py


Dry Run Mode: True

--- sample_services_aflex20160323-124715 
+++ sample_services_aflex 
@@ -107,7 +107,4 @@
    if { [HTTP::path] starts_with "/api/sample-service/" } {
         pool sample_grp
    }
-   if { [HTTP::path] starts_with "/api/sample-service2/" } {
-        pool sample_grp
-   }
 }

Dry Run Mode : False

Running in Dry Run mode False 
 ### Checking for the aflex name sample_services_aflex
Here is the payload : {'name': 'sample_services_aflex'} 
Got response from Get Query : {"aflex":{"name":"sample_services_aflex","syntax_check":1,"ref_count":2}} 
Udating aflex: sample_services_aflex
Your update to aflex got response <Response [200]>

