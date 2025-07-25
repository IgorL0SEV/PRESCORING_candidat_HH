import streamlit as st
import openai
from parse_hh import get_html, extract_vacancy_data, extract_resume_data

# Инициализация OpenAI-клиента
client = openai.OpenAI(api_key="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") 


SYSTEM_PROMPT = """
Проскорь кандидата, насколько он подходит для данной вакансии.
Сначала напиши короткий анализ, который будет пояснять оценку.
Отдельно оцени качество заполнения резюме (понятно ли, с какими задачами сталкивался кандидат и каким образом их решал?). Эта оценка должна учитываться при выставлении финальной оценки - нам важно нанимать таких кандидатов, которые могут рассказать про свою работу
Потом представь результат в виде оценки от 1 до 10.
""".strip()

def request_gpt(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1000,
        temperature=0,
    )
    return response.choices[0].message.content

# UI
st.title('CV Scoring App')
job_url = st.text_area('Введите ссылку на вакансию')
resume_url = st.text_area('Введите ссылку на резюме')

if st.button("Проанализировать соответствие"):
    with st.spinner("Парсим данные и отправляем в GPT..."):
        try:
            job_html = get_html(job_url).text
            resume_html = get_html(resume_url).text
            job_text = extract_vacancy_data(job_html)
            resume_text = extract_resume_data(resume_html)
            prompt = f"# ВАКАНСИЯ\n{job_text}\n\n# РЕЗЮМЕ\n{resume_text}"
            response = request_gpt(SYSTEM_PROMPT, prompt)
            st.subheader("📊 Результат анализа:")
            st.markdown(response)
        except Exception as e:
            st.error(f"Произошла ошибка: {e}")
