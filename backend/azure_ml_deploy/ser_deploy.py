from azure.ai.ml import MLClient
from azure.ai.ml.entities import Model
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import CodeConfiguration
import os

# ml_client = MLClient(DefaultAzureCredential(), "<subscription-id>", "<resource-name>", "<workspace-name>")
ml_client = MLClient(DefaultAzureCredential(), os.getenv("SUBSCRIPTION_ID"), os.getenv("RESOURCE_NAME"), os.getenv("WORKSPACE_NAME"))

model = Model(
    path="SER/registry",
    name="speech_emotion_model",
    description="Emotion detection model",
    type="custom_model"
)

registered_model = ml_client.models.create_or_update(model)

from azure.ai.ml.entities import ManagedOnlineEndpoint

endpoint = ManagedOnlineEndpoint(
    name="speech-emotion-endpoint-1",
    description="Endpoint for emotion detection model"
)

ml_client.begin_create_or_update(endpoint).result()

from azure.ai.ml.entities import Environment

env = Environment(
    name="ser_environment_8",
    version="1",
    conda_file="SER/conda_env.yml",
    image="mcr.microsoft.com/azureml/minimal-ubuntu22.04-py39-cuda11.8-gpu-inference:latest"
    # image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04",
    # image="mcr.microsoft.com/azureml/tensorflow-2.10-ubuntu20.04-py38-cuda11-gpu:latest",  # GOOD IMAGE
    # image="mcr.microsoft.com/azureml/curated/tensorflow-2.16-cuda12:11",
)

ml_client.environments.create_or_update(env)


from azure.ai.ml.entities import ManagedOnlineDeployment

deployment = ManagedOnlineDeployment(
    name="emotion-deployment-1",
    endpoint_name=endpoint.name,
    model=registered_model.id,
    code_configuration=CodeConfiguration(
        code="SER/registry",
        scoring_script="score.py"
    ),
    environment=env,
    instance_type="Standard_F2s_v2",
    instance_count=1
)

ml_client.begin_create_or_update(deployment).result()
deployment_state = ml_client.online_deployments.get(name="emotion-deployment-1", endpoint_name="speech-emotion-endpoint-1")

endpoint.traffic = {"emotion-deployment-1": 100}
ml_client.begin_create_or_update(endpoint).result()