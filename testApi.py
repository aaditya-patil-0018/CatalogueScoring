'''
testApi
    This file is used for testing our API
'''

# This program is basically to test the API

# importing the needed modules
import requests

BASE = "http://127.0.0.1:8000/score"

inputFile = input("Enter file name: ")

# Function to load JSON data from file
def load_from_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()  # Read the file before closing

File = load_from_file(inputFile)
filetype = inputFile.split(".")[-1]
if filetype == "json":
    files = {'json': File}  # Prepare the file to be sent in the request
elif filetype == "csv":
    files = {'csv': File}
elif filetype == "xlsx":
    files = {'xlsx': File}

response = requests.put(BASE, files=files)  # Pass files=files to send the file
print(response.json())
