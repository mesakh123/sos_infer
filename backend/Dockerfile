
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# Update aptitude with new repo
RUN apt-get update
RUN apt-get install git ffmpeg libsm6 libxext6  -y

COPY . /backend/

WORKDIR /backend/


RUN pip install -r /backend/requirements.txt

CMD ["sh","-c","alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload"]