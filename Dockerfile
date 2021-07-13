FROM python:3.8
COPY /app /app
COPY /db /db
COPY pyproject.toml .
COPY wsgi.py .
COPY alembic.ini .
COPY tests /tests/
#WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Run the application
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8081", "wsgi:app"]