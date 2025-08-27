FROM python:3.13-slim
RUN apt-get update \
 && apt-get upgrade -y
 
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
 && rm /tmp/*

COPY --chown=ops:ops sftpgo-user-manager.py /sftpgo-user-manager.py
WORKDIR /

ENTRYPOINT ["python", "sftpgo-user-updater.py"]