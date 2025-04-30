from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.ingest import QueuedIngestClient, IngestionProperties
from azure.kusto.ingest.ingestion_properties import DataFormat
from io import BytesIO
import json
import os

# ADX connection details
cluster = os.getenv("KUSTO_CLUSTER")
db_name = os.getenv("KUSTO_DB_NAME")
table_name = os.getenv("KUSTO_TABLE_NAME")
kcsb = KustoConnectionStringBuilder.with_az_cli_authentication(cluster)
ingest_client = QueuedIngestClient(kcsb)


def add_data():
    # Ingestion properties
    ingest_props = IngestionProperties(
        database=db_name,
        table=table_name,
        data_format=DataFormat.JSON
    )

    # Sample data to ingest
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

def run_query():
    query = "journal_entry | take 10"
    kcsb = KustoConnectionStringBuilder.with_az_cli_authentication(cluster)
    client = KustoClient(kcsb)
    print("KUSTO  => ", client, db_name)
    response = client.execute(db_name, query)
    print("KUSTO Response => ", response.primary_results[0])
    for row in response.primary_results[0]:
        print('ROW --> ', row.to_dict())

    return




