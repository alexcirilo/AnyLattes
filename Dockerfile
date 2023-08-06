FROM python:3.11.4-alpine
LABEL maintainer="AnyLattes"
WORKDIR /app/AnyLattes
COPY . . 
RUN apk add --no-cache build-base 
RUN pip install --no-cache-dir Flask xlrd 
run pip install -r requirements.txt --no-cache-dir

CMD ["python" "app.py"]
