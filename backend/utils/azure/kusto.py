from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.ingest import QueuedIngestClient, IngestionProperties
from azure.kusto.ingest.ingestion_properties import DataFormat
from utils.cosmos.journal_entry import get_user_entries
from io import BytesIO
import json
from bson import ObjectId
from datetime import datetime
import os

# ADX connection details
cluster = os.getenv("KUSTO_CLUSTER")
db_name = os.getenv("KUSTO_DB_NAME")
table_name = os.getenv("KUSTO_TABLE_NAME")
kcsb = KustoConnectionStringBuilder.with_az_cli_authentication(cluster)
ingest_client = QueuedIngestClient(kcsb)

 # Sample data to ingest
def add_data():
    # Ingestion properties
    ingest_props = IngestionProperties(
        database=db_name,
        table=table_name,
        data_format=DataFormat.JSON
    )
   
    data = [
        {"name": "Alice", "entryTime": "2025-04-01", "entryText": "Sample entry", "user_id": "1"},
        {"name": "Bob", "entryTime": "2025-04-02", "entryText": "Another entry", "user_id": "2"}
    ]

    # Ingest data
    for entry in data:
        print('Injesting data in ADX ...')
        json_data = json.dumps(entry)
        ingest_client.ingest_from_stream(BytesIO(json_data.encode()), ingest_props)

    return

def serialize_entry(entry):
    def convert(val):
        if isinstance(val, ObjectId):
            return str(val)
        elif isinstance(val, datetime):
            return val.isoformat()
        elif isinstance(val, dict):
            return {k: convert(v) for k, v in val.items()}
        elif isinstance(val, list):
            return [convert(v) for v in val]
        else:
            return val

    return {k: convert(v) for k, v in entry.items()}

def add_user_entries_to_adx(user_id: str):
    entries = get_user_entries(user_id)

    ingest_props = IngestionProperties(
        database=db_name,
        table=table_name,
        data_format=DataFormat.JSON
    )

    for entry in entries:
        entry = serialize_entry(entry)
        json_data = json.dumps(entry)
        ingest_client.ingest_from_stream(BytesIO(json_data.encode()), ingest_props)


def run_query(index: int):
    query = [
        'journal_entry | summarize avg(text_emotion_score), avg(speech_emotion_score) by bin(timestamp, 1d), user_id | order by timestamp desc',
        'journal_entry | summarize count() by text_emotion, speech_emotion | top 5 by count_',
        'journal_entry | where user_id == "507f1f77bcf86cd799439011" | summarize count() by sentiment',
        'journal_entry | summarize avg(sentiment_score) by bin(timestamp, 7d) | order by timestamp desc',
        'journal_entry | summarize count() by journal_type',
        'journal_entry | summarize entries = count() by user_id | top 10 by entries',
        'journal_entry | project sentiment_score, text_emotion_score, speech_emotion_score'
    ]
    kcsb = KustoConnectionStringBuilder.with_az_cli_authentication(cluster)
    client = KustoClient(kcsb)
    print("KUSTO  => ", client, db_name)
    response = client.execute(db_name, query[index])
    print("KUSTO Response => ", response.primary_results[0])
    for row in response.primary_results[0]:
        print('ROW --> ', row.to_dict())

    return response.primary_results[0]




