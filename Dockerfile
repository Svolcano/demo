FROM python:3.12-bullseye

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./ /code/
# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]