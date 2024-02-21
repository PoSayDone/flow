FROM python:3.11
WORKDIR /usr/src/dev
COPY ./backend ./backend
COPY ./backend/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
