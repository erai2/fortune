import streamlit as st
import pandas as pd
from modules.suam_analysis import load_analysis, save_analysis, llm_auto_analysis

st.set_page_config(page_title="수암명리 통합분석 시스템", layout="wide")

st.sidebar.title("수암명리 분석 메뉴")
st.sidebar.info("연구/실무에 필요한 구조 해석, 명리용어, 연관검색 지원")

st.title("🌀 수암명리 구조 해석 시스템 (자동/수동 입력, 연관 자료 통합)")

suam_data = load_analysis()

# --- Tabs for input/auto analysis and search/edit ---
tab1, tab2 = st.tabs(["구조 해석 입력/자동분석", "검색/수정/통합검색"])

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

    table_summary = st.text_area("1. 구조 표 요약", height=60, key="f1")
    tiangan_analysis = st.text_area("2. 천간 분석", height=80, key="f2")
    dizhi_analysis = st.text_area("3. 지지 분석", height=80, key="f3")
    hapchung_analysis = st.text_area("4. 합/충/형/파 분석", height=80, key="f4")
    reality_application = st.text_area("5. 현실 응용/해석", height=100, key="f5")
    prompt_field = st.text_area("프롬프트(질문 내용)", height=100, key="f6")

    if auto_gen and api_key and tiangan and dizhi and topic:
        with st.spinner("LLM 구조 해석 중..."):
            fields, prompt_used = llm_auto_analysis(api_key, tiangan, dizhi, topic)
            st.session_state.f1, st.session_state.f2, st.session_state.f3, st.session_state.f4, st.session_state.f5 = fields
            st.session_state.f6 = prompt_used
            st.success("자동 구조 해석이 완료되었습니다. 내용 수정 후 저장 가능!")

    if st.button("💾 구조 해석 저장"):
        entry = {
            "명식_천간": tiangan,
            "명식_지지": dizhi,
            "주제": topic,
            "구조_표": st.session_state.get("f1", ""),
            "천간_분석": st.session_state.get("f2", ""),
            "지지_분석": st.session_state.get("f3", ""),
            "합충_분석": st.session_state.get("f4", ""),
            "현실_응용": st.session_state.get("f5", ""),
            "프롬프트": st.session_state.get("f6", ""),
        }
        edit_idx = st.session_state.get("edit_idx")
        if edit_idx is not None:
            suam_data[edit_idx] = entry
            st.session_state.edit_idx = None
            st.success("기존 구조 해석이 수정되었습니다.")
        else:
            suam_data.append(entry)
            st.success("구조 해석이 저장되었습니다.")
        save_analysis(suam_data)

with tab2:
    st.subheader("구조 해석 데이터 검색/수정/통합")
    keyword = st.text_input("키워드 검색 (명식, 주제, 분석 등)", key="search1")
    field_sel = st.selectbox("검색 필드", ["전체", "명식_천간", "명식_지지", "주제", "천간_분석", "지지_분석", "합충_분석", "현실_응용"])
    search_btn = st.button("🔍 검색")

    if search_btn:
        results = []
        for idx, item in enumerate(suam_data):
            target_text = " ".join(map(str, item.values())) if field_sel == "전체" else item.get(field_sel, "")
            if keyword and keyword in target_text:
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
                if st.button("이 해석 불러와 편집", key=f"edit_{idx}"):
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

    st.markdown("---\n#### 전체 구조 해석 데이터")
    df = pd.DataFrame(suam_data)
    if not df.empty:
        st.dataframe(df)

st.caption("데이터는 JSON 파일로 저장/불러오기됩니다. LLM 자동 해석, 입력 세분화, 연관자료, 수정/재저장까지 통합 지원.")
