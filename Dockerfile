FROM python:3
ENV PYTHONUNBUFFERED=1
COPY . /epam-lab/
WORKDIR /epam-lab/myshows
RUN pip install -r /epam-lab/requirements.txt && \ 
    chmod a+x /epam-lab/entrypoint.sh
ENTRYPOINT ["/epam-lab/entrypoint.sh"]
