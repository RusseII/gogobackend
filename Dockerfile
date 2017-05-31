# our base image
FROM python:3-onbuild

# specify the port number the container should expose
EXPOSE 3001

#export sendgrid key so sendgrid works
export SENDGRID_API_KEY

#run tests
pytest



# run the application
CMD ["python", "./main.py"]

