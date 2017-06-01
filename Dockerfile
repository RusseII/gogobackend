# our base image
FROM python:3-onbuild

# specify the port number the container should expose
EXPOSE 3001


# run the application
CMD ["python", "./main.py"]

