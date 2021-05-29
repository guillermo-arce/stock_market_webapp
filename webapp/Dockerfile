FROM python:3.6.10-slim
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt 
EXPOSE 7000 
ENTRYPOINT [ "python" ] 
CMD [ "run.py" ] 

