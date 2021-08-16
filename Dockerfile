FROM ubuntu:20.04

# Installing python and pip
RUN apt update && apt dist-upgrade -y
RUN apt install python3.8 python3.8-dev python3-pip -y
RUN ln -s /usr/bin/python3.8 /usr/bin/python

# Installing packages to python
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN python -c "import nltk; nltk.download('all')"
RUN python -c "import fasttext; import fasttext.util; fasttext.util.download_model('en')"

COPY main.py main.py
COPY static/ static/
COPY summarizers/ summarizers/
COPY templates/ templates/

ENV FLASK_APP main

CMD ["flask", "run", "--host=0.0.0.0"]