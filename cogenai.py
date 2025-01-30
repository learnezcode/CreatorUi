import yaml
from g4f.client import Client
import time

# Initialize the g4f client
client = Client()

def transform_to_g4f(messages_chatgpt):
    """
    Transforms messages into a format compatible with g4f.
    """
    messages_g4f = []
    for message in messages_chatgpt:
        if message['role'] == 'system':
            messages_g4f.append({"role": "system", "content": message['content']})
        elif message['role'] == 'user':
            messages_g4f.append({'role': 'user', 'content': message['content']})
        elif message['role'] == 'assistant':
            messages_g4f.append({'role': 'assistant', 'content': message['content']})
    return messages_g4f

def translator(text, lang):
    """
    Translates text into the specified language using g4f.
    """
    while True:
        try:
            messages = [
                {"role": "system", "content": f"Act as a translator to {lang} language. Translate full sentences only. Do not translate programming language names."},
                {"role": "user", "content": f"Translate this: {text}"}
            ]
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=transform_to_g4f(messages),
                web_search=False
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error during translation: {e}. Waiting for 1 minute...")
            time.sleep(60)

def generate_language(course_path, lang):
    with open(course_path, 'r') as file:
        doc = file.read().replace('\n', '\n')
    info = yaml.load(doc, Loader=yaml.Loader)
    
    name_t = translator(info['name'], lang.capitalize())
    desc_t = translator(info['description'], lang.capitalize())
    print(f'Generating course\nName: {name_t}\nDescription: {desc_t}')
    
    course = {'name': name_t, 'desc': desc_t, 'lang': lang, 'content': []}
    message_list = [
        {"role": "system", "content": "You're an AI Programming teacher ezcode. You need to write text for a course with chapters. User gives you chapter name and instructions for this chapter. Always write all variables in English. NEVER USE HEADING MARKDOWN, instead make text bold without heading markdown."},
        {"role": "user", "content": f"Course: {course['name']}. Description: {course['desc']}. Chapter name: {info['course'][0]['chapter-name']}\nInstructions: {info['course'][0]['info']}. Write it in {lang.capitalize()}. NEVER USE HEADING MARKDOWN, instead make text bold without heading markdown."}
    ]
    
    print(f'Generating {lang.upper()}')
    for i in range(len(info['course'])):
        if i == 0:
            response_app = get_response(message_list)
        else:
            message_list.append({"role": "user", "content": f"Chapter name: {info['course'][i]['chapter-name']}\nInstructions: {info['course'][i]['info']}. Write it in {lang.capitalize()} language. NEVER USE HEADING MARKDOWN, instead make text bold without heading markdown."})
            response_app = get_response(message_list)
        
        course['content'].append({"chapter": i+1, "chapter-name": info['course'][i]['chapter-name'], "text": response_app})
        message_list.append({'role': 'assistant', 'content': response_app})
    
    return course

def get_response(message_list):
    """
    Sends messages to g4f and retrieves the response.
    """
    while True:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=transform_to_g4f(message_list),
                web_search=False
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error during content generation: {e}. Waiting for 1 minute...")
            time.sleep(60)

def generate_course(file, languages=['en', 'ru', 'by']):
    """
    Generates the course in multiple languages.
    """
    courses = {}
    for lang in languages:
        courses[lang] = generate_language(file, lang)
    return courses

# Example usage:
# result = generate_course('course.yaml')
# print(result)