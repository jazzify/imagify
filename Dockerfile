# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

# Install requirements
RUN python -m pip install -r requirements.txt
RUN pip install pipenv && pipenv install --system --deploy

EXPOSE 8000

# Give some special permisions to upload files to the container
RUN chgrp -R www-data uploaded_files/
RUN chmod -R g+w uploaded_files/

ADD docker-entrypoint.sh /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
