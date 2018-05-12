FROM python:3.6-alpine
ADD . /front
WORKDIR /front
RUN pip install -r requirements.txt
CMD ["python", "run.py"]