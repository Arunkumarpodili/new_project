FROM python:3.9-slim-buster
WORKDIR /app
ADD requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_RUN-HOST=0.0.0.0
EXPOSE 8080
CMD ["flask", "run"]