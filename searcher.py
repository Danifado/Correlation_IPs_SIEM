import json
import pandas as pd 
import re


"""
this script, works by giving you a j son file and a database in . CSV file and returns three dictionaries.
1. Whole dictionary with modifications 
2. A dictionary with a unique "item" key containing a list of incidents 
3. dictionary containing all the information obtained from the database, referring to what is presented in the json report
"""
'''---------------------read_dict------------------------'''

def open_json(json_f):
    with open('response.json') as json_file:
        data = json.load(json_file)
    return data

    
def Search_Source_Ip(Dict, Item=0):
    IP = Dict['items'][ Item ]['alertMeta']["SourceIp"][0]
    return IP



def Search_Destination_Ip(Dict, Item=0):
    List_Ip = Dict['items'][Item]['alertMeta']["DestinationIp"]
    return List_Ip
    
"""----------------end_compare-----------------------------"""
"""--------------proob_whit_csv----------------------------"""

        
def search_csv_v3(Keys,Archive,dicc={}):
    archive = pd.read_csv(Archive + ".csv" ,sep = ";", names = ["Fuerza","Unidad","Dependencia","Ciudad","VLAN id","Proveedor (Satelital. ISP - CGFFMM)","Segmento Lan","Mascara","Gateway","DNS","Dir IP FW","OBSERV." ] )
    # dropping null value columns to avoid errors 
    Column = list(archive)
    total_rows = archive.shape[0]
    count = 0
    lista_=[]
    for k in Column:
        dicc[k]=[]
    patron = ('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    expre = re.compile(patron)
    for ip in Keys:
        lista_=[]
        for u in range(total_rows):
            
            ip_base = archive['Segmento Lan'][u].split()[0]
            rango = archive['Segmento Lan'][u].split()[1][1:]
            octetos_base = ip_base.split(".")
            octetos_ip = ip.split(".")
            primeros_3 = bool (octetos_base[0]==octetos_ip[0] and octetos_base[1]==octetos_ip[1] and octetos_base[2]==octetos_ip[2] )
            lista_ip = [i for i in range( int(octetos_ip[3]),int (rango)+1)]
            
            if(primeros_3  and expre.search( ip_base) != None and int(octetos_ip[3]) in lista_ip ):
                count = u
                break
            else:
                count= -1                
        if(count != -1):
            for index in Column:
                lista_=[]
                lista_.append(archive[index][count])
                dicc[index] = dicc[index] + lista_
                
            lista_=[]
        elif(count == -1):
            for index in Column:
                lista_=[]
                lista_.append("NF")
                dicc[index] = dicc[index] + lista_
                lista_=[]
        lista_=[]
    return dicc
               
    
 
"""----------------end_proob-------------------------------"""
"""--------------compare_json´s----------------------------"""

def Multi_Change(Dict):
    information = {}
    listas_IP = []
    for i in range(len(Dict["items"])):#you go through the dictionary which has an "item" key
        listas_IP=[]
        IP = Search_Source_Ip(Dict, i) #we look for the "IP" key within the same dicciolnari, in this case in just one incident
        listas_IP.append(IP)
        destination = Search_Destination_Ip(Dict,i)
        listas_IP = listas_IP +  destination
        information = search_csv_v3(listas_IP,"DB")
        #we extract a dictionary from the database in . CSV containing all the required information
        Dict['items'][i].update(information)    
            #we added this information to the list created previously
        information={}
        #we added this information to the dictionary previously given
        listas_IP = []
    return Dict , listas_IP #we returned the dictionary with the extra information and a list of the information that was extracted from the database

"""-----------end_compare_json´s---------------------------"""
"""-----------function_aux---------------------------------"""
def get_Fuerza(dic):
    fuerza = dic['Fuerza']
    return fuerza

def get_Unidad(dic):
    Unidad = dic['Unidad']
    return Unidad

def get_Dependencia(dic):
    Dependencia = dic['Dependencia']
    return Dependencia

def get_Ciudad(dic):
    Ciudad = dic['Ciudad']
    return Ciudad

def get_VLAN(dic):
    VLAN = dic['VLAN id']
    return VLAN

def get_Proveedor(dic):
    Proveedor = dic['Proveedor (Satelital. ISP - CGFFMM)']
    return Proveedor

def get_Segmento(dic):
    Segmento = dic['Segmento Lan']
    return Segmento

def get_Mascara(dic):
    Mascara = dic['Mascara']
    return Mascara

def get_Gateway(dic):
    Gateway = dic['Gateway']
    return Gateway

def get_DNS(dic):
    DNS = dic['DNS']
    return DNS

def get_Dir(dic):
    Dir = dic['Dir IP FW']
    return Dir

def get_OBSERV(dic):
    OBSERV = dic['OBSERV']
    return OBSERV
    
"""--------------end_funtions_aux--------------------------"""
"""------------execute_and_change--------------------------"""
# route to find the IP  ['items'][0]['alertMeta']["SourceIp"]
data = open_json('response.json')

A , B = Multi_Change(data) #A = it´s a diccionary with new information, B contains a list with all the new information within a list




