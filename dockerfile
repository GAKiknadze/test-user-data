FROM python:3.10-slim

COPY . .

ARG HOST=0.0.0.0
ARG PORT=8000
ARG DB_URL
ARG DADATA_TOKEN

EXPOSE ${PORT}

RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]
