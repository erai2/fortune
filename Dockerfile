FROM python:3.11-slim

WORKDIR /app

COPY New/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY New/ ./

EXPOSE 8501
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
