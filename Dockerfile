FROM python:3.12-slim
 
RUN apt-get update && \
    apt-get -y install gcc mono-mcs
 
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
 
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
 
EXPOSE 50051
# Install pip requirements
COPY requirements.txt .
#RUN apt-get -qq -y install psutil
#RUN apt-get update && apt-get install -y \ gcc python3-dev \ && apt-get clean && rm -rf /var/lib/apt/lists/*
 
RUN python -m pip install -r requirements.txt
 
WORKDIR /app
COPY . /app
 
# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
 
# During debugging, this entry point will be overridden.
CMD ["python", "/app/gRPC/app/server.py"]