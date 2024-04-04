import boto3
import json
import requests

lambda_client = boto3.client('lambda')

def get_plugin_configurations(pluginId, ruleId):
    payload = {
        'pluginId': pluginId,
        'ruleId':  ruleId
    }
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:us-east-1:100716272475:function:getPluginRuleAssignment', # Replace with the ARN of the getPluginRuleAssignment Lambda function
        InvocationType='RequestResponse',
        Payload = json.dumps(payload)
    )
    response_payload = json.loads(response['Payload'].read().decode('utf-8'))
    body = json.loads(response_payload['body'])
    return body

def lambda_handler(event, context):
    plugin = event.get('plugin')
    pluginId = plugin.get('id')
    name = plugin.get('name')
    capacity = plugin.get('capacity')
    connectUri = plugin.get('connectURL')
    defaultFrequency = plugin.get('frequency')
    
    configUri = connectUri + "/api/configuration"

    ruleId = event.get('ruleId')
    configs = get_plugin_configurations(pluginId, ruleId)
    
    if 'frequency' in configs:
        rule_frequency = configs['frequency']
        frequency = None
        if rule_frequency is not None:
            frequency = rule_frequency
    else:
        frequency = defaultFrequency

    payload = {
        "pluginId": pluginId,
        "name": name,
        "capacity": capacity,
        "frequency": frequency,
        "cloudUri": "https://y5g26uoeyc.execute-api.us-east-1.amazonaws.com/test/createMeasurement", # Replace with the URI of the createMeasurement Lambda function
        "measurementUri": connectUri + "/api/measurements",
        "configUri": configUri
    }
    
    response = requests.post(configUri, json=payload)
    
    return {
        "statusCode": response.status_code,
        "body": response.text
    }
