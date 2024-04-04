import boto3
import json
from datetime import datetime
from enum import Enum
from zoneinfo import ZoneInfo

lambda_client = boto3.client('lambda')

CURR_TIME_STR = datetime.now(ZoneInfo("Europe/Vienna")).strftime('%Y-%m-%d %H:%M:%S')
CURR_TIME = datetime.now(ZoneInfo("Europe/Vienna"))

class ComparisonOperator(Enum):
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    GREATER_THAN = "GREATER_THAN"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN_OR_EQUAL = "GREATER_THAN_OR_EQUAL"
    LESS_THAN_OR_EQUAL = "LESS_THAN_OR_EQUAL"

class LogicalOperator(Enum):
    AND = "AND"
    OR = "OR"
    NOT = "NOT"

def log_state(ruleId, description):
    payload = {
        'ruleId': ruleId,
        'description': description,
        'timestamp': CURR_TIME_STR
    }
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:us-east-1:100716272475:function:createLog', # Replace with the ARN of the createLog function
        InvocationType='RequestResponse',
        Payload = json.dumps(payload)
    )
    response_payload = json.loads(response['Payload'].read().decode('utf-8'))
    body = json.loads(response_payload['body'])
    return body

def log_error_state(description):
    payload = {
        'ruleId': 1,
        'description': description,
        'timestamp': CURR_TIME_STR
    }
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:us-east-1:100716272475:function:createLog', # Replace with the ARN of the createLog function
        InvocationType='RequestResponse',
        Payload = json.dumps(payload)
    )
    response_payload = json.loads(response['Payload'].read().decode('utf-8'))
    body = json.loads(response_payload['body'])
    return body

def get_all_primary_rules():
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:us-east-1:100716272475:function:getPrimaryRulesAll', # Replace with the ARN of the getPrimaryRulesAll function
        InvocationType='RequestResponse',
        Payload = json.dumps({})
    )
    response_payload = json.loads(response['Payload'].read().decode('utf-8'))
    body = json.loads(response_payload['body'])
    if 'rules' in body:
        return body['rules']
    return []

def get_log_latest():
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:us-east-1:100716272475:function:getLatestLog', # Replace with the ARN of the getLatestLog function
        InvocationType='RequestResponse',
        Payload = json.dumps({})
    )
    response_payload = json.loads(response['Payload'].read().decode('utf-8'))
    body = json.loads(response_payload['body'])
    return body

def get_all_plugins():
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:us-east-1:100716272475:function:getAllPlugins', # Replace with the ARN of the getAllPlugins function
        InvocationType='RequestResponse',
        Payload = json.dumps({})
    )
    response_payload = json.loads(response['Payload'].read().decode('utf-8'))
    body = json.loads(response_payload['body'])
    return body['plugins']

def get_iot_devices_by_plugin(pluginId):
    payload = {
        "pluginId": pluginId
    }
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:us-east-1:100716272475:function:getAllPluginIoTDeviceAssignments', # Replace with the ARN of the getAllPluginIoTDeviceAssignments function
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    response_payload = json.loads(response['Payload'].read().decode('utf-8'))
    body = json.loads(response_payload['body'])
    if 'assignments' in body:
        return body['assignments']
    return []

def get_conditional_rules(primaryRuleId):
    payload = {
        'primaryRuleId': primaryRuleId
    }
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:us-east-1:100716272475:function:getRuleAssignmentByPrimaryRuleId', # Replace with the ARN of the getRuleAssignmentByPrimaryRuleId function
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    response_payload = json.loads(response['Payload'].read().decode('utf-8'))
    body = json.loads(response_payload['body'])
    if 'assignments' in body:
        return body['assignments']
    return []

def get_latest_measurement_by_plugin_id(pluginId):
    payload = {
        'pluginId': pluginId
    }
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:us-east-1:100716272475:function:getMeasurementLatestByPluginId', # Replace with the ARN of the getMeasurementLatestByPluginId function
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    response_payload = json.loads(response['Payload'].read().decode('utf-8'))
    body = json.loads(response_payload['body'])
    return body

