"""
Step 3: SOAP Service Returning a Raw XML Document String
WSDL: https://graphical.weather.gov/xml/SOAP_server/ndfdXMLserver.php?wsdl

This NOAA National Weather Service operation returns a literal XML document string (<dwml>...</dwml>).
We parse the string with lxml.etree and display the structured XML elements.
"""

from zeep import Client
from lxml import etree

wsdl_url = "https://graphical.weather.gov/xml/SOAP_server/ndfdXMLserver.php?wsdl"

print(f"Connecting to NOAA Weather SOAP service at:\n{wsdl_url}\n")

# Initialize SOAP client
client = Client(wsdl=wsdl_url)

# Call operation that returns a complete XML document as a string
print("Calling LatLonListCityNames(displayLevel=1)...")
xml_document_string = client.service.LatLonListCityNames(displayLevel=1)

print("\n--- Raw XML Document (first 1000 characters) ---")
print(xml_document_string[:1000])
print("\n... [truncated] ...\n")

# Parse XML string into an element tree
root = etree.fromstring(xml_document_string.encode("utf-8"))

# Print root tag and namespace/attributes
print(f"XML Root Element Tag : {root.tag}")

# Find and display parsed data from the XML document
# NOAA DWML format contains cityNameList and latLonList
city_names_elem = root.find(".//cityNameList")
lat_lon_elem = root.find(".//latLonList")

if city_names_elem is not None and lat_lon_elem is not None:
    cities = city_names_elem.text.split("|")
    coords = lat_lon_elem.text.split(" ")
    
    print("\n--- Parsed Sample Data from the XML Document ---")
    for city, coord in zip(cities[:5], coords[:5]):
        print(f"  City: {city.strip():<20} Coordinates: {coord.strip()}")

# Pretty-print formatted XML snippet
print("\n--- Formatted XML Snippet ---")
snippet = etree.tostring(root, pretty_print=True, encoding="unicode")
print("\n".join(snippet.splitlines()[:30]))
print("...")
