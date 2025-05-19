FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

RUN chmod +x src/prestart.sh

ENTRYPOINT ["src/prestart.sh"]
CMD ["python", "./src/main.py"]
