import requests
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
import os

ml_client = MLClient(DefaultAzureCredential(), os.getenv("SUBSCRIPTION_ID"), os.getenv("RESOURCE_NAME"), os.getenv("WORKSPACE_NAME"))
keys = ml_client.online_endpoints.get_keys("speech-emotion-endpoint")

endpoint_url = "https://<name>.<region>.inference.ml.azure.com/score"
api_key = keys.primary_key

# print('API => ', api_key)

# headers = {
#     "Content-Type": "application/octet-stream",
#     "Authorization": api_key,
#     "azureml-model-key": api_key
# }

# with open("test.wav", "rb") as f:
#     audio_data = f.read()

# print('Audio Data opened')

# response = requests.post(endpoint_url, headers=headers, data=audio_data)

# print("Response:", response.json())

from azureml.core import Workspace
from azureml.core.webservice import Webservice

# Connect to the Azure ML workspace
ws = Workspace.from_config(path="config/config.json")

# Retrieve the deployed model
service = Webservice(name="speech-emotion-endpoint", workspace=ws)

# Check if the model is healthy
print(service.state)