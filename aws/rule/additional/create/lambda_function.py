import boto3
import json

headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
}

lambda_client = boto3.client('lambda')

def save_rule_in_db(rule):
    payload = rule
    response = lambda_client.invoke(
        FunctionName='SAVE_RULE_IN_DB_LAMBDA_ARN', # Replace with the ARN of the Save Rule in DB Lambda
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    response_payload = json.loads(response['Payload'].read().decode('utf-8'))
    body = json.loads(response_payload['body'])
    return body
    
def assign_to_primary_rule(primaryRuleId, conditionalRuleId):
    payload = {
        'primaryRuleId': primaryRuleId,
        'conditionalRuleId': conditionalRuleId
    }
    response = lambda_client.invoke(
        FunctionName='ASSIGN_TO_PRIMARY_RULE_LAMBDA_ARN', # Replace with the ARN of the Assign to Primary Rule Lambda
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    response_payload = json.loads(response['Payload'].read().decode('utf-8'))
    body = json.loads(response_payload['body'])
    return body

def run_commissioner():
    try:
        payload = {}
        response = lambda_client.invoke(
            FunctionName='COMMISSIONER_LAMBDA_ARN', # Replace with the ARN of the Commissioner Lambda
            InvocationType='Event',
            Payload=json.dumps(payload)
        )
        return {"status": "Commissioner run initiated"}
    except Exception as e:
        return {"status": "Error initiating Commissioner", "error": str(e)}

def lambda_handler(event, context):
    body = json.loads(event['body'])
    response = save_rule_in_db(body['rule'])
    assign_response = assign_to_primary_rule(body['primaryRuleId'], rule_creation_response['id'])
    run_commissioner_response = run_commissioner() 
            
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(response)
    }