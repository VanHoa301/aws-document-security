import boto3
import os
from datetime import datetime


def get_table(table_name):
    dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION'))
    return dynamodb.Table(table_name)


def save_document_metadata(doc_id, filename, uploader, size):
    table = get_table(os.getenv('DYNAMODB_DOCUMENTS_TABLE'))
    table.put_item(Item={
        'document_id': doc_id,
        'filename': filename,
        'uploader': uploader,
        'size': size,
        'uploaded_at': datetime.utcnow().isoformat()
    })


def list_documents():
    table = get_table(os.getenv('DYNAMODB_DOCUMENTS_TABLE'))
    response = table.scan()
    items = response.get('Items', [])
    items.sort(key=lambda x: x.get('uploaded_at', ''), reverse=True)
    return items


def get_document(doc_id):
    table = get_table(os.getenv('DYNAMODB_DOCUMENTS_TABLE'))
    response = table.get_item(Key={'document_id': doc_id})
    return response.get('Item')


def delete_document(doc_id):
    table = get_table(os.getenv('DYNAMODB_DOCUMENTS_TABLE'))
    table.delete_item(Key={'document_id': doc_id})
