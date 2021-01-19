import requests
import json
import sys
import datetime
#--------------------------------------------------------------------------------------#
#Open the json file and save it into a variable with type 'dict'


def open_json(json_f):
    with open(json_f+".json") as json_file:
        data = json.load(json_file)
    return data

#If any input value is empty, set it to "Empty value" as default


def set_default_values_1():  # If any input value is empty, set it to "Empty value" as default
    global ip_rsa, port_rsa, user, password
    if ip_rsa == "":
        ip_rsa = "Empty Value"
    if port_rsa == "":
        port_rsa = "443"
    if user == "":
        user = "Empty Value"
    if password == "":
        password = "Empty Value"


def set_default_values_2():  # If any input value is empty, set it to "Empty value" as default
    global pg, ps, snc, unt
    if pg == "":
        pg = "0"
    if ps == "":
        ps = "100"
    if snc == "":
        snc = previous_time
    if unt == "":
        unt = current_time


#--------------------------------------------------------------------------------------#
#api.netwitness.local
#Authentication with the RSA NetWitness
ip_rsa = input("Please insert the IP of the RSA NetWitness server: ")
port_rsa = input(
    "Please insert the communication port with the RSA NetWitness server [default: 443]: ")
user = input("Please insert the username: ")
password = input("Please insert the password: ")

headers_1 = {"Accept": "application/json;charset=UTF-8",
             "Content-Type": "application/x-www-form-urlencoded; charset=ISO-8859-1"}

url_1 = "https://"+ip_rsa+":"+port_rsa+"/rest/api/auth/userpass/"
set_default_values_1()
print("Authentication attempt through", url_1)

data_1 = {"username": user, "password": password}

resp_token = requests.post(url_1, data=data_1, headers=headers_1, verify=False)

print(resp_token.status_code)

if resp_token.status_code == 200:
    resp_token_json = resp_token.json()
    NW_token = resp_token_json["accessToken"]
    print("Authentication Successful")
else:
    print("Authentication Error")
    NW_token = "none"
    sys.exit()

#--------------------------------------------------------------------------------------#
#Obtainment of incidents from RSA NetWitness
print("Obtainment of incidents from RSA NetWitness by Date Range")
while True:
    current_time = datetime.datetime.now().isoformat() + "Z"
    previous_time = datetime.datetime.now() - datetime.timedelta(hours=6, minutes=0)
    previous_time = previous_time.isoformat() + "Z"
    url2 = "https://"+ip_rsa+":"+port_rsa+"/rest/api/incidents"
    pg = input("Please insert the requested page number [default: 0]: ")
    ps = input(
        "Please insert the maximum number of items to return in a single page [default: 100]: ")
    snc = input("Please insert SINCE when to gather incidents [default: {}]: ".format(
        previous_time))
    unt = input(
        "Please insert UNTIL when to gather incidents [default: {}]: ".format(current_time))
    set_default_values_2()

    par = {"pageNumber": pg, "pageSize": ps,
           "since": snc, "until": unt}  # HTTP Parameters
    headers_2 = {"Accept": "application/json;charset=UTF-8",
                 "NetWitness-Token": NW_token}  # HTTP Parameters
    # HTTP GET function call
    response = requests.get(url2, params=par, headers=headers_2, verify=False)
    data_2 = response.json()  # Generate dict based on the json response

    with open("response.json", "w") as outfile:  # Save the json response into a json file
        json.dump(data_2, outfile)

    #--------------------------------------------------------------------------------------#
    #Open and read the obtained json file with the results

    # Call the funcion to open the created json file
    data = open_json("response")
    
    # Executes Reporter module

    exec(open('reporter.py').read()) 

    newrequest = input(
        "Please press enter to make a new consult or another letter to exit: ")
    if newrequest != "":
        break
    #--------------------------------------------------------------------------------------#
