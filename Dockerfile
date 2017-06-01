# our base image
FROM python:3-onbuild

# specify the port number the container should expose
EXPOSE 3001

#Run Tests
RUN pytest

# run the application
CMD ["python", "./main.py"]

