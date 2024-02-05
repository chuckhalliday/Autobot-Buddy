import requests
import json
import io
from PyPDF2 import PdfReader
from products.models import VehicleAttachment, File

def fetch_data(vin):
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}*BA?format=json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        
        data = response.json()
        
        vehicle_object = data.get("Results", [])
        
        if vehicle_object:
            year = vehicle_object[10].get("Value", "")
            make = vehicle_object[7].get("Value", "").lower()
            trim = vehicle_object[13].get("Value", "").lower()
            model = vehicle_object[9].get("Value", "").lower()
            
            return {
                "vehicle_model": f"{year} {make.capitalize()} {model.capitalize()} {trim.capitalize()}",
                "vehicle_handle": f"{year}{make}{model}",
                "year": year,
                "make": make,
                "model": model,
                "show_text": True
            }
        
    except requests.exceptions.RequestException as e:
        print(f"Something went wrong: {e}")
    
    return None

def extract_text_from_url_pdf(url: str, vehicle: str, obj: str):
    file_name = f"{vehicle}.txt"
    file_instance = File.objects.filter(name=vehicle).first()

    if not file_instance:
        
    # Download the PDF content from the URL
        response = requests.get(url)

    # Check if the request was successful (status code 200)
        if response.status_code == 200:
            binary_content = response.content

            pdf_content = io.BytesIO(binary_content)
            with pdf_content as pdf_file:
                reader = PdfReader(pdf_file)
                number_of_pages = len(reader.pages)
            
                pdf_text = ""
                for i in range(number_of_pages):
                    page = reader.pages[i]
                    pdf_text += page.extract_text()
                    pdf_text += "\n"

        else:
            print(f"Failed to download PDF. Status code: {response.status_code}")

    
        file_instance = File(name=vehicle)
        file_instance.file.save(file_name, io.BytesIO(pdf_text.encode('utf-8')))
        attachment_instance = VehicleAttachment(vehicle=obj, file=file_instance)
        attachment_instance.save()

        
    else:
        print(f"File '{file_name}' already exists. Skipping creation.")
        attachment_instance = VehicleAttachment(vehicle=obj, file=file_instance)
        attachment_instance.save()