#!/bin/bash

echo version patch
poetry version patch
version=$(poetry version)

echo new version: ${version}

echo update and lock
poetry update --lock

echo export requirements.txt
poetry export > requirements.txt

echo local build
poetry build
