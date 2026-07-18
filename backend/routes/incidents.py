from flask import Blueprint, jsonify, request
from botocore.exceptions import BotoCoreError, ClientError

from middleware.auth_middleware import require_auth, require_role
from services.incident_service import (
    get_incident,
    invoke_incident_action,
    list_incidents,
    update_incident_status,
)

incidents_bp = Blueprint('incidents', __name__)


@incidents_bp.route('/incidents', methods=['GET'])
@require_auth
def incidents():
    filters = {
        'severity': request.args.get('severity'),
        'status': request.args.get('status'),
        'type': request.args.get('type'),
    }
    limit = min(int(request.args.get('limit', 100)), 200)

    try:
        return jsonify(list_incidents(filters=filters, limit=limit))
    except (BotoCoreError, ClientError) as exc:
        return jsonify({'error': 'Cannot load security incidents', 'detail': str(exc)}), 502


@incidents_bp.route('/incidents/<incident_id>', methods=['GET'])
@require_auth
def incident_detail(incident_id):
    try:
        incident = get_incident(incident_id)
    except (BotoCoreError, ClientError) as exc:
        return jsonify({'error': 'Cannot load incident detail', 'detail': str(exc)}), 502

    if not incident:
        return jsonify({'error': 'Incident not found'}), 404
    return jsonify(incident)


@incidents_bp.route('/incidents/<incident_id>/status', methods=['PATCH'])
@require_auth
@require_role('admin')
def incident_status(incident_id):
    status = (request.get_json() or {}).get('status', '').strip().upper()
    if status not in {'OPEN', 'INVESTIGATING', 'RESOLVED'}:
        return jsonify({'error': 'Status must be OPEN, INVESTIGATING, or RESOLVED'}), 400

    try:
        return jsonify(update_incident_status(incident_id, status))
    except (BotoCoreError, ClientError) as exc:
        return jsonify({'error': 'Cannot update incident status', 'detail': str(exc)}), 502


def _run_incident_action(incident_id, action):
    try:
        incident = get_incident(incident_id)
        if not incident:
            return jsonify({'error': 'Incident not found'}), 404
        result = invoke_incident_action(incident, action, request.current_user)
        return jsonify({'result': result, 'incident': get_incident(incident_id)})
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400
    except (BotoCoreError, ClientError, RuntimeError) as exc:
        return jsonify({'error': 'Security response action failed', 'detail': str(exc)}), 502


@incidents_bp.route('/incidents/<incident_id>/quarantine', methods=['POST'])
@require_auth
@require_role('admin')
def quarantine_incident(incident_id):
    return _run_incident_action(incident_id, 'QUARANTINE_APPROVED')


@incidents_bp.route('/incidents/<incident_id>/restore', methods=['POST'])
@require_auth
@require_role('admin')
def restore_incident(incident_id):
    return _run_incident_action(incident_id, 'RESTORE_APPROVED')


@incidents_bp.route('/incidents/<incident_id>/stop', methods=['POST'])
@require_auth
@require_role('admin')
def stop_incident(incident_id):
    return _run_incident_action(incident_id, 'STOP_APPROVED')
