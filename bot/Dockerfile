FROM python:3.8-slim

WORKDIR /app
COPY . .
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r ./requirements.txt --no-cache-dir
CMD ["gunicorn", "bot.wsgi:application", "--bind", "0:8000" ]