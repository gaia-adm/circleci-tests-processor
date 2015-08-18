#!/usr/bin/env python3.4
import os
import json
import unittest
from tests.test_utils import execute_processor
from testfixtures import compare


def data_file_path(file_name):
    return os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', file_name))


class TestProcessor(unittest.TestCase):
    def test_circleci_tests1(self):
        custom_metadata = {'SCM_BRANCH': 'master', 'SCM_REPO_NAME': 'jenkins-tests-processor',
                           'SCM_URL': 'https://github.com/gaia-adm/jenkins-tests-processor',
                           'BUILD_URI': 'https://circleci.com/gh/gaia-adm/jenkins-tests-processor/12',
                           'BUILD_NUMBER': '12',
                           'BUILD_STATUS': 'success', 'BUILD_START_TIME': '2015-08-18T08:59:27.444Z'}
        output = execute_processor(data_file_path('circleci-tests1.json'), custom_metadata=custom_metadata)
        output_json = json.loads(output.decode("utf-8"))
        # print(output.decode("utf-8"))

        # this is what we expect
        with open(data_file_path('result-tests1.json'), "rt") as myfile:
            expected_json = json.load(myfile)

        compare(expected_json, output_json, strict=True)


if __name__ == '__main__':
    unittest.main()
