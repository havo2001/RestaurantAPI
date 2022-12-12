FROM python:3-alpine3.14

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]