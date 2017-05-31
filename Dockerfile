# our base image
FROM python:3-onbuild

# specify the port number the container should expose
EXPOSE 3001

#export sendgrid key so sendgrid works
RUN export SENDGRID_API_KEY

#run tests
RUN pytest



# run the application
CMD ["python", "./main.py"]

