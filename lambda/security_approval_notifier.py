import os
from urllib.parse import urlencode

import boto3


sns = boto3.client("sns")

SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]
APPROVAL_API_URL = os.environ["APPROVAL_API_URL"].rstrip("/")


def lambda_handler(event, context):
    task_token = event.get("task_token", "")
    incident_id = event.get("incident_id", "")
    instance_id = event.get("instance_id", "")
    severity = event.get("severity", "UNKNOWN")
    severity_score = event.get("severity_score", 0)

    if not task_token or not incident_id or not instance_id:
        raise ValueError("task_token, incident_id, and instance_id are required")

    def decision_url(decision):
        query = urlencode(
            {
                "decision": decision,
                "incident_id": incident_id,
                "task_token": task_token,
            }
        )
        return f"{APPROVAL_API_URL}?{query}"

    message = (
        "SECURITY RESPONSE APPROVAL REQUIRED\n\n"
        f"Incident: {incident_id}\n"
        f"Instance: {instance_id}\n"
        f"Severity: {severity} ({severity_score})\n\n"
        "Choose one response:\n\n"
        f"APPROVE QUARANTINE:\n{decision_url('QUARANTINE')}\n\n"
        f"APPROVE STOP:\n{decision_url('STOP')}\n\n"
        f"REJECT:\n{decision_url('REJECT')}\n\n"
        "Each approval link can complete the waiting workflow only once."
    )

    response = sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=f"[SECURITY APPROVAL] {severity} - {instance_id}"[:100],
        Message=message,
    )

    return {
        "message": "Approval email sent",
        "incident_id": incident_id,
        "message_id": response["MessageId"],
    }
