FROM python:3.9-slim
WORKDIR /quizlet_bot
COPY . /quizlet_bot
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/quizlet_bot
CMD ["python", "main.py"]