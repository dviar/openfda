import http.server
import socketserver
import http.client
import json




class OpenFDAClient():
# HTTPRequestHandler class
 #enlaza al soker con el handler, el otro define el server 
	
	OPENFDA_API_URL = "api.fda.gov"
	OPENFDA_API_EVENT = "/drug/event.json"
	
	def get_search(self,search,name):
		conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
		if search=='company':
			company=name
			conn.request("GET", self.OPENFDA_API_EVENT + '?search=companynumb:'+company+'&limit=10')
		else:
			drug=name
			conn.request("GET", self.OPENFDA_API_EVENT + '?search=patient.drug.medicinalproduct:'+drug+'&limit=10')
		r1 = conn.getresponse()
		print (r1.status, r1.reason)
		data1 = r1.read()
		data=data1.decode("utf8")
		events=json.loads(data)
		return events
	
	def get_events(self,limit):
		conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
		conn.request("GET", self.OPENFDA_API_EVENT + "?limit="+limit+"")
		r1 = conn.getresponse()
		print (r1.status, r1.reason)
		data1 = r1.read()
		data=data1.decode("utf8")
		events=json.loads(data)
		return events
class OpenFDAParser():

		
	def get_listCompanies(self, events):
		company=[]
		for event in events ['results']:
			company+=[event['companynumb']]
		return company
	def get_listDrugs(self,events):
		medicamento=[]
		for event in events ['results']:
			medicamento+=[event['patient']['drug'][0]["medicinalproduct"]]
		return medicamento
	def get_listGender(self,events):
		gender=[]
		for event in events ['results']:
			gender+=[event['patient']['patientsex']]
		return gender

class OpenFDAHTML():	
	def gender_page(self,items):
 
		male=items.count('1')
		female=items.count('2')
		#counter male drugs
		counter=	"""<h3>Number of drugs distributed for men :"""
		counter+=		str(male)
		counter+= """</h3>"""
		#counter female drugs
		counter+= """<h3>Number of drugs distributed for womans :"""
		counter+=str(female)
		counter+="""</h3>"""
		
		s=''
		for item in items:
			s +="<li>"+item+"</li>"
		html="""
		<html>
			<head><title>OPEN FDA COOL</title></head>
				<body>
					<h1><u> Gender </u></h1>"""
		html +=		counter
		html +=			"""<ol>
						%s
					</ol>
				</body>
			</html>""" %(s)
		return html 
		
				
	def get_list(self,name,items):
		
		s=''
		for item in items:
			s +="<li>"+item+"</li>"
		html="""
		<html>
			<head><title>OPEN FDA COOL</title></head>
				<body>
					<h1><u><font color="#58D3F7"> """
		html +=			name
		html +=			"""</font></u></h1>
					<ol type="circle">
						%s
					</ol>
				</body>
			</html>""" %(s)
		return html 
			
		

	def get_main_page(self):
		html= """
        <html>
			<head>
				<title>Open FDA</title>
			
			</head>
			<center><h1><font color=#FFFF00>OpenFDA Client</font></h1></center>
				<hr width="100%" font color=#FFFF00 align="left">
			<body bgcolor=#2E2E2E text=#BDBDBD >
			
				<form method= "get" action="listDrugs">
					
					<input type = "submit" value="Drug List: Send to OpenFDA">
					</input>
				
					Limit:<input type='text' size='5' name='limit'></input>
				</form>
				
				<form method="get" action="searchDrug">
					<input type="submit" value="Drug Search ">
					<input type='text' name='drug'></input>
					
				</form>
				
				<form method= "get" action="listCompanies">
					
					<input type = "submit" value="Company list: Send to OpenFDA">
					</input>
					Limit:<input type='text' size='5' name='limit'></input>
				</form>
				
				<form method="get" action="searchCompany">
					<input type="submit" value="Company Search ">
					<input type='text' name='company'></input>
					
				</form>
				
				<form method="get" action="listGender">
					<input type="submit" value="Gender Search ">
					Limit:<input type='text' size='5' name='gender'></input>
					
				</form>
			</body>
        </html>
        """
		return html
	def errorhtml(self):
		html="""
			<html>
			<head><title>ERROR</title></head>
				<body>
					<h1><b>ERROR 404 NOT FOUND</b> </h1>
				</body>
			</html>"""
		return html

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):		
	def do_GET(self):
		client=OpenFDAClient()
		paser=OpenFDAParser()
		Html=OpenFDAHTML()
		if self.path == "/":
			html=Html.get_main_page()
			self.send_response(200)
		
		elif "/listDrugs" in self.path:
			limit=self.path.split('=')[1]
			events = client.get_events(limit)
			drugs=paser.get_listDrugs(events)
			html= Html.get_list('Drugs',drugs)
			self.send_response(200)
		
		elif '/searchDrug' in self.path:
			drug=self.path.split('=')[1]
			events=client.get_search('drug',drug)
			companies=paser.get_listCompanies(events)
			html=Html.get_list(drug,companies)
			self.send_response(200)
		
		elif '/listCompanies' in self.path:
			limit=self.path.split('=')[1]
			event = client.get_events(limit)
			companies=paser.get_listCompanies(event)
			html=Html.get_list('Companies',companies)
			self.send_response(200)
		
		elif '/searchCompany' in self.path:
			company=self.path.split('=')[1]
			events=client.get_search('company',company)
			drugs=paser.get_listDrugs(events)
			html=Html.get_list(company,drugs)
			self.send_response(200)
		
		elif '/listGender' in self.path:
			gender=self.path.split('=')[1]
			events = client.get_events(gender)
			gender= paser.get_listGender(events)
			html= Html.gender_page(gender)
			self.send_response(200)
		
		else:
			html=Html.errorhtml()
			self.send_response(404)
		
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write(bytes(html,"utf8"))
		
		return
	
#Copyright [2017] [David Viar Hernandez]
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

#	http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.		

		
		
### GET EVENT		

