import os
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Attr


def _table():
    table_name = os.getenv('DYNAMODB_INCIDENTS_TABLE')
    dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION'))
    return dynamodb.Table(table_name)


def _json_safe(value):
    if isinstance(value, Decimal):
        return int(value) if value % 1 == 0 else float(value)
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    return value


def list_incidents(filters=None, limit=100):
    filters = filters or {}
    scan_kwargs = {'Limit': limit}
    expressions = []

    if filters.get('severity'):
        expressions.append(Attr('severity').eq(filters['severity']))
    if filters.get('status'):
        expressions.append(Attr('status').eq(filters['status']))
    if filters.get('type'):
        expressions.append(Attr('finding_type').contains(filters['type']))

    if expressions:
        expression = expressions[0]
        for item in expressions[1:]:
            expression = expression & item
        scan_kwargs['FilterExpression'] = expression

    response = _table().scan(**scan_kwargs)
    items = [_json_safe(item) for item in response.get('Items', [])]
    items.sort(key=lambda x: x.get('timestamp', x.get('time', '')), reverse=True)
    return items


def get_incident(incident_id):
    response = _table().get_item(Key={'incident_id': incident_id})
    item = response.get('Item')
    return _json_safe(item) if item else None


def update_incident_status(incident_id, status):
    response = _table().update_item(
        Key={'incident_id': incident_id},
        UpdateExpression='SET #status = :status',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':status': status},
        ReturnValues='ALL_NEW',
    )
    return _json_safe(response.get('Attributes', {}))
