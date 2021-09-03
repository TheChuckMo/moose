#!/bin/bash

build=${1:-patch}

case $build in
  patch|minor|major|prepatch|preminor|premajor|prerelease)
    echo == build ${build}
    ;;
  *)
    echo == build ${build} INVALID
    echo valid: patch, minor, major, prepatch, preminor, premajor, prerelease
    exit 1
    ;;
esac

echo == version ${build}
poetry version ${build}
version=$(poetry version --short)

echo == new ${build} version: ${version}

echo == update and lock
poetry update --lock

echo == pytest
poetry run pytest -v

echo == export requirements.txt
poetry export > requirements.txt

echo == local build
poetry build

echo == commit version
git commit --all --message "version ${version}"

echo == version tag
git tag "${version}"

echo == push commmit
git push --all

echo == push tags
git push --tags
