FROM python:3.11.4-bullseye
LABEL maintainer="AnyLattes"
WORKDIR /app/AnyLattes
COPY . . 
RUN pip install --no-cache-dir Flask xlrd pycairo==1.24.0
run pip install -r requirements.txt --no-cache-dir

# CMD ["python" "app.py"]
CMD python app.py
