FROM python:3.6

# Install ffmpeg
RUN apt-get -y update && apt-get -y install ffmpeg

# Install additional dependencies if needed
# RUN apt-get -y update && apt-get -y install git wget python-dev python3-dev libopenmpi-dev python-pip zlib1g-dev cmake python-opencv

# Set the code directory
ENV CODE_DIR /root/code

# Copy the code to the container
COPY . $CODE_DIR/baselines

# Set the working directory to the baselines directory
WORKDIR $CODE_DIR/baselines

# Clean up pycache and pyc files
RUN rm -rf __pycache__ && \
    find . -name "*.pyc" -delete && \
    
# Install TensorFlow version less than 2 and the test requirements
    pip install 'tensorflow < 2' && \
    pip install -e .[test]

# Set the command to run when the container starts
CMD /bin/bash
