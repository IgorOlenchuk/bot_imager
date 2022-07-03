FROM python:3.7-slim

RUN apt-get update && apt-get install -y \
    software-properties-common \
    unzip \
    curl \
    xvfb 
RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" >> /etc/apt/sources.list.d/debian.list
RUN apt-get update
RUN apt-get install -y --no-install-recommends firefox
RUN apt install wget
ENV GECKODRIVER_VERSION 0.31.0
RUN wget --no-verbose -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz \
  && rm -rf /opt/geckodriver \
  && tar -C /opt -zxf /tmp/geckodriver.tar.gz \
  && rm /tmp/geckodriver.tar.gz \
  && mv /opt/geckodriver /opt/geckodriver-$GECKODRIVER_VERSION \
  && chmod 755 /opt/geckodriver-$GECKODRIVER_VERSION \
  && ln -fs /opt/geckodriver-$GECKODRIVER_VERSION /bin/geckodriver \
  && ln -fs /opt/geckodriver-$GECKODRIVER_VERSION /bin/wires

RUN mkdir /app
COPY requirements.txt /app
RUN mkdir /app/screenshots
# install dependencies
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt --no-cache-dir
# copy project
COPY ./ /app/
# set work directory
WORKDIR /app
# run app
CMD ["python", "bot.py"]
ENV TELEGRAM_TOKEN ${TELEGRAM_TOKEN}