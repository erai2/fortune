import streamlit as st
import os
import shutil
from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
import pandas as pd

# --- 기본 설정 ---
st.set_page_config(page_title="통합 문서 분석 시스템", layout="wide")
st.title("🧩 통합 문서 분석 및 RAG 시스템")

# 업로드 폴더 설정 (정리 가이드에 따라 단순 경로)
UPLOAD_DIR = "./uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- 문서 로드 함수 ---
@st.cache_data
def load_documents(directory_or_file):
    """PDF, Word, 텍스트 파일에서 문서 추출"""
    docs = []
    if os.path.isdir(directory_or_file):
        files = os.listdir(directory_or_file)
        for filename in files:
            path = os.path.join(directory_or_file, filename)
            docs.extend(load_documents(path))
        return docs
    else:
        filename = os.path.basename(directory_or_file)
        try:
            if filename.endswith(".pdf"):
                loader = PyPDFLoader(directory_or_file)
            elif filename.endswith((".docx", ".doc")):
                loader = UnstructuredWordDocumentLoader(directory_or_file)
            elif filename.endswith(".txt"):
                loader = TextLoader(directory_or_file, encoding="utf-8")
            else:
                return []
            return loader.load()
        except Exception as e:
            st.warning(f"[{filename}] 문서 로딩 실패: {e}")
            return []

# --- RAG 체인 빌드 함수 ---
@st.cache_resource
def build_rag_chain(_docs, openai_api_key):
    """문서 임베딩 및 벡터스토어 구축, LLM 체인 생성"""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(_docs)

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)

    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(temperature=0, openai_api_key=openai_api_key),
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return qa_chain

# --- 문서 요약 함수 ---
@st.cache_data
def summarize_text(text, openai_api_key, model="gpt-3.5-turbo"):
    """LLM을 활용한 문서 요약"""
    client = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model_name=model)
    prompt = f"다음 텍스트를 한국어로 명확하게 요약:\n\n{text[:4000]}"
    summary = client.invoke(prompt)
    return summary.content

# --- 군집화 함수 ---
@st.cache_data
def cluster_documents(docs_for_cluster):
    """문서 내용 임베딩 및 KMeans 군집화"""
    if not docs_for_cluster or len(docs_for_cluster) < 2:
        return None
    texts = [d['text'] for d in docs_for_cluster]
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts)
    num_clusters = min(len(docs_for_cluster), 4)
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init='auto').fit(embeddings)
    result_df = pd.DataFrame({
        "파일명": [d['filename'] for d in docs_for_cluster],
        "그룹 번호": kmeans.labels_
    })
    return result_df.sort_values(by="그룹 번호").reset_index(drop=True)

# --- UI: 사이드바 파일 관리 ---
with st.sidebar:
    st.header("⚙️ 설정")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    st.header("📂 문서 관리")
    uploaded_file = st.file_uploader("문서 업로드", type=["pdf", "docx", "doc", "txt"])
    if uploaded_file:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"'{uploaded_file.name}' 업로드 완료!")
        st.rerun()

    files = [f for f in os.listdir(UPLOAD_DIR) if os.path.isfile(os.path.join(UPLOAD_DIR, f))]
    if files:
        selected_file_for_delete = st.selectbox("삭제할 파일 선택", options=[""] + files)
        if selected_file_for_delete and st.button("선택한 파일 삭제"):
            os.remove(os.path.join(UPLOAD_DIR, selected_file_for_delete))
            st.success(f"'{selected_file_for_delete}' 삭제 완료!")
            st.rerun()
    else:
        st.info("업로드된 문서가 없습니다.")

# --- 메인 탭 UI ---
tab1, tab2, tab3 = st.tabs(["💬 문서 기반 Q&A (RAG)", "✍️ 문서 요약", "📊 문서 군집 분석"])

# --- 탭 1: RAG Q&A ---
with tab1:
    st.subheader("문서 내용에 대해 AI에게 질문하세요")
    if not openai_api_key:
        st.warning("사이드바에서 OpenAI API 키를 입력하세요.")
    elif not files:
        st.info("먼저 문서를 업로드해주세요.")
    else:
        if "rag_chain" not in st.session_state or st.button("문서 변경, 체인 재생성"):
            with st.spinner("RAG 체인 준비 중..."):
                docs = load_documents(UPLOAD_DIR)
                if docs:
                    st.session_state.rag_chain = build_rag_chain(docs, openai_api_key)
                    st.success("RAG 체인 빌드 완료!")
                else:
                    st.error("문서 로딩에 실패했습니다.")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("질문을 입력하세요..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("답변 생성 중..."):
                    if "rag_chain" in st.session_state:
                        response = st.session_state.rag_chain({"question": prompt})
                        answer = response['answer']
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        st.error("RAG 체인이 초기화되지 않았습니다.")

# --- 탭 2: 문서 요약 ---
with tab2:
    st.subheader("선택한 문서를 AI가 요약합니다")
    if not openai_api_key:
        st.warning("사이드바에서 OpenAI API 키를 입력하세요.")
    elif not files:
        st.info("요약할 문서를 먼저 업로드하세요.")
    else:
        selected_file_for_summary = st.selectbox("요약할 파일 선택", options=[""] + files, key="summary_select")
        if selected_file_for_summary and st.button("선택한 파일 요약하기"):
            with st.spinner(f"'{selected_file_for_summary}' 파일 요약 중..."):
                doc = load_documents(os.path.join(UPLOAD_DIR, selected_file_for_summary))
                if doc:
                    summary = summarize_text(doc[0].page_content, openai_api_key)
                    st.success("요약 결과:")
                    st.write(summary)
                else:
                    st.error("문서 내용을 읽을 수 없습니다.")

# --- 탭 3: 문서 군집 분석 ---
with tab3:
    st.subheader("업로드된 모든 문서를 내용 기반으로 그룹화합니다")
    if not files or len(files) < 2:
        st.info("분석하려면 2개 이상의 문서를 업로드하세요.")
    else:
        if st.button("전체 문서 분석 및 군집화 실행"):
            with st.spinner("문서 임베딩 및 군집화 중..."):
                docs_for_cluster = []
                for f in files:
                    loaded_doc = load_documents(os.path.join(UPLOAD_DIR, f))
                    if loaded_doc:
                        docs_for_cluster.append({"filename": f, "text": loaded_doc[0].page_content})
                result_df = cluster_documents(docs_for_cluster)
                if result_df is not None:
                    st.success("군집 분석 결과:")
                    st.dataframe(result_df)
                else:
                    st.error("분석할 문서가 부족합니다.")
