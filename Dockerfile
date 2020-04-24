FROM python:3.6.8-jessie

COPY requirements.txt /
RUN pip install -r requirements.txt

RUN mkdir djecommerce
COPY . ./djecommerce
WORKDIR /djecommerce

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000/tcp
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000" ]