#!/bin/bash

function test_connection()
{
    curl --connect-timeout 5 -s -X OPTIONS http://www.google.com >> /dev/null
}

function setup_proxy()
{
    proxies[0]=http://proxy.bbn.hp.com:8080
    proxies[1]=http://web-proxy.israel.hp.com:8080

    # first try no proxy
    test_connection

    if [ $? -eq 0 ];then
       echo "No proxy is necessary"
       return 0
    else
       echo "Detecting suitable proxy server.."
       for i in "${proxies[@]}"
       do
           export http_proxy=$i
           export https_proxy=$i
           export no_proxy=localhost,127.0.0.1

           test_connection
           if [ $? -eq 0 ];then
               echo "Connection through proxy "$i" was successful"
               return 0
           fi
       done
    fi
    echo "No suitable proxy was found"
    return 1
}

function setup_processor()
{
    echo "Setting up data processor.."
    # install any data processor dependencies here
    pip install ijson==2.2
    pip install python-dateutil==2.4.2
    # test dependencies
    pip install testfixtures==4.2.0
    pip install nose==1.3.7
}

setup_proxy

if [ $? -eq 0 ];then
    set -x
    setup_processor
else
    echo "Unable to continue setup"
    exit 1
fi
