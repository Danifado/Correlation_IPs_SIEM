# Correlation between IPs and SIEM alarms


Propose toautomate the manual process done by the SIEM administrator, through a pragmatic software solution that communicates with:
1. A SIEM, e.g. a RSA Netwitness
1. A simple database, e.g. an Excel spreadsheet, and generate a report with the relations found.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following libraries:
- requests
- json
- sys
- datetime
- pandas
- re
- docx
- socket
- selenium

```bash
pip install requests json sys datetime pandas re docx socket selenium
```

## Usage
Make sure that the database name is saved as "DB.xls"` and it should has the same columns as the excel "sample.xls" with the columns: Sucursal, Area,	Dependencia, 	Ciudad,	VLAN id,	Proveedor Internet, Segmento Lan,	Mascara	Gateway, DNS	Dir, IP FW, where:

-Sucursal: Branch of the organization
-Area: internal area in the "sucursal"
-Dependencia: internal subarea in the "area"
-Ciudad: City
-VLAN id:	Identification of the vlan
-Proveedor Internet: ISP - Interet Service Provider
-Segmento Lan: 10.10.20.1 -81
-Mascara: 255.255.242.1
-Gateway: 10.10.20.2
-DNS	Dir: 10.10.20.25	
-IP FW: 10.10.20.1

Run $python requester.py, then fill every field with the requested information.
```bash
Please insert the IP of the RSA NetWitness server: XX.XX.XX.XX
Please insert the communication port with the RSA NetWitness server [default: 443]: 443
Please insert the username: Admin  
Please insert the password: 12345
Authentication attempt through https://XX.XX.XX.XX:443/rest/api/auth/userpass/
200
Authentication Successful
Obtainment of incidents from RSA NetWitness by Date Range
Please insert the requested page number [default: 0]:
Please insert the maximum number of items to return in a single page [default: 100]: 
Please insert SINCE when to gather incidents [default: 2021-01-18T14:31:34.346954]: 2021-01-18T14:31:34.346954
Please insert UNTIL when to gather incidents [default: 2021-01-18T20:31:34.346954]: 2021-01-18T20:31:34.346954
```

You can do more than one consulte at once:
```bash
Please press enter to make a new consult or another letter to exit: 
```

Then you will have a .docx file with the expected report

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
