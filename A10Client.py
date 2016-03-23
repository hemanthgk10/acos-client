import base64
import csv
import difflib
import getpass
import glob
import os
import requests
import sys
import time
import urllib

# Variables
A10_SERVER  = " YOUR A10 SERVER DETAILS GOES HERE "
USERNAME    = " YOUR USERNAME "
PASSWORD    = " YOUR PASSWORD "
AFLEX_DIR   = "data/aflex_files"
BACKUP_DIR  = "data/backup/"
mode        = os.environ["DRY_RUN"]



class A10Client:

    def __init__(self):
        """
        Initializes the connection with A10 server and gets the
        session id
        """
        self.A10_API_BASE_URL = "http://"+A10_SERVER+"/services/rest/v2.1/"
        session_id_url = self.A10_API_BASE_URL+"?method=authenticate&username="+USERNAME+\
                "&password="+base64.b64decode(PASSWORD)+"&format=json"
        session_id_raw_json = requests.get(session_id_url)
        session_id_info = json.loads(session_id_raw_json.content)
        self.session_id = session_id_info["session_id"]

    def get_aflex_by_name(self, name):
        """
        Method to get the Aflex by name
        """
    	get_url = self.A10_API_BASE_URL+"?method=slb.aflex.search&session_id="+self.session_id+\
		      "&format=json"
	response = None
	try :
            payload = { 'name': name }
            print "Here is the payload : %s, url : %s" % (payload,get_url)
            headers = {'Content-type': 'application/json'}
            response = requests.post(get_url,data=json.dumps(payload),headers=headers )
            print "Got response from Get Query : %s " % response.content
            content = response.text
            if content.find("ref_count") < 0:
               response = None
	except:
	    print "Failed to get the flex by name %s " % name
	    response = None
        return response
    
    def download_aflex_by_name(self, name):
        """
        Download the aflex by specified name
        """
        download_url = self.A10_API_BASE_URL+"?session_id="+self.session_id+\
                      "&format=json&method=slb.aflex.download&name=%s" %name
        filename = BACKUP_DIR+name+time.strftime("%Y%m%d-%H%M%S")
        try:
           headers = {'Content-type': 'application/json'}
           response = requests.post(download_url, data = json.dumps({'name': name}), headers=headers )
           print "Saving response to file %s with content: %s " % (filename, response.content)
           with  open(filename, 'w') as f:
              f.write(response.content)
           f.close()
        except:
           print "Failed to get the flex by name %s " % name
        return filename

    def get_all_files(self):
        """
        Get All Aflex files from the server
        """
        download_url = self.A10_API_BASE_URL+"?session_id="+self.session_id+\
                      "&format=json&method=slb.aflex.getAll"
        headers = {'Content-type': 'application/json'}
        response = requests.post(download_url, headers=headers)
        aflex_list = json.loads(response.content).get("aflex_list")
        for aflex in aflex_list:
            aflex_name = aflex.get("name")
            aflex_dir = "../
            with open(
                    
    def post_aflex(self):
        """
    	Method to post data to a Aflex in A10 Servers
    	It first checks if a flex exists with by that name, if so it updates
    	else it upload the flex
        """
        for aflex in glob.glob(AFLEX_DIR+'/*'):
	       aflex_name = aflex.split('/')[-1]
               print "Running in Dry Run mode %s " % mode 
               if mode=="True":
                  backup_file = self.download_aflex_by_name(aflex_name)
                  backup_file_name = backup_file.split('/')[-1]
                  with open(backup_file, 'r') as oldfile:
                       with open(aflex, 'r') as newfile:
                          diff = difflib.unified_diff(
                            oldfile.readlines(),
                            newfile.readlines(),
                            fromfile=backup_file_name,
                            tofile=aflex_name,
                          )
                          for line in diff:
                            sys.stdout.write(line)
               elif mode=="False":
                  print " ### Checking for the aflex name %s" % aflex_name
                  response = self.get_aflex_by_name(aflex_name)
	          if response is None:
	             url = self.A10_API_BASE_URL+"?session_id="+self.session_id+\
		              "&format=json&method=slb.aflex.upload"
                     print "Uploading Aflex %s" % aflex_name
		     upload_response = requests.post(url, files={aflex: open(aflex, 'rb')})
                     print "Response for your upload request is %s " % upload_response
	          else:
		     url = self.A10_API_BASE_URL+"?session_id="+self.session_id+\
		              "&format=json&method=slb.aflex.update"
                     print "Udating aflex: %s" % aflex_name
                     payload = { 'name':aflex_name, 'filename':aflex_name }
                     update_response = requests.post(url, files={aflex: open(aflex, 'rb')})
                     print "Response for your update request is %s " % update_response

if __name__ == "__main__":
    a10_client = A10Client()
    #a10_client.post_aflex()
    a10_client.get_all_files()
