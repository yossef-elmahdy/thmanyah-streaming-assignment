from google.cloud import bigquery
from app.config import BQ_CREDENTIALS_PATH, BQ_TABLE_ID


bq_client = bigquery.Client.from_service_account_json(BQ_CREDENTIALS_PATH)


def ensure_table_exists(row):
    try:
        bq_client.get_table(BQ_TABLE_ID)
    except Exception:
        schema = [
            bigquery.SchemaField(key, "STRING") if isinstance(value, str) else
            bigquery.SchemaField(key, "FLOAT") if isinstance(value, float) else
            bigquery.SchemaField(key, "INTEGER")
            for key, value in row.items()
        ]
        table = bigquery.Table(BQ_TABLE_ID, schema=schema)
        bq_client.create_table(table)
        print(f"Table created: {BQ_TABLE_ID}")


def insert_to_bigquery(row):
    try:
        ensure_table_exists(row)
        errors = bq_client.insert_rows_json(BQ_TABLE_ID, [row])
        if errors:
            print(f"[BigQuery] Insert errors: {errors}")
        else:
            print(f"Inserted to BigQuery: {row['content_id']}")
    except Exception as e:
        print(f"BigQuery error: {e}")
