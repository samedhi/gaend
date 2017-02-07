from google.cloud import bigquery
from google.cloud.bigquery import dataset
from google.cloud.bigquery.schema import SchemaField
import logging

# Not sure if the following helps
from oauth2client.client import GoogleCredentials
credentials = GoogleCredentials.get_application_default()

# Here we go http://gcloud-python.readthedocs.io/en/latest/bigquery-schema.html

GOOGLE_SERVICE_ACCOUNT = None

def put(json):
    client = bigquery.Client(project='gaend-157207')
    dataset = bigquery.dataset.Dataset("testing", client=client)


    if dataset.exists():
        logging.error("dataset already created")
    else:
        dataset.create()

    schema = [
        SchemaField(name='name', field_type='STRING'),
        SchemaField(name='breed', field_type='STRING'),
        SchemaField(name='born', field_type='DATETIME'),
    ]

    table = bigquery.table.Table("dogs", dataset, schema=schema)
    if table.exists():
        logging.error("table already created")
    else:
        table.create()
