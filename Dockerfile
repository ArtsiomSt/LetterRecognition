FROM django

WORKDIR /app

COPY converter .

CMD ["python3", "manage.py", "runserver"]