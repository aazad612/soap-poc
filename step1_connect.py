"""
Step 1: Connecting to a SOAP Service with Python
WSDL: http://www.dneonline.com/calculator.asmx?wsdl
"""

from zeep import Client

# 1. Define the WSDL URL (the service contract)
wsdl_url = "http://www.dneonline.com/calculator.asmx?wsdl"

print(f"Connecting to SOAP service at: {wsdl_url}...")

# 2. Initialize the SOAP client
# Zeep reads the WSDL and automatically builds Python bindings for all operations.
client = Client(wsdl=wsdl_url)

print("Connected successfully!\n")

# 3. Call 1 simple operation: Add(intA=10, intB=25)
a = 10
b = 25
result = client.service.Add(intA=a, intB=b)

print(f"Operation: Add({a}, {b})")
print(f"Result from SOAP service: {result}")
