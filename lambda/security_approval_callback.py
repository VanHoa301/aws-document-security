import base64
import html
import json
from urllib.parse import parse_qs

import boto3
from botocore.exceptions import ClientError


stepfunctions = boto3.client("stepfunctions")
VALID_DECISIONS = {"QUARANTINE", "STOP", "REJECT"}


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"content-type": "text/html; charset=utf-8"},
        "body": body,
    }


def request_method(event):
    return (
        event.get("requestContext", {}).get("http", {}).get("method")
        or event.get("httpMethod")
        or "GET"
    ).upper()


def request_values(event):
    values = dict(event.get("queryStringParameters") or {})
    body = event.get("body") or ""
    if event.get("isBase64Encoded") and body:
        body = base64.b64decode(body).decode("utf-8")
    if body:
        values.update(
            {key: items[0] for key, items in parse_qs(body).items() if items}
        )
    return values


def confirmation_page(decision, incident_id, task_token):
    safe_decision = html.escape(decision)
    safe_incident = html.escape(incident_id)
    safe_token = html.escape(task_token, quote=True)
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Security approval</title></head>
<body style="font-family:Arial;max-width:680px;margin:48px auto;padding:24px">
  <h1>Confirm security response</h1>
  <p><strong>Incident:</strong> {safe_incident}</p>
  <p><strong>Decision:</strong> {safe_decision}</p>
  <p>This decision can complete the waiting workflow only once.</p>
  <form method="post">
    <input type="hidden" name="decision" value="{safe_decision}">
    <input type="hidden" name="incident_id" value="{safe_incident}">
    <input type="hidden" name="task_token" value="{safe_token}">
    <button type="submit" style="padding:12px 18px">Confirm {safe_decision}</button>
  </form>
</body>
</html>"""


def lambda_handler(event, context):
    values = request_values(event)
    decision = values.get("decision", "").upper()
    incident_id = values.get("incident_id", "")
    task_token = values.get("task_token", "")

    if decision not in VALID_DECISIONS or not incident_id or not task_token:
        return response(400, "<h1>Invalid or incomplete approval request</h1>")

    if request_method(event) == "GET":
        return response(200, confirmation_page(decision, incident_id, task_token))

    if request_method(event) != "POST":
        return response(405, "<h1>Method not allowed</h1>")

    callback_output = {
        "decision": decision,
        "incident_id": incident_id,
        "approved_by": "email-approval-user",
    }

    try:
        stepfunctions.send_task_success(
            taskToken=task_token,
            output=json.dumps(callback_output),
        )
    except ClientError as exc:
        error_code = exc.response["Error"]["Code"]
        if error_code in {"InvalidToken", "TaskTimedOut", "TaskDoesNotExist"}:
            return response(409, "<h1>This approval link is invalid or already used</h1>")
        raise

    return response(
        200,
        f"<h1>Decision recorded</h1><p>{html.escape(decision)}: "
        f"{html.escape(incident_id)}</p>",
    )
