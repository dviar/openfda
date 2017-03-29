import http.server
import socketserver
import http.client
import json





# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler): #enlaza al soker con el handler, el otro define el server 
	
	OPENFDA_API_URL = "api.fda.gov"
	OPENFDA_API_EVENT = "/drug/event.json"
	
	def get_search_company(self,company):
		conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
		conn.request("GET", self.OPENFDA_API_EVENT + '?search=companynumb:'+company+'&limit=10')
		r1 = conn.getresponse()
		print (r1.status, r1.reason)
		data1 = r1.read()
		data=data1.decode("utf8")
		events=json.loads(data)
		return events
	
	def get_search(self,drug):
		conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
		conn.request("GET", self.OPENFDA_API_EVENT + '?search=patient.drug.medicinalproduct:'+drug+'&limit=10')
		r1 = conn.getresponse()
		print (r1.status, r1.reason)
		data1 = r1.read()
		data=data1.decode("utf8")
		events=json.loads(data)
		return events
	def company(self,events):
		company=[]
		for event in events ['results']:
			company+=[event['patient']['drug'][0]["medicinalproduct"]]
		
		return company
	def companynumb(self, events):
		company=[]
		for event in events ['results']:
			company+=[event['companynumb']]
		return company
	def get_event(self,limit):
		conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
		conn.request("GET", self.OPENFDA_API_EVENT + "?limit="+limit+"")
		r1 = conn.getresponse()
		print (r1.status, r1.reason)
		data1 = r1.read()
		data=data1.decode("utf8")
		events=json.loads(data)
		return events
	def drug_list(self,events):
		medicamento=[]
		for event in events ['results']:
			medicamento+=[event['patient']['drug'][0]["medicinalproduct"]]
		return medicamento
	def gender_list(self,events):
		gender=[]
		for event in events ['results']:
			gender+=[event['patient']['patientsex']]
		return gender
	
	def gender_page(self,gender):
		s=''
		for type_gender in gender:
			s +="<li>"+type_gender+"</li>"
		html="""
		<html>
			<head><title>OPEN FDA COOL</title></head>
				<body>
					<h1>Gender </h1>
					<ol>
						%s
					</ol>
				</body>
			</html>""" %(s)
		return html 
				
	def drug_page(self,medicamento):
		s=''
		for med in medicamento:
			s +="<li>"+med+"</li>"
		html="""
		<html>
			<head><title>OPEN FDA COOL</title></head>
				<body>
					<h1>OpenFDA </h1>
					<ul type="square">
						%s
					</ul>
				</body>
			</html>""" %(s)
		return html 
			
		

	def get_main_page(self):
		html= """
        <html>
			<head>
				<title>Open FDA</title>
			</head>
			<body>
				<h1>OpenFDA Client</h1>
				<form method= "get" action="listDrugs">
					
					<input type = "submit" value="Drug List: Send to OpenFDA">
					</input>
				
					Limit:<input type='text' name='limit'></input>
				</form>
				
				<form method="get" action="searchDrug">
					<input type="submit" value="Drug Search ">
					<input type='text' name='drug'></input>
					
				</form>
				
				<form method= "get" action="listCompanies">
					
					<input type = "submit" value="Company list: Send to OpenFDA">
					</input>
					Limit:<input type='text' name='limit'></input>
				</form>
				
				<form method="get" action="searchCompany">
					<input type="submit" value="Company Search ">
					<input type='text' name='company'></input>
					
				</form>
				
				<form method="get" action="listGender">
					<input type="submit" value="Gender Search ">
					Limit:<input type='text' name='gender'></input>
					
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
					<h1>ERROR 404 </h1>
				</body>
			</html>"""
		return html
		
	def do_GET(self):
		main_page=False
		is_event=False
		is_search=False
		is_event_company=False
		is_search_company=False
		is_search_gender=False
		
		if self.path == "/":
			main_page=True
		elif "/listDrugs" in self.path:
			is_event=True
			url=self.path
			url_lista=url.split('=')
			limit=url_lista[1]
		elif '/searchDrug' in self.path:
			is_search=True
			url=self.path
			url_lista=url.split('=')
			drug=url_lista[1]
		elif '/listCompanies' in self.path:
			is_event_company=True
			url=self.path
			url_lista=url.split('=')
			limit=url_lista[1]
		elif '/searchCompany' in self.path:
			is_search_company=True
			url=self.path
			url_lista=url.split('=')
			company=url_lista[1]
		elif '/listGender' in self.path:
			is_search_gender=True
			url=self.path
			url_lista=url.split('=')
			gender=url_lista[1]
			
			
        # Send response status code
		

		
        # Send message back to client
        #message = "Hello world! " + self.path


        # Write content as utf-8 data
		if main_page :
			html=self.get_main_page()
			self.send_response(200)
		elif is_event :
			
			event = self.get_event(limit)
			cc=self.drug_list(event)
			html= self.drug_page(cc)
			self.send_response(200)
		elif is_search :
			drugs=self.get_search(drug)
			cc=self.companynumb(drugs)
			html=self.drug_page(cc)
			self.send_response(200)
		elif is_event_company :
			event = self.get_event(limit)
			company=self.companynumb(event)
			html=self.drug_page(company)
			self.send_response(200)
		elif is_search_company :
			companys=self.get_search_company(company)
			cc=self.company(companys)
			html=self.drug_page(cc)
			self.send_response(200)
		elif is_search_gender :
			event = self.get_event(gender)
			cc= self.gender_list(event)
			html= self.gender_page(cc)
			self.send_response(200)
		else:
			html=self.errorhtml()
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

