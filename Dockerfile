FROM python:3.10.10-alpine
COPY . .
WORKDIR .

EXPOSE 5000
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
