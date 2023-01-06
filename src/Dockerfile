FROM locustio/locust

# set work directory
RUN mkdir app
RUN mkdir app/reports
WORKDIR /app

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

# # copy project
COPY $REPO_PATH /app

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]