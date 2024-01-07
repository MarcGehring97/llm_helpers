import sys
import requests
import json
# Idea from: https://www.youtube.com/watch?v=CluNm3OfyO8&ab_channel=IamYou
# Find the quick actions at ~/Library/Services

# Get the command line arguments
args = sys.argv[1:]

# Convert the arguments to a single string
user_content = ' '.join(args)

# Load API key from file
# The API key has the format "Bearer sk-or-..."
api_key = "<your API key>"

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
      "Authorization": api_key
  },
  data=json.dumps({
    "model": "mistralai/mistral-7b-instruct",
    "messages": [{
      "role": "system", "content": """
        Rephrase the following sentences to be more reader-friendly and engaging in the same language as the user content. Do not preface your response with Response, provide the improved sentence directly.
        
        Examples:
        User content: "I have a test tomorrow, so I needs to study all night. I'm so tired."
        Response: "I have a test tomorrow, so I need to study all night. I'm so tired."
        
        User content: "He don't like to eat vegetables. Vegetables are healthy and provide essential nutrients."
        Response: "He doesn't like to eat vegetables. Vegetables are healthy and provide essential nutrients."
        
        User content:
      """
    }, {"role": "user", "content": user_content}]
  })
)

# Extract the 'content' field from the response
content = response.json()["choices"][0]["message"]["content"]
print(content)
