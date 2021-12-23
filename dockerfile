FROM python:3.8.3-alpine


# installing dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt


# running application
CMD ["python","server.py"]