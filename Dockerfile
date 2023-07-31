FROM python:3.11.4-alpine
LABEL maintainer="AnyLattes"
WORKDIR /app/AnyLattes
COPY . . 
RUN chmod +x dependencias_linux.sh
ENTRYPOINT ["/dependencias_linux.sh"]
ENV FLASK_APP=app
CMD ["python","app.py"]
