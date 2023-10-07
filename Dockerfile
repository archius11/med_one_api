FROM python:3.11-alpine
WORKDIR /code
COPY . /code
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt && chmod +x /code/entrypoint.sh
CMD ["/code/entrypoint.sh"]