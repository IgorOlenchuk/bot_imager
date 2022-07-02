FROM python:3.8
# set work directory
WORKDIR /usr/src/app/
# copy project
COPY . /usr/src/app/
# install dependencies
RUN pip install -r requirements.txt
# run app
CMD ["python", "bot.py"]

ENV TELEGRAM_TOKEN '1318925936:AAFJBq7ZKJQmVKy0vREuLYtdRer6EtuaJO8'