#!/bin/bash

# Run tests and generate report
python3 -m pytest resources/tests/ -v --html=./report.html --self-contained-html

# Open the report in the default browser
open report.html
