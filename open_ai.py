import base64
import requests

# OpenAI API Key
api_key = "YOUR API KEY"

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "test.jpeg"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}
prompt = '''
You are a computer programmer who is tasked with writing code to control a robot on the moon.

You are given a set of inputs, as follows:

Environment state information:
    Temperature - float --> normal range of values are between -20 degrees celsius and 50 degrees celsius
    Luminosity - float -->  normal range of values are between 0.3 and up to 1 
    Vibration - float --> normal range of values are between 0.1 IPS and up to 0.5 IPS 

You have to make a decision whether it is safe to proceed or not. Your answer should only be in binary, meaning yes or no. If you respond with anything else the program will crush
Based on the image provided along with the following important values of vibration levels 2.5 IPS, lumnoisty of 0.5 and temperature 50 degrees celsiius. Is it safe to proceed?
'''

payload = {
  "model": "gpt-4-vision-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": prompt
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  "max_tokens": 200
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json())

