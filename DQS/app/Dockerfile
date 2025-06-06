FROM python:3.10

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501"]
