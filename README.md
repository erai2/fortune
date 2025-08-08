# FortuneAI 통합 프로젝트

이 저장소는 명리 해석 자동화를 위한 최신 Streamlit 애플리케이션만을 제공합니다.

## 📁 프로젝트 구조

```
New/
├── main.py           # 스트림릿 진입점
├── modules/          # 데이터 처리 및 프롬프트 모듈
└── pages/            # 개별 페이지 구성
```

## 🚀 사용 방법

### 로컬 실행
```bash
pip install -r New/requirements.txt
streamlit run New/main.py
```

`New/secret.toml` 파일에 OpenAI API 키를 저장해야 합니다:
```toml
openai_api_key = "sk-your-key"
```

### Docker 배포
Netlify 설정을 제거하고 Docker로 실행할 수 있는 예제 `Dockerfile`을 제공합니다.

```bash
docker build -t fortune-app .
docker run -p 8501:8501 -v $(pwd)/New/secret.toml:/app/secret.toml fortune-app
```

컨테이너가 실행되면 [http://localhost:8501](http://localhost:8501)에서 앱을 사용할 수 있습니다.
