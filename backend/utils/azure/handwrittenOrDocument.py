from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
import numpy as np
import os

endpoint = os.getenv("DOCUMENT_VISION_ENDPOINT")
key = os.getenv("DOCUMENT_VISION_KEY")
region=os.getenv("DOCUMENT_VISION_REGION")


def analyze_read(image: str):
    
    document_intelligence_client  = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-read", AnalyzeDocumentRequest(url_source=image)
    )
    result = poller.result()

    print ("Document contains content: ", result.content)
    return result.content