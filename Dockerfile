FROM python:3.7-alpine

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Prepare duration.csv
RUN mkdir static
RUN echo "description,request id,duration" > static/duration.csv

EXPOSE 5000

ENTRYPOINT [ "sh" ]
CMD [ "./init.sh" ]
