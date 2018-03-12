#!/usr/bin/env bash

nosetests -v --cover-html --cover-erase --cover-inclusive --with-coverage
coverage html
xdg-open cover/index.html
