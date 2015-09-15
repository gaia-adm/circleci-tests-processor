#!/usr/bin/env python3.4
import sys
import signal
import json
from dateutil.parser import parse as parseDateTime
from utils import get_params

def get_json_parser():
    """
    Returns a JSON parser. If possible yajl2 (written in C) wrapper is used, if not found a Python parser implementation
    is used.
    """
    ijson = None
    try:
        # try to use yajl dll/so first (faster)
        import ijson.backends.yajl2 as ijson
    except ImportError:
        # if not yajl available, use Python JSON parser
        import ijson.backends.python as ijson
    finally:
        return ijson

def parse_class_name(class_name):
    """
    Parses full class name into package and short class name.
    """
    if class_name.endswith('.story'):
        # i.e stories/sanity/ci-sanity/myName.story
        index = class_name.rfind('/')
    else:
        # TODO: class name format may be language specific, this works for Java
        index = class_name.rfind('.')
    if index != -1 and (index + 1) <= len(class_name):
        return class_name[:index], class_name[index + 1:]
    else:
        return None, class_name

def create_test_execution_event(content_metadata, custom_metadata, test_execution):
    """
    Creates code_testrun event for GAIA message gateway. For data format see https://github.com/gaia-adm/api-data-format.
    """
    test_run_event = {'event': 'code_testrun'}
    dateTime = parseDateTime(custom_metadata['BUILD_START_TIME'])
    dateTime = dateTime.replace(microsecond = 0)
    test_run_event['time'] = dateTime.isoformat()
    # source
    source = {}
    source['build_uri'] = custom_metadata.get('BUILD_URI')
    source['job_name'] = custom_metadata.get('SCM_REPO_NAME')
    source['repository'] = custom_metadata.get('SCM_URL')
    source['branch'] = custom_metadata.get('SCM_BRANCH')
    test_run_event['source'] = source
    # tags
    tags = {}
    tags['build_result'] = custom_metadata.get('BUILD_STATUS')
    tags['source_type'] = test_execution['source_type']
    test_run_event['tags'] = tags
    # id part
    id = {}
    id['file'] = test_execution['file']
    id['method'] = test_execution['name']
    package, clazz = parse_class_name(test_execution['classname'])
    if package != None:
        id['package'] = package
    if clazz != None:
        id['class'] = clazz
    id['build_number'] = custom_metadata.get('BUILD_NUMBER')
    test_run_event['id'] = id
    # result part
    result = {}
    result['status'] = test_execution['result']
    result['error'] = test_execution.get('message')
    result['run_time'] = float(test_execution.get('run_time'))
    test_run_event['result'] = result
    return test_run_event

def process_test_execution(content_metadata, custom_metadata, test_execution):
    """
    Processes single CircleCI test execution. Creates GAIA code_testrun event and writes it on STDOUT. Caller is
    responsible for sending the data to message gateway.
    """
    # create the test run event object
    event = create_test_execution_event(content_metadata, custom_metadata, test_execution)
    # write the object on stdout in JSON
    sys.stdout.write(json.dumps(event))

def process_tests_json(content_metadata, custom_metadata):
    sys.stdout.write('[')
    ijson = get_json_parser()
    # parser = ijson.parse(open('c:\circleci-tests.json', mode='rb'))
    parser = ijson.parse(sys.stdin.buffer)
    count = 0
    test_execution = None
    expected_key = None
    for prefix, event, value in parser:
        if prefix == 'tests.item':
            if event == 'start_map':
                test_execution = {}
            elif event == 'end_map':
                if count > 0:
                    sys.stdout.write(',')
                process_test_execution(content_metadata, custom_metadata, test_execution)
                count = count + 1
            elif event == 'map_key':
                expected_key = value
        else:
            if expected_key != None and prefix == ('tests.item.' + expected_key):
                test_execution[expected_key] = value
            expected_key = None
        # print(prefix + ':' + event + ':' + str(value))
    sys.stdout.write(']')

# when executed from command line
def execute():
    def signal_handler(_signo, _stack_frame):
        sys.stderr.write('Caught ' + _signo + ', exiting')
        sys.exit(1)

    signal.signal(signal.SIGTERM, signal_handler)

    content_metadata, custom_metadata = get_params()

    if len(content_metadata) > 0:
        process_tests_json(content_metadata, custom_metadata)
    else:
        # no parameters, just exit
        print('[]')
        sys.exit(0)

