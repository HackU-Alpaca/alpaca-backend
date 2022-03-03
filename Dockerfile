
FROM python:3.9

ARG CHANNEL_ACCESS_TOKEN
ARG CHANNEL_SECRET
ENV CHANNEL_ACCESS_TOKEN=$CHANNEL_ACCESS_TOKEN
ENV CHANNEL_SECRET=$CHANNEL_SECRET

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src ./src/
EXPOSE 5000
CMD ["python", "./src/app.py"]
