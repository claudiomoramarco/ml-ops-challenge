#dipendenze
FROM python:3.9 as builder
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /usr/src/app/wheels -r requirements.txt

#slim se necessario
FROM python:3.9-slim
WORKDIR /usr/src/app
COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --no-cache /wheels/*
COPY ./app ./app
EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]