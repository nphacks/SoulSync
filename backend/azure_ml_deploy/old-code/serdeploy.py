from azureml.core import Workspace, Model  
from azureml.core.webservice import AciWebservice  
from azureml.core.model import InferenceConfig
from azureml.core.environment import Environment

ws = Workspace.from_config(path="config/config.json")  
model = Model.register(
    ws, 
    model_name="emotion_model", 
    model_path="SER/registry",  # Folder containing BOTH .h5 and .npy
    description="Model + Scaler"
)
print('Model => ', model)

# Create environment (add conda/pip dependencies if needed)
env = Environment.from_conda_specification(name="myenv", file_path="SER/conda_env.yml")

print('ENV => ', env)

# Define inference config (point to scoring script)
inference_config = InferenceConfig(
    entry_script="SER/registry/score.py",  # Your scoring script (see below)
    environment=env
)

print('Inference Config => ', inference_config)

# # Deploy to ACI  
aci_config = AciWebservice.deploy_configuration(
    cpu_cores=2,  # Increased from 1
    memory_gb=4,  # Increased from 2
    auth_enabled=True,
    enable_app_insights=True  # For better logging
)
print('ACI Config => ', aci_config)
try:
    service = Model.deploy(
        workspace=ws,
        name="emotion-service",
        models=[model],
        deployment_config=aci_config,
        inference_config=inference_config,
        overwrite=True  # Only if fixing a previous deploy
    )
    service.wait_for_deployment(show_output=True)
    print('LOGS: ', service.get_logs())
    print(f"Scoring URI: {service.scoring_uri}")

except Exception as e:
    print(f"Deployment failed: {e}")
    if 'service' in locals():  # Check logs if deployment was attempted
        print("LOGS:", service.get_logs())

print('DONE!')