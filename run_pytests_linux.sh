#!/bin/bash

# Install Python 3 and pip
sudo apt update
sudo apt install -y python3 python3-pip

# Install Java Runtime Environment (JRE)
sudo apt install -y default-jre

# Install pytest, selenium, and other required Python packages
pip3 install pytest selenium pytest-xdist pytest-html pytest-rerunfailures snoop requests

# Install Allure command line tool
sudo apt-key adv --fetch-keys 'https://dl.bintray.com/user/downloadSubjectPublicKey?username=bintray'
echo "deb https://dl.bintray.com/qameta/generic qameta-generic main" | sudo tee /etc/apt/sources.list.d/qameta-generic.list
sudo apt update
sudo apt install -y allure

# Add Allure command line tool to system path
export PATH=$PATH:/opt/allure/bin
echo 'export PATH=$PATH:/opt/allure/bin' >> ~/.bashrc

# Install WebDriver for Chrome
sudo apt install -y unzip
sudo apt install -y chromium-chromedriver

# Install Firefox browser
sudo apt install -y firefox

# Add geckodriver to system path
sudo mv /usr/bin/geckodriver /usr/local/bin/

# Install Allure pytest plugin
pip3 install allure-pytest

# Run pytests
pytest --alluredir=allure-report --clean-alluredir

# Generate temporary allure report
allure serve allure-report  

# Generate report
# allure generate --clean
