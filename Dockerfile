FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /epam-lab
COPY requirements.txt /epam-lab/
ADD entrypoint.sh /epam-lab/
RUN pip install -r requirements.txt
RUN chmod a+x /epam-lab/entrypoint.sh
COPY . /epam-lab/
ENTRYPOINT ["/epam-lab/entrypoint.sh"]