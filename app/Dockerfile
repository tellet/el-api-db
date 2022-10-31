FROM python:3.10

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

EXPOSE 5000

COPY . .

CMD [ "python", "src/app.py" ]