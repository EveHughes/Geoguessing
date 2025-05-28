import openai
from pathlib import Path
import base64

#get key
with open('key.txt', 'r') as file:
    my_key = file.read().strip()

#empty images list
images = []
#encodes images to base64 and adds to list
def get_images(number_images):
    for i in range(number_images):
        image_path = Path(__file__).parent / ("images/image" + str(i) + ".jpg")
        with open(image_path, "rb") as image_file:
            images.append(base64.b64encode(image_file.read()).decode('utf-8'))

#empty prompts list
prompts = []
#reads in geoguessr prompts and adds to list
def read_prompts(number_prompts):
    for i in range(number_prompts):
        file_path = Path(__file__).parent / ("prompts/prompt" + str(i) + ".txt")
        with open(file_path, "r", encoding="utf-8") as f:
            rubric_text = f.read()
        prompts.append(rubric_text)
    

#guesses location, prompt varies
def guess(): 
    responses = []
    
    client = openai.OpenAI(api_key = my_key)

    for prompt in prompts:
        response = client.chat.completions.create(
            model="gpt-4o",  
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{images[2]}"
                            }
                        }
                    ]
                }
            ],
            max_tokens = 400
        )
        print(response.choices[0].message.content)
        responses.append(response.choices[0].message.content)
    return responses

if __name__ == "__main__":
    read_prompts(3)
    get_images(6)
    guesses = guess()
