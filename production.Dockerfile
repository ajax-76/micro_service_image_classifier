FROM python:3.6.9
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install --upgrade pip
RUN apt-get update -y
RUN apt-get install -y libgl1-mesa-dev

# We copy just the requirements.txt first to leverage Docker cache

RUN python3 -m pip install torch==1.5.0+cpu torchvision==0.6.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN python3 -m pip install detectron2==0.1.3+cpu -f https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/index.html
RUN python3 -m pip install pymongo
RUN python3 -m pip install redis
RUN python3 -m pip install -r requirements.txt

COPY . /app
#RUN export FLASK_APP=app.py
#ENTRYPOINT ["flask","run"]
CMD ["python3","msscript_classification.py"]