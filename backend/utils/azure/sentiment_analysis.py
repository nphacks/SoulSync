from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ConnectionType
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import os

def sentiment_analysis(text: str):
    try:
        # Get project client
        project_connection_string = os.getenv("SENTIMENT_ANALYSIS_PROJECT_CONNECTION")
        project_client = AIProjectClient.from_connection_string(
            credential=DefaultAzureCredential(),
            conn_str=project_connection_string,
        )

        # Get the properties of the default Azure AI Services connection with credentials
        connection = project_client.connections.get_default(
        connection_type=ConnectionType.AZURE_AI_SERVICES,
        include_credentials=True, 
        )

        # Use the connection information to create a text analytics client
        ai_svc_credential = AzureKeyCredential(connection.key)
        text_analytics_client = TextAnalyticsClient(endpoint=connection.endpoint_url, credential=ai_svc_credential)

        # Use the Language service to analyze some text (to infer sentiment) 
        # text = "I watched a new movie. The movie was slow and long but was insightful."
        sentimentAnalysis = text_analytics_client.analyze_sentiment(documents=[text])[0]
        return sentimentAnalysis

    except Exception as ex:
        print("Error in sentiment analysis", ex)