def get_conditional_rule(id):
    payload = {
        'ruleId': id
    }
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:us-east-1:100716272475:function:getConditionalRuleById', # Replace with the ARN of the getConditionalRuleById function
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    response_payload = json.loads(response['Payload'].read().decode('utf-8'))
    body = json.loads(response_payload['body'])
    return body

def run_plugin_deployer(plugin, ruleId):
    payload = {
        'plugin': plugin,
        'ruleId': ruleId
    }
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:us-east-1:100716272475:function:pluginDeployer', # Replace with the ARN of the pluginDeployer function
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    response_payload = json.loads(response['Payload'].read().decode('utf-8'))
    return response_payload


def deploy_plugins(ruleId):
    plugins = get_all_plugins()
    for plugin in plugins:
        run_plugin_deployer(plugin, ruleId)

def compare_values(op, value1, value2):
    if op == ComparisonOperator.EQUAL.name:
        return value1 == value2
    elif op == ComparisonOperator.NOT_EQUAL.name:
        return value1 != value2
    elif op == ComparisonOperator.GREATER_THAN.name:
        return value1 > value2
    elif op == ComparisonOperator.LESS_THAN.name:
        return value1 < value2
    elif op == ComparisonOperator.GREATER_THAN_OR_EQUAL.name:
        return value1 >= value2
    elif op == ComparisonOperator.LESS_THAN_OR_EQUAL.name:
        return value1 <= value2
    else:
        raise ValueError(f'Unsupported operation {op}')

def evaluate_conditional_rules(primary_rule):
    conditional_rules = get_conditional_rules(primary_rule['id'])
    primary_rule_logical_op = primary_rule['logicalOperator']
    
    comparison_results = []
    if len(conditional_rules) == 0:
        return True
    
    for rule in conditional_rules:
        conditional_rule_id = rule['conditionalRuleId']
        conditional_rule = get_conditional_rule(conditional_rule_id)
        measurement_value = get_latest_measurement_by_plugin_id(conditional_rule['pluginId'])
        is_rule_satisfied = compare_values(conditional_rule['comparisonOperator'], measurement_value['value'], conditional_rule['value'])
        comparison_results.append(is_rule_satisfied)

    if primary_rule_logical_op == LogicalOperator.AND.name:
        return all(comparison_results)
    elif primary_rule_logical_op == LogicalOperator.OR.name:
        return any(comparison_results)
    return False

def get_primary_rules_info():
    primary_rules = get_all_primary_rules()
    current_rule = None
    for rule in primary_rules:
        are_rules_satisfied = evaluate_conditional_rules(rule)
        start_time = datetime.strptime(rule['startTimeFrom'], '%H:%M:%S').time()
        end_time = datetime.strptime(rule['startTimeTo'], '%H:%M:%S').time()

        if start_time <= CURR_TIME.time() <= end_time and are_rules_satisfied:
            current_rule = rule
            break

    return current_rule
    
def check_error_state(actual_primary_rule, expected_primary_rule):
    primary_rules = get_all_primary_rules()
    rules_same_time = []
    for rule in primary_rules:
        ruleStartTime = rule['startTimeFrom']
        ruleEndTime = rule['startTimeTo']
        if ruleStartTime == expected_primary_rule['startTimeFrom'] and ruleEndTime == expected_primary_rule['startTimeTo']:
            rules_same_time.append(rule['id'])

    if actual_primary_rule['ruleId'] not in rules_same_time:
        log_error_state('The actual state is not the same as the expected state.')


def lambda_handler(event, context):
    expected_primary_rule = get_primary_rules_info()

    actual_primary_rule = get_log_latest()
    
    if actual_primary_rule['ruleId'] != expected_primary_rule['id']:
        check_error_state(actual_primary_rule, expected_primary_rule)
        deploy_plugins(expected_primary_rule['id'])

        log_state(expected_primary_rule['id'], 'The system state was changed.')
        return {
            'statusCode': 200,
            'body': json.dumps({'responseMessage': f'System state changed to {expected_primary_rule["id"]} {expected_primary_rule["name"]} and plugins deployed successfully)'})
        }
    else:
        log_state(expected_primary_rule['id'], 'No state change required.')
        return {
            'statusCode': 200,
            'body': json.dumps({'responseMessage': f'No state change required, current state is id {actual_primary_rule["ruleId"]}'})
        }