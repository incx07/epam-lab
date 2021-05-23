FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /epam-lab
COPY requirements.txt /epam-lab/
RUN pip install -r requirements.txt
COPY . /epam-lab/