FROM gaiaadm/result-processing:latest-python

# Bundle app source
COPY . /src/processors/circleci-tests-processor

# setup.sh script is temporary workaround until Docker adds support for passing ENV variables
# to docker build command to allow setting up proxy
ADD setup.sh /tmp/setup.sh
RUN chmod +x /tmp/setup.sh \
    && /tmp/setup.sh /src/processors/circleci-tests-processor

# generate pyc cache
RUN python -m compileall /src/processors/circleci-tests-processor
