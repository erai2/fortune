import re
from pathlib import Path
from typing import Tuple, List

from .db_utils import load_json, save_json

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "suam_analysis.json"


def load_analysis() -> List[dict]:
    """Load stored analysis entries."""
    return load_json(DB_PATH)


def save_analysis(data: List[dict]):
    """Persist analysis entries."""
    save_json(DB_PATH, data)


def build_prompt(tiangan: str, dizhi: str, topic: str) -> str:
    return (
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
        f"\n예시 명식:\n천간: {tiangan}\n지지: {dizhi}"
    )


def llm_auto_analysis(api_key: str, tiangan: str, dizhi: str, topic: str) -> Tuple[List[str], str]:
    """Return analysis fields and the prompt used."""
    from langchain_openai import ChatOpenAI

    prompt = build_prompt(tiangan, dizhi, topic)
    llm = ChatOpenAI(openai_api_key=api_key, temperature=0.2, model="gpt-3.5-turbo")
    response = llm.invoke(prompt)
    text = response.content
    parts = re.split(r"\n?[\d\.]+[\)\.] ", text)
    if len(parts) < 6:
        table = tiangan_desc = dizhi_desc = hapchung_desc = reality = ""
    else:
        _, table, tiangan_desc, dizhi_desc, hapchung_desc, reality = parts[:6]
    return [table.strip(), tiangan_desc.strip(), dizhi_desc.strip(), hapchung_desc.strip(), reality.strip()], prompt
