import sys
import requests
import json
import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector
# Idea from: https://www.youtube.com/watch?v=CluNm3OfyO8&ab_channel=IamYou
# Find the quick actions at ~/Library/Services

# Get the command line arguments
args = sys.argv[1:]

# Convert the arguments to a single string
user_content = " ".join(args)

# Load API key from file
api_key = json.load(open("/Users/Marc/Desktop/Past Affairs/Past Universities/SSE Courses/Master Thesis/llm_key.json"))["llm_key"]

def get_lang_detector(nlp, name):
       return LanguageDetector()

nlp = spacy.load("en_core_web_sm")
Language.factory("language_detector", func=get_lang_detector)
nlp.add_pipe('language_detector', last=True)

def detect_language(text):
    doc = nlp(text)
    return doc._.language["language"]

def get_reponse(prompt):
	response = requests.post(
  	url="https://openrouter.ai/api/v1/chat/completions",
  	headers={
    	  "Authorization": api_key
  	},
  	data=json.dumps({
  	  "model": "mistralai/mistral-7b-instruct",
   	 "messages": [
   	   {"role": "system", "content":        
	"""
	"""},
     	 {"role": "user", "content": prompt}
   	 ]
  	})
	)
	
	# Extract the "content" field from the response
	content = response.json()["choices"][0]["message"]["content"]

	# Process the string
	content = content.replace("<</SYS>>", "").strip()

	return content

# Detect the language of the user input
language = detect_language(user_content)

# Translate the text
if language == "en":
	content = get_reponse("Translate the text '" + user_content + "' to German. Do it strictly in the following format: Translation: <your translation>")
else:
	content = get_reponse("Translate the text '" + user_content + "' to English. Do it strictly in the following format: Translation: <your translation>")

# Process the string
content = content.replace("Translation:", "").replace(user_content, "").replace("German:", "").strip()

if content[0] == "<" and content[-1] == ">":
	content = content[1:len(content)-1]

if content[0] == '"' and content[-1] == '"':
	content = content[1:len(content)-1]

print(content)