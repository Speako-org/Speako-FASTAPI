FROM python:3.10.11-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY core/ core/
COPY routes/ routes/
COPY schemas/ schemas/
COPY services/ services/
COPY utils/ utils/
COPY templates/ templates/

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]