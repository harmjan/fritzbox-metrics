FROM python:slim-buster

MAINTAINER Harmjan Treep "mail@harmjantreep.nl"

WORKDIR /opt/fritzbox-metrics

# Copy the requirements and install them
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the source file later, I'll edit main.py more often and don't want to have to rerun
# pip install every time
COPY ./main.py .

CMD ["python3", "-u", "main.py"]
