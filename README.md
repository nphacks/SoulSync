# SoulSync – AI-Powered Mini Journaling App

SoulSync is a lightweight journaling app that supports voice, text, handwritten input, and chatbot interaction—powered by AI for sentiment and emotion analysis.

---

## Getting Started

### Frontend Setup (Angular)

```bash
cd frontend
npm install
ng serve
```

🔐 Login credentials for testing:
Email: alice@gmail.com

Password: alice123

### Backend Setup (FastAPI + Azure Services)

#### Environment Variables
Create a .env file in the backend directory and add the following:

```bash
AZURE_STORAGE_CONNECTION_STRING=your_value_here
AZURE_STORAGE_CONTAINER=your_container_name
YOUR_AZURE_SPEECH_KEY=your_value_here
YOUR_AZURE_ENDPOINT=your_value_here
DOCUMENT_VISION_ENDPOINT=your_value_here
DOCUMENT_VISION_KEY=your_value_here
DOCUMENT_VISION_REGION=your_region_here
JINA_API=your_jina_api_key
MONGODB_URI=your_cosmos_mongodb_connection_string
MONGODB_DB_NAME=your_db_name
SUBSCRIPTION_ID=your_azure_subscription_id
RESOURCE_NAME=your_resource_group
WORKSPACE_NAME=your_ml_workspace
OPENAI_ENDPOINT=your_openai_endpoint
OPENAI_MODEL_NAME=your_model_name
OPENAI_DEPLOYMENT=your_deployment_name
OPENAI_SUBSCRIPTION_KEY=your_openai_subscription_key
OPENAI_API_VERSION=2023-09-15-preview
KUSTO_CLUSTER=your_kusto_cluster_url
KUSTO_DB_NAME=your_kusto_db
KUSTO_TABLE_NAME=your_table_name
SENTIMENT_ANALYSIS_PROJECT_CONNECTION=your_project_connection_id
```

#### Run the Backend Server
```bash
uvicorn main:app --reload
```

#### Project Structure

```bash
SoulSync/
├── frontend/            # Angular frontend
├── backend/             # FastAPI backend
│   ├── main.py
│   ├── requirements.txt
│   └── ...
└── README.md
```

#### Notes
The app uses Azure Cognitive Services and Hugging Face models for emotion and sentiment analysis.

Graphs currently displayed in the app are real but screen-captured from Azure Data Explorer due to time constraints.

Vector search is implemented in Cosmos DB (Mongo API) to retrieve related journal entries via the chatbot.