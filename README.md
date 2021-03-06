[![Circle CI](https://circleci.com/gh/gaia-adm/circleci-tests-processor.svg?style=svg)](https://circleci.com/gh/gaia-adm/circleci-tests-processor) [![Codacy Badge](https://api.codacy.com/project/badge/grade/a13ef84e614744b1bfa139f657899ab0)](https://www.codacy.com/app/alexei-led/circleci-tests-processor) [![](https://badge.imagelayers.io/gaiaadm/circleci-tests-processor:latest.svg)](https://imagelayers.io/?images=gaiaadm/circleci-tests-processor:latest 'Get your own badge on imagelayers.io')

# Circle CI tests data processor

This is Circle CI test results data processor for GAIA analytics. It is based on "gaiaadm/result-processing" Docker image. It adds Python 3.4 and this data processor. It processes data format from <a href="https://circleci.com/api/v1/project/{username}/{project}/{buildNumber}/tests">https://circleci.com/api/v1/project/{username}/{project}/{buildNumber}/tests</a>

## Building

Execute:
- docker build -t gaiaadm/circleci-tests-processor .

## Running

Execute:
- docker run -d -e AMQ_USER="admin" -e AMQ_PASSWORD="mypass" -v "/tmp:/upload" --link rabbitmq:amqserver --link mgs:metricsgw --name circleci-tests-processor gaiaadm/circleci-tests-processor

Note that for development it is recommended to mount a local directory containing result processor directory to /src/processors or mount the processor directory into /src/processors/{processorName}

Executing tests:
- nosetests --with-xunit
or
- python -m unittest discover -s tests -v
