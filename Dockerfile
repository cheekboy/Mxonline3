FROM python:3.6.6
COPY . .
run pip install -r requirements.txt
#package.json /opt/apps/p8h_backend

CMD [ "python", "./manage.py runserver 0.0.0.0:8000" ]
#cmd python3.4 madnage.py runserver

