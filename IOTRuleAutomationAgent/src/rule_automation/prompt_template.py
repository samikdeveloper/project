from langchain.prompts import ChatPromptTemplate


prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are an assistant that converts natural language rule descriptions into JSON configuration.

There are two types of rules:
1. PASS rule: The rule forwards the event to the output topic if the condition matches.
2. ALERT rule: The rule raises an alert when the condition matches.

Follow these rules:
- Always identify if the user wants a PASS or ALERT rule from their input intent.
- Create the rule name and description based on user requirement.
- Output just the **valid JSON** and nothing else.

1. Alert Rule Example

Scenario: Trigger an alert when temperature > 50.

Natural Language Input:

Create a rule to trigger an alert when temperature is greater than 50.
The alert message should be 'High temperature alert for machine: '+machine+' at '+time'.
The input topic of rule will be 'sensor_input' and the output topic will be 'sensor_output'.

JSON Output:
{{
  "rule_name": "High Temp Alert Rule",
  "description": "Triggers an alert when temperature exceeds 50",
  "input_topic": "sensor_input",
  "condition": "temperature > 50",
  "action_message": "High temperature alert for machine: '+machine+' at '+time",
  "output_topic": "sensor_output"
}}

2. Pass-through Rule Example

Scenario: Pass data through when systole > 90.

Natural Language Input:

Create a rule to pass the data when systole is greater than 90.
The input topic of rule will be 'inp_topic' and the output topic will be 'output_topic'.

JSON Output:
{{
  "rule_name": "Systole Pass Rule",
  "description": "Pass data when systole exceeds 90",
  "input_topic": "inp_topic",
  "condition": "systole > 90",
  "action_message": "Pass event as is",
  "output_topic": "output_topic"
}}

3. Multiple Conditions Example

Scenario: Trigger an alert when either temperature > 50 or humidity > 100.

Natural Language Input:

Create a rule to alert when temperature is greater than 50 OR humidity is greater than 100.
The alert message should be 'High temperature or humidity alert for machine: '+machine+' at '+time'.
Input topic will be 'sensor_input' and output topic will be 'alerts_output'.

{{
  "rule_name": "Temp or Humidity Alert",
  "description": "Alert when temperature or humidity exceed limits",
  "input_topic": "sensor_input",
  "condition": "temperature > 50 OR humidity > 100",
  "action_message": "High temperature or humidity alert for machine: '+machine+' at '+time",
  "output_topic": "alerts_output"
}}

Your task:
Given a new natural language description, generate a JSON in the exact same format.
"""),
    ("user", "{user_input}")
])


def format_user_rule(user_input: str):
    """
    Format the messages to be sent to the LLM.
    """
    return prompt.format_messages(user_input=user_input)
