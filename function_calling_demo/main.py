import os
import json
import openai
from datetime import datetime, timedelta

from secret_key import openai_key
openai.api_key= openai_key

# ----------------------------------------------------------------------------------------------------------------------------
# Create tools which includes a function for fetching source and destination from the prompt 
# ----------------------------------------------------------------------------------------------------------------------------

tools = [
    {
        "type": "function",
        "function":  {
        "name": "get_flight_info",
        "description":"Get flight information between source and destination",
        "parameters":{
            "type":"object",
            "properties": {
                "loc_origin": {
                    "type": "string",
                    "description": "The departure airport, e.g. DUS",
                },
                "loc_destination": {
                    "type": "string",
                    "description": "The destination airport, e.g. HAM",
                },
            },
            "required": ["loc_origin", "loc_destination"],
            "additionalProperties": False,
        },        
    }
    }
]

# ----------------------------------------------------------------------------------------------------------------------------
# Prompt
# ----------------------------------------------------------------------------------------------------------------------------

user_prompt = "What time is the next flight between surat and bengaluru?"

# ----------------------------------------------------------------------------------------------------------------------------
# open_api call to fetch the source,destination 
# ----------------------------------------------------------------------------------------------------------------------------

completion = openai.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
        {
            "role": "user",
            "content": user_prompt,
        },
        {"role": "system", "content": "You are a helpful customer support assistant. Use the supplied tools to assist the user."},
    ],
    tools= tools,
)

params=  json.loads(completion.choices[0].message.tool_calls[0].function.arguments)

# ----------------------------------------------------------------------------------------------------------------------------
# Function defined to get the structured output of the flight details 
# ----------------------------------------------------------------------------------------------------------------------------

def get_flight_info(loc_origin, loc_destination):
    """Get flight information between two locations."""
    # Example output returned from an API or database
    flight_info = {
        "loc_origin": loc_origin,
        "loc_destination": loc_destination,
        "datetime": str(datetime.now() + timedelta(hours=2)),
        "airline": "KLM",
        "flight": "KL643",
    }

    return json.dumps(flight_info)


loc_origin= params['loc_origin']
loc_destination= params['loc_destination']

chosen_function= eval(completion.choices[0].message.tool_calls[0].function.name)
flight_details =  chosen_function(**params)
print(flight_details)


# --------------------------------------------------------------
# Add function result to the prompt for a final answer
# --------------------------------------------------------------

# The key is to add the function output back to the messages with role: function
second_completion= openai.chat.completions.create(
    model = "gpt-3.5-turbo-0125",
    messages =[
        {
            "role":"user", "content":user_prompt,
        },
        {"role": "function", "name": completion.choices[0].message.tool_calls[0].function.name, "content": flight_details},

    ],
)

response= second_completion.choices[0].message.content
print(response)

if __name__=="__main__":
    pass