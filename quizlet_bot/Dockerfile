FROM python:3.9-slim
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*
WORKDIR /quizlet_bot
COPY . /quizlet_bot
RUN chmod +x /quizlet_bot/wait-for-db.sh
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/quizlet_bot
ENTRYPOINT ["/quizlet_bot/wait-for-db.sh", "python", "main.py"]