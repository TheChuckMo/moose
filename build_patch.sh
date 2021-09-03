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

echo commit version
git commit --all --message "version ${version}"

echo version tag
git tag "${version}"

echo push commmit
git push --all

echo push tags
git push --tags
