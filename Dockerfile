FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /epam-lab
COPY . /epam-lab/
RUN pip install -r requirements.txt && \ 
    chmod a+x /epam-lab/entrypoint.sh
ENTRYPOINT ["/epam-lab/entrypoint.sh"]
