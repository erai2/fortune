import streamlit as st
import pandas as pd
import os
import json
from pathlib import Path

from langchain_openai import ChatOpenAI

# ---------- [1] 파일 경로 및 데이터 관리 ----------
DB_PATH = './suam_analysis.json'

# 기존 데이터 로딩 (없으면 빈 리스트)
def load_suam_data():
    if os.path.exists(DB_PATH):
        with open(DB_PATH, encoding='utf-8') as f:
            return json.load(f)
    return []

def save_suam_data(data):
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

suam_data = load_suam_data()

# 연관 이론/용어/사례 샘플 DB
basic_theory = [
    {"Category": "합충", "Concept": "천간합", "Detail": "갑기합토, 을경합금 등"},
    {"Category": "십신", "Concept": "재성", "Detail": "재물의 실제성/허상 판단 기준"}
]
terminology = [
    {"Term": "합", "Meaning": "서로 다른 오행/간지의 결합", "Category": "합충"},
    {"Term": "충", "Meaning": "상대적 파괴/긴장", "Category": "합충"}
]
case_studies = [
    {"Birth Info": "甲乙辛癸 / 寅卯酉丑", "Chart": "甲乙辛癸寅卯酉丑", "Analysis": "재물 실제 작동/허상 해석", "Result": "실제 작동 약함"}
]

# ---------- [2] LLM 자동 구조 해석 함수 ----------
def suam_prompt_builder(tiangan, dizhi, topic):
    # 구조적 관점 프롬프트 자동 생성
    prompt = (
        "[수암명리 구조 해석] "
        "아래 명식을 구조적 관점(글자 간 실제 연결/작용력, 허상 여부 등)으로 해석해줘. "
        "십신 설명은 최소화하고, 일간 중심의 생극, 합, 충, 회, 실제 현실에서 작동할 수 있는 연결만 구체적으로 분석해줘. "
        f"특히 ‘{topic}’이 실제 현실에 작동하는지, 허상인지, 이유까지 분석해줘. "
        "결과는 다음 형식으로:\n"
        "1. 구조 표 요약 (간략 표)\n"
        "2. 천간 분석\n"
        "3. 지지 분석\n"
        "4. 합/충/형/파 분석\n"
        "5. 현실 응용/해석\n"
        "\n예시 명식:\n천간: " + tiangan + "\n지지: " + dizhi
    )
    return prompt

def suam_llm_analyze(api_key, tiangan, dizhi, topic):
    """
    OpenAI LLM에 프롬프트를 보내고, 응답을 5개 필드로 분할 반환
    """
    prompt = suam_prompt_builder(tiangan, dizhi, topic)
    llm = ChatOpenAI(openai_api_key=api_key, temperature=0.2, model="gpt-3.5-turbo")
    response = llm.invoke(prompt)
    text = response.content

    # 대략적으로 1-5로 분리(실무에선 좀 더 robust하게 파싱 가능)
    import re
    parts = re.split(r'\n?[\d\.]+[\)\.] ', text)
    if len(parts) < 6:
        # 실패시 그냥 순서대로 채움
        table, tiangan_desc, dizhi_desc, hapchung_desc, reality = [""]*5
    else:
        _, table, tiangan_desc, dizhi_desc, hapchung_desc, reality = parts[:6]
    return table.strip(), tiangan_desc.strip(), dizhi_desc.strip(), hapchung_desc.strip(), reality.strip(), prompt

# ---------- [3] Streamlit UI/기능 구현 ----------
st.set_page_config(page_title="수암명리 구조 해석 DB", layout="wide")
st.title("🌀 수암명리 구조 해석 시스템 (자동/수동 입력, 연관 자료 통합)")

tab1, tab2 = st.tabs(["구조 해석 입력/자동분석", "검색/수정/통합검색"])

# --- 구조 해석 입력/자동분석 ---
with tab1:
    st.subheader("수암명리 구조 해석 입력 및 LLM 자동 생성")

    col1, col2 = st.columns([2,1])
    with col1:
        tiangan = st.text_input("천간 (예: 壬 甲 辛 戊)", key="in1")
        dizhi = st.text_input("지지 (예: 子 午 酉 申)", key="in2")
        topic = st.text_input("주제/관점 (예: 재물의 현실 작동력)", value="재물의 현실 작동력", key="in3")
        api_key = st.text_input("OpenAI API Key (자동 해석용)", type="password")
    with col2:
        auto_gen = st.button("🔵 LLM 자동 구조 해석")

    # 세부 구조 필드
    table_summary = st.text_area("1. 구조 표 요약", height=60, key="f1")
    tiangan_analysis = st.text_area("2. 천간 분석", height=80, key="f2")
    dizhi_analysis = st.text_area("3. 지지 분석", height=80, key="f3")
    hapchung_analysis = st.text_area("4. 합/충/형/파 분석", height=80, key="f4")
    reality_application = st.text_area("5. 현실 응용/해석", height=100, key="f5")
    prompt_field = st.text_area("프롬프트(질문 내용)", height=100, key="f6")

    # 자동 생성 클릭 시 LLM 분석 → 필드 채움
    if auto_gen and api_key and tiangan and dizhi and topic:
        with st.spinner("LLM 구조 해석 중..."):
            t, tian, di, hap, real, prompt_used = suam_llm_analyze(api_key, tiangan, dizhi, topic)
            st.session_state.f1 = t
            st.session_state.f2 = tian
            st.session_state.f3 = di
            st.session_state.f4 = hap
            st.session_state.f5 = real
            st.session_state.f6 = prompt_used
            st.success("자동 구조 해석이 완료되었습니다. 내용 수정 후 저장 가능!")

    # 저장 (수정/신규 통합)
    edit_idx = st.session_state.get("edit_idx", None)
    if st.button("💾 구조 해석 저장"):
        entry = {
            "명식_천간": tiangan, "명식_지지": dizhi, "주제": topic,
            "구조_표": st.session_state.f1,
            "천간_분석": st.session_state.f2,
            "지지_분석": st.session_state.f3,
            "합충_분석": st.session_state.f4,
            "현실_응용": st.session_state.f5,
            "프롬프트": st.session_state.f6
        }
        if edit_idx is not None:
            suam_data[edit_idx] = entry
            st.session_state.edit_idx = None
            st.success("기존 구조 해석이 수정되었습니다.")
        else:
            suam_data.append(entry)
            st.success("구조 해석이 저장되었습니다.")
        save_suam_data(suam_data)

