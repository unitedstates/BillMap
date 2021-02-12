#!/bin/bash

cd "${0%/*}"
cd ..
cp *.adoc ./server_py/flatgov/static/docs
asciidoctor ./server_py/flatgov/static/docs/*.adoc
rm ./server_py/flatgov/static/docs/*.adoc