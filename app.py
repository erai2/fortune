import os
import json
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT_TEMPLATE = """\
아래 명리/사주 관련 문서에서 각 단락/문단/항목별로

- category(분류),
- term(용어/개념),
- definition(설명),
- example(예시/사례, 있으면),
- keywords(주요 키워드),
- relations(다른 용어나 사례와의 연관성)
을 뽑아, JSON 배열로 구조화해줘.

출력 예시:
[
{
"category": "운기개념",
"term": "대운",
"definition": "10년 단위로 운이 변하는 명리학의 기본 개념...",
"example": "예: 25세~34세 대운에 진로 변화",
"keywords": ["운", "대운", "10년"],
"relations": ["세운", "응기"]
},
...
]

문서:
"""


def extract_terms(text: str):
    prompt = PROMPT_TEMPLATE + f"""\
{text}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    content = response.choices[0].message.content
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        st.error("OpenAI가 유효한 JSON을 반환하지 않았습니다.")
        return []


def main():
    st.title("명리/사주 문서 자동 구조화")
    uploaded_file = st.file_uploader("텍스트 파일 업로드", type=["txt"])
    input_text = st.text_area("또는 직접 텍스트 입력", height=200)

    text = ""
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
    elif input_text.strip():
        text = input_text

    if st.button("추출 실행"):
        if not text:
            st.warning("텍스트를 입력하세요.")
        else:
            results = extract_terms(text)
            st.json(results)
            if results:
                st.download_button(
                    "JSON 다운로드",
                    data=json.dumps(results, ensure_ascii=False, indent=2),
                    file_name="terms.json",
                    mime="application/json",
                )


if __name__ == "__main__":
    main()
