import streamlit as st
import yaml
import io

# Translations dictionary
translations = {
    'ru': {
        'title': "Создание курса!",
        'send_file': "Отправьте файл сюда",
        'course_title': "Введите название курса:",
        'course_description': "Введите описание курса:",
        'num_topics': "Введите количество тем:",
        'topic': "Тема",
        'chapter_name': "Название главы для темы",
        'info': "Информация для темы",
        'generate_yaml': "Сгенерировать YAML",
        'generated_yaml': "Сгенерированный YAML:",
        'download_yaml': "Скачать YAML",
        'error': "Пожалуйста, заполните все поля перед генерацией YAML."
    },
    'be': {
        'title': "Стварэнне курса!",
        'send_file': "Адпраўце файл сюды",
        'course_title': "Увядзіце назву курса:",
        'course_description': "Увядзіце апісанне курса:",
        'num_topics': "Увядзіце колькасць тэм:",
        'topic': "Тэма",
        'chapter_name': "Назва главы для тэмы",
        'info': "Інфармацыя для тэмы",
        'generate_yaml': "Сгенераваць YAML",
        'generated_yaml': "Сгенераваны YAML:",
        'download_yaml': "Спампаваць YAML",
        'error': "Калі ласка, запоўніце ўсе палі перад генерацыяй YAML."
    },
    'en': {
        'title': "Course Creation!",
        'send_file': "Send file here",
        'course_title': "Enter the name of the course:",
        'course_description': "Enter the description of the course:",
        'num_topics': "Enter the number of topics:",
        'topic': "Topic",
        'chapter_name': "Chapter name for topic",
        'info': "Info for topic",
        'generate_yaml': "Generate YAML",
        'generated_yaml': "Generated YAML:",
        'download_yaml': "Download YAML",
        'error': "Please fill in all fields before generating YAML."
    }
}

# Language selector with flags
language_options = {
    'ru': '🇷🇺 Russian',
    'be': '🇧🇾 Belarusian',
    'en': '🇬🇧 English'
}
language = st.selectbox("Select Language", options=list(language_options.keys()), format_func=lambda x: language_options[x])

# Suggestion to use English
st.caption("📝 Please use English for the best results.")

# Function to create the YAML structure
def create_yaml(course_title, course_description, topics):
    course_data = {
        'name': course_title,
        'description': course_description,
        'course': {}
    }
    
    for i, topic in enumerate(topics, start=1):
        chapter_name = topic['chapter_name']
        info = topic['info']
        course_data['course'][i] = {
            'chapter-name': chapter_name,
            'info': info
        }
    
    return yaml.dump(course_data, sort_keys=False)

# Streamlit UI
st.title(translations[language]['title'])

# Add a hyperlink to the Telegram bot
telegram_link = "https://t.me/contactlabsbot"
st.markdown(f"[{translations[language]['send_file']}]({telegram_link})", unsafe_allow_html=True)

# Input for course title
course_title = st.text_input(translations[language]['course_title'])

# Input for course description
course_description = st.text_area(translations[language]['course_description'])

# Input for number of topics
num_topics = st.number_input(translations[language]['num_topics'], min_value=1, step=1)

# List to hold topic details
topics = []

# Input fields for each topic
for i in range(num_topics):
    st.subheader(f"{translations[language]['topic']} {i + 1}")
    chapter_name = st.text_input(f"{translations[language]['chapter_name']} {i + 1}:")
    info = st.text_area(f"{translations[language]['info']} {i + 1}:")
    
    if chapter_name and info:
        topics.append({'chapter_name': chapter_name, 'info': info})

# Button to generate YAML
if st.button(translations[language]['generate_yaml']):
    if course_title and course_description and topics:
        yaml_output = create_yaml(course_title, course_description, topics)
        st.subheader(translations[language]['generated_yaml'])
        st.code(yaml_output, language='yaml')
        
        # Create a download button for the YAML file
        yaml_bytes = io.BytesIO(yaml_output.encode('utf-8'))
        st.download_button(
            label=translations[language]['download_yaml'],
            data=yaml_bytes,
            file_name=f"{course_title.replace(' ', '_')}.yaml",
            mime="text/yaml"
        )
        
    else:
        st.error(translations[language]['error'])