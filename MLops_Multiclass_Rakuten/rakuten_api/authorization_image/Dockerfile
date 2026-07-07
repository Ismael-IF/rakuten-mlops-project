FROM alpine:latest
RUN apk update 
RUN apk add  python3 py3-pip
#RUN pip install requests --user 

RUN mkdir app
COPY requirements.txt  /app/requirements.txt
COPY authorization.py  /app/authorization.py 

WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages
ENTRYPOINT ["python3", "authorization.py"] 

