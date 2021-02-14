#!/bin/bash

cd "${0%/*}"
cd ..
cp ./*.adoc ./server_py/flatgov/static/docs
cp ./server_py/flatgov/crs/*.adoc ./server_py/flatgov/static/docs
cp media/*.png ./server_py/flatgov/static/docs/media/
asciidoctor ./server_py/flatgov/static/docs/*.adoc
rm ./server_py/flatgov/static/docs/*.adoc