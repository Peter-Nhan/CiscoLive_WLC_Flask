# Python + Flask + Gunicorn
FROM python:slim
COPY requirements.txt /
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 8081
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8081", "app:app"]
