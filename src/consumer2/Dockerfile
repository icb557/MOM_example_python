FROM python:3.12.9-alpine3.21
RUN addgroup pythonapp && adduser -S -G pythonapp pythonapp
USER pythonapp
WORKDIR /app/
COPY --chown=pythonapp requirements.txt .
RUN pip install -r requirements.txt
COPY --chown=pythonapp . .
CMD ["python", "consumer.py"]