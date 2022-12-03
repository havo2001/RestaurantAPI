FROM python:3-alpine3.14

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . ./

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]