# --- 검색/수정/통합검색 ---
with tab2:
    st.subheader("구조 해석 데이터 검색/수정/통합")
    # 세부 필터
    keyword = st.text_input("키워드 검색 (명식, 주제, 분석 등)", key="search1")
    field_sel = st.selectbox("검색 필드", ["전체", "명식_천간", "명식_지지", "주제", "천간_분석", "지지_분석", "합충_분석", "현실_응용"])
    search_btn = st.button("🔍 검색")
    edit_idx = st.session_state.get("edit_idx", None)

    # 검색 실행
    if search_btn:
        results = []
        for idx, item in enumerate(suam_data):
            # 필드 선택별 검색
            target_text = ""
            if field_sel == "전체":
                target_text = " ".join([str(v) for v in item.values()])
            else:
                target_text = item.get(field_sel, "")
            if keyword in target_text:
                results.append((idx, item))
        if results:
            st.info(f"{len(results)}건 검색됨 (클릭시 편집)")
            for idx, item in results:
                st.markdown(f"---\n#### {idx+1}. [명식: {item['명식_천간']} / {item['명식_지지']}] | {item['주제']}")
                st.markdown(f"- **[1. 구조표]**\n{item['구조_표']}")
                st.markdown(f"- **[2. 천간]**\n{item['천간_분석']}")
                st.markdown(f"- **[3. 지지]**\n{item['지지_분석']}")
                st.markdown(f"- **[4. 합충]**\n{item['합충_분석']}")
                st.markdown(f"- **[5. 현실응용]**\n{item['현실_응용']}")
                st.markdown(f"**[프롬프트]**\n{item['프롬프트']}")
                if st.button("이 해석 불러와 편집", key=f"edit_{idx}"):
                    # 해당 데이터로 입력폼 세팅
                    st.session_state.in1 = item["명식_천간"]
                    st.session_state.in2 = item["명식_지지"]
                    st.session_state.in3 = item["주제"]
                    st.session_state.f1 = item["구조_표"]
                    st.session_state.f2 = item["천간_분석"]
                    st.session_state.f3 = item["지지_분석"]
                    st.session_state.f4 = item["합충_분석"]
                    st.session_state.f5 = item["현실_응용"]
                    st.session_state.f6 = item["프롬프트"]
                    st.session_state.edit_idx = idx
                    st.success("입력 폼에 데이터가 불러와졌습니다. (상단 탭에서 수정/저장)")
        else:
            st.info("검색 결과가 없습니다.")

    # 전체 데이터 표로 보기
    st.markdown("---\n#### 전체 구조 해석 데이터")
    df = pd.DataFrame(suam_data)
    if not df.empty:
        st.dataframe(df)

    # 연관 자료 통합 표출
    st.markdown("---\n### 연관 이론/용어/사례 자동 연결")
    if search_btn and results:
        st.markdown("#### 연관 이론/용어/사례")
        # 예시: 주제, 분석 키워드로 관련 이론/용어/사례 자동 매칭(간단하게 포함 단어 검색)
        rel_keywords = set()
        for idx, item in results:
            rel_keywords |= set(item["주제"].split())
            rel_keywords |= set(item["합충_분석"].split())
            rel_keywords |= set(item["천간_분석"].split())
            rel_keywords |= set(item["지지_분석"].split())
        theory_hits = [x for x in basic_theory if any(k in x["Concept"] or k in x["Category"] or k in x["Detail"] for k in rel_keywords)]
        term_hits = [x for x in terminology if any(k in x["Term"] or k in x["Meaning"] for k in rel_keywords)]
        case_hits = [x for x in case_studies if any(k in x["Analysis"] or k in x["Result"] for k in rel_keywords)]
        if theory_hits:
            st.markdown("**[연관 이론]**")
            st.dataframe(pd.DataFrame(theory_hits))
        if term_hits:
            st.markdown("**[연관 용어]**")
            st.dataframe(pd.DataFrame(term_hits))
        if case_hits:
            st.markdown("**[연관 사례]**")
            st.dataframe(pd.DataFrame(case_hits))
        if not (theory_hits or term_hits or case_hits):
            st.info("연관 자료가 없습니다.")

st.caption("데이터는 JSON 파일로 저장/불러오기됩니다. LLM 자동 해석, 입력 세분화, 연관자료, 수정/재저장까지 통합 지원.")