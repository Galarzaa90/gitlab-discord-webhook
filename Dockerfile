FROM python:3.12-alpine
WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY gitlab_discord_webhook/ gitlab_discord_webhook/
COPY pyproject.toml .
RUN pip install .

EXPOSE 7400
ENTRYPOINT ["gitlab-discord-webhook"]
