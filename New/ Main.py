import streamlit as st

st.set_page_config(page_title="수암명리 통합분석 시스템", layout="wide")

st.sidebar.title("수암명리 분석 메뉴")
st.markdown("""
# 수암명리 통합 분석 플랫폼  
왼쪽 사이드 메뉴 또는 상단 탭에서 기능을 선택하세요.
""")
st.sidebar.info("연구/실무에 필요한 구조 해석, 명리용어, 연관검색 지원")

# Streamlit pages/ 디렉토리의 *.py 파일이 자동 메뉴에 등록됨.