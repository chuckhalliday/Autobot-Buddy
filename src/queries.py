import requests
import json
import io
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter # for splitting text in smaller snippets
import os # for reading environment variables
from dotenv import load_dotenv # for loading environment variables
from openai import OpenAI # openai api
from numpy import dot
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
EMBEDDING_MODEL = "text-embedding-ada-002"
CHUNK_SIZE = 1000 # chunk size of snippets
CHUNK_OVERLAP = 200 # check size to create overlap between snippets
CONFIDENCE_SCORE = 0.75 # for filtering search results. [0,1] prefered: 0.75 or greater

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
    file_instance = File.objects.filter(file=file_name).first()

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

    
        file_instance = File(name=vehicle, filetype='txt')
        file_instance.file.save(file_name, io.BytesIO(pdf_text.encode('utf-8')))
        attachment_instance = VehicleAttachment(vehicle=obj, file=file_instance)
        attachment_instance.save()

        
    else:
        print(f"File '{file_name}' already exists. Skipping creation.")
        attachment_instance = VehicleAttachment(vehicle=obj, file=file_instance)
        attachment_instance.save()


def create_embeddings(file_path: str, vehicle: str, obj: str):
    file_name = f"{vehicle}.json"
    file_instance = File.objects.filter(file=file_name).first()

    if not file_instance:
    
        snippets = []
        #Initialize a CharacterTextSplitter with specified settings
        text_splitter = CharacterTextSplitter(separator="\n",
                                         chunk_size=CHUNK_SIZE,
                                         chunk_overlap=CHUNK_OVERLAP,
                                         length_function=len)

    # Read the content of the file specified by file_path
        with open(file_path, "r", encoding="utf-8") as file:
                file_text = file.read()

    # Split the text into snippets using the specified settings
        snippets = text_splitter.split_text(file_text)

    
        client = OpenAI(api_key=OPENAI_API_KEY)
    
    # Request embeddings for the snippets using the specified model
        response = client.embeddings.create(input=snippets,model=EMBEDDING_MODEL)
    
    # Extract embeddings from the API response
        embedding_list = [response_object.embedding for response_object in response.data]

    # Create a JSON object containing embeddings and snippets
        embedding_json = {
            'embeddings': embedding_list,
            'snippets': snippets
        }
    
    # Convert the JSON object to a formatted JSON string
        json_object = json.dumps(embedding_json, indent=4)

        file_instance = File(name=vehicle, filetype='json')
        file_instance.file.save(file_name, io.BytesIO(json_object.encode('utf-8')))
        attachment_instance = VehicleAttachment(vehicle=obj, file=file_instance)
        attachment_instance.save()

    else:
        print(f"File '{file_name}' already exists. Skipping creation.")
        attachment_instance = VehicleAttachment(vehicle=obj, file=file_instance)
        attachment_instance.save()


def get_embeddings(extracted_json_path: str):
    
    # Open the JSON file containing embeddings and snippets
    with open(extracted_json_path,'r') as file:
        # Load the JSON data into a Python dictionary
        embedding_json = json.load(file)
        
    # Return the embeddings and snippets from the loaded JSON
    return embedding_json['embeddings'], embedding_json['snippets']


def user_question_embedding_creator(question: str):
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # Request embedding for the provided question using the specified model
    response = client.embeddings.create(input=question,model=EMBEDDING_MODEL)
    
    # Extract and return the embedding from the API response
    return response.data[0].embedding


def answer_users_question(user_question, embeddings, snippets, gpt_model):
    
    try:
        # Create an embedding for the user's question
        user_question_embedding = user_question_embedding_creator(user_question)
    except Exception as e:
        # Handle any exception that occurred while using Embedding API.
        return f"An error occurred while creating embedding: {str(e)}"
        
    
    # Calculate cosine similarities between the user's question embedding and the document embeddings
    cosine_similarities = []
    for embedding in embeddings:
        cosine_similarities.append(dot(user_question_embedding,embedding))

    # Pair snippets with their respective cosine similarities and sort them by similarity
    scored_snippets = zip(snippets, cosine_similarities)
    sorted_snippets = sorted(scored_snippets, key=lambda x: x[1], reverse=True)
    
    # Filter snippets based on a confidence score and select the top 5 results
    formatted_top_results = [snipps for snipps, _score in sorted_snippets if _score > CONFIDENCE_SCORE]
    if len(formatted_top_results) > 5:
        formatted_top_results = formatted_top_results[:5]
        
    # Create the chatbot system using pdf_description provided by the user.
    chatbot_system = f"""You are provided with SEARCH RESULTS from a pdf. You need to generate answer to the user's question based on the given SEARCH RESULTS. SEARCH RESULTS as a python list. SEARCH RESULTS and USER's QUESTION are delimited by ``` \n If there is no information available, or question is irrelevent respond with - "Sorry! I can't help you." """
    
    # Create the prompt using results and user's question.
    prompt = f"""\
    SEARCH RESULTS:
    ```
    {formatted_top_results}
    ```
    USER'S QUESTION:
    ```
    {user_question}
    ```
    
    """
    
    # Prepare the chat conversation and use GPT model for generating a response
    messages = [{'role':'system', 'content':chatbot_system},
                {'role':'user', 'content':prompt}]
    
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        completion = client.chat.completions.create(model=gpt_model,
                                             messages=messages,
                                             temperature=0,
                                             stream=False)
    except Exception as e:
        # Handle exception while communicating with ChatCompletion API
        return f"An error occurred with chatbot: {str(e)}"
        
    # Return the chatbot response.
    return completion.choices[0].message.content