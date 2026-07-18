import os
import json
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


def invoke_incident_action(incident, action, approved_by):
    function_name = os.getenv('SECURITY_RESPONSE_LAMBDA_FUNCTION')
    if not function_name:
        raise ValueError('SECURITY_RESPONSE_LAMBDA_FUNCTION is not configured')

    instance_id = incident.get('instance_id') or incident.get('resource_id')
    if not instance_id or not str(instance_id).startswith('i-'):
        raise ValueError('Incident does not reference an EC2 instance')

    payload = {
        'action': action,
        'incident_id': incident['incident_id'],
        'instance_id': instance_id,
        'approved_by': approved_by,
    }
    client = boto3.client('lambda', region_name=os.getenv('AWS_REGION'))
    response = client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',
        Payload=json.dumps(payload).encode('utf-8'),
    )
    result = json.loads(response['Payload'].read() or '{}')
    if response.get('FunctionError'):
        raise RuntimeError(result.get('errorMessage', 'Security response Lambda failed'))

    body = result.get('body', result)
    return json.loads(body) if isinstance(body, str) else body
