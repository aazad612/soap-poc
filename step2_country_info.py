"""
Step 2: SOAP Service with Complex XML Structures
WSDL: http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL

This service returns complex XML with nested elements, arrays, and objects.
We also use Zeep's HistoryPlugin to capture the exact raw XML response document.
"""

from zeep import Client
from zeep.plugins import HistoryPlugin
from lxml import etree
from zeep.helpers import serialize_object
import json 


wsdl_url = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL"

print(f"Connecting to Country Info SOAP service at:\n{wsdl_url}\n")

# Use HistoryPlugin to capture the raw HTTP and XML envelopes
history = HistoryPlugin()
client = Client(wsdl=wsdl_url, plugins=[history])

# Call FullCountryInfo for the United States ("US")
iso_code = "US"
print(f"Calling FullCountryInfo(sCountryISOCode='{iso_code}')...")
country = client.service.FullCountryInfo                         (sCountryISOCode=iso_code)

# print(type(country))  

# data = serialize_object(country)
# print(json.dumps(data, indent=2))

# fields = [attr for attr in dir(country) if not attr.startswith('_')]
# print(fields)

# print("\n--- Deserialized Python Object ---")
# print(f"Country Name : {country.sName}")
# print(f"Capital City : {country.sCapitalCity}")
# print(f"Phone Code   : {country.sPhoneCode}")
# print(f"Currency     : {country.sCurrencyISOCode}")
# print(f"Flag URL     : {country.sCountryFlag}")

# # Languages is a list of complex types (tLanguage)
# print("Languages    :")
# for lang in country.Languages.tLanguage:
#     print(f"  - {lang.sName} ({lang.sISOCode})")

# # Print the actual raw XML document received from the service
# print("\n--- Raw XML Document Received from SOAP Service ---")
# raw_xml_envelope = history.last_received["envelope"]
# pretty_xml = etree.tostring(raw_xml_envelope, pretty_print=True, encoding="unicode")
# print(pretty_xml)


#=======

countries = client.service.ListOfCountryNamesByName()
print(f"Total countries: {len(countries)}")