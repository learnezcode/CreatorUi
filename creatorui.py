import streamlit as st
import yaml
import io
import os
from cogenai import generate_course

# Translations dictionary
translations = {
    'ru': {
        'title': "Создание курса!",
        'en_tab': 'Английская версия',
        'ru_tab': 'Русская версия',
        'by_tab': 'Белорусская версия',
        'download_course': 'Скачать курс',
        'send_file': "Отправьте файл сюда",
        'course_title': "Введите название курса:",
        'course_description': "Введите описание курса:",
        'num_topics': "Введите количество тем:",
        'topic': "Тема",
        'chapter_name': "Название главы для темы",
        'info': "Информация для темы",
        'generate_yaml': "Сгенерировать YAML",
        'generate_courses': "Сгенерировать курсы",
        'generated_yaml': "Сгенерированный YAML:",
        'download_yaml': "Скачать YAML",
        'error': "Пожалуйста, заполните все поля перед генерацией YAML.",
        'courses_generated': "Курсы успешно сгенерированы!"
    },
    'be': {
        'title': "Стварэнне курса!",
        'en_tab': 'Англійская версія',
        'ru_tab': 'Руская версія',
        'by_tab': 'Беларуская версія',
        'download_course': 'Спампаваць курс',
        'send_file': "Адпраўце файл сюды",
        'course_title': "Увядзіце назву курса:",
        'course_description': "Увядзіце апісанне курса:",
        'num_topics': "Увядзіце колькасць тэм:",
        'topic': "Тэма",
        'chapter_name': "Назва главы для тэмы",
        'info': "Інфармацыя для тэмы",
        'generate_yaml': "Сгенераваць YAML",
        'generate_courses': "Сгенераваць курсы",
        'generated_yaml': "Сгенераваны YAML:",
        'download_yaml': "Спампаваць YAML",
        'error': "Калі ласка, запоўніце ўсе палі перад генерацыяй YAML.",
        'courses_generated': "Курсы паспяхова створаны!"
    },
    'en': {
        'title': "Course Creation!",
        'en_tab': 'English Version',
        'ru_tab': 'Russian Version',
        'by_tab': 'Belarusian Version',
        'download_course': 'Download Course',
        'send_file': "Send file here",
        'course_title': "Enter the name of the course:",
        'course_description': "Enter the description of the course:",
        'num_topics': "Enter the number of topics:",
        'topic': "Topic",
        'chapter_name': "Chapter name for topic",
        'info': "Info for topic",
        'generate_yaml': "Generate YAML",
        'generate_courses': "Generate Courses",
        'generated_yaml': "Generated YAML:",
        'download_yaml': "Download YAML",
        'error': "Please fill in all fields before generating YAML.",
        'courses_generated': "Courses successfully generated!"
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
        'course': []
    }
    for topic in topics:
        course_data['course'].append({
            'chapter-name': topic['chapter_name'],
            'info': topic['info']
        })
    return yaml.dump(course_data, sort_keys=False, allow_unicode=True)

def save_course_to_yaml(course, lang, output_dir="output"):
    import os
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"course_{lang}.yaml")
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(course, file, allow_unicode=True, sort_keys=False)
    print(f"Course saved to {file_path}")

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

# Buttons row
col1, col2 = st.columns(2)  # Create two columns for buttons

with col1:
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

with col2:
    if st.button(translations[language]['generate_courses']):
        if course_title and course_description and topics:
            yaml_output = create_yaml(course_title, course_description, topics)
            temp_file = "temp_course.yaml"
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(yaml_output)
            
            try:
                courses = generate_course(temp_file)
                # Create tabs for different languages
                tabs = st.tabs([translations[language]['en_tab'], 
                              translations[language]['ru_tab'], 
                              translations[language]['by_tab']])
                
                for i, lang in enumerate(['en', 'ru', 'by']):
                    with tabs[i]:
                        if lang in courses:
                            # Display course content
                            st.code(courses[lang], language='yaml')
                            
                            # Create download button for this language
                            st.download_button(
                                label=translations[language]['download_course'],
                                data=courses[lang],
                                file_name=f"course_{lang}.yaml",
                                mime="text/yaml",
                                key=f"download_{lang}"
                            )
                        else:
                            st.error(translations[language]['error_generation'] + lang.upper())
                
                st.success(translations[language]['courses_generated'])
                
            except Exception as e:
                st.error(f"Generation failed: {str(e)}")
        else:
            st.error(translations[language]['error'])