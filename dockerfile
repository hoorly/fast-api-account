# Стартовый образ
FROM python:3.11-alpine

# рабочая директория
WORKDIR /usr/src/app

# переменные окружения для python
#не создавать файлы кэша .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# не помещать в буфер потоки stdout и stderr
ENV PYTHONUNBUFFERED 1

# обновим pip
RUN pip install --upgrade pip

# скопируем и установим зависимости. эта операция закешируется 
# и будет перезапускаться только при изменении requirements.txt
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# копируем всё что осталось.
COPY . .

#ENTRYPOINT ["/usr/src/app/entrypoint.sh" ]
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
