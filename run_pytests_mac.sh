#!/bin/bash

# # Install Homebrew package manager
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3 and pip
brew install python

# Install Java Runtime Environment (JRE)
brew install --cask adoptopenjdk

# Install pytest, selenium, and other required Python packages
pip3 install pytest selenium pytest-xdist pytest-html pytest-rerunfailures snoop requests

# Install Allure command line tool
brew install allure

# Install WebDriver for Chrome
brew install chromedriver

# Install Allure pytest plugin
pip3 install allure-pytest

# Run pytests
pytest --alluredir=allure-report --clean-alluredir

# Generate temporary allure report
allure serve allure-report                                                           

# Generate report if temporary is not enough
# allure generate --clean
