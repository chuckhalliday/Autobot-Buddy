import requests
import json
import io
from PyPDF2 import PdfReader

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
                "vehicle_model": f"{year} {make} {model} {trim}",
                "year": year,
                "make": make,
                "model": model,
                "show_text": True
            }
        
    except requests.exceptions.RequestException as e:
        print(f"Something went wrong: {e}")
    
    return None

def extract_text_from_url_pdf(url: str):
    # Download the PDF content from the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Create a file-like object from the content
        binary_content = response.content

    # Convert binary content to a BytesIO object
        pdf_content = io.BytesIO(binary_content)
        # Use PyPDF2 to read the PDF content
        reader = PdfReader(pdf_content)

        number_of_pages = len(reader.pages)

        pdf_text = ""

        for i in range(number_of_pages):
            page = reader.pages[i]
            pdf_text += page.extract_text()
            pdf_text += "\n"

        # Specify the file path for the new text file
        # Adjust this path as needed
        file_path = "extracted_text.txt"

        # Write the content to the text file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(pdf_text)
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")