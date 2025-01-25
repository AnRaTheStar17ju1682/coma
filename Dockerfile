FROM python:3.12.8
WORKDIR /coma

COPY pyproject.toml ./

RUN pip install --no-cache-dir .

RUN mkdir ./content
RUN mkdir ./content/thumbnails

COPY static ./static
COPY app ./app
COPY README.md ./README.md

EXPOSE 8000

CMD ["python", "./app/main.py"]
