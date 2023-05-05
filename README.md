# pytests


To run pytests:
```
pytest test_a1_registration_flow_cheap.py --alluredir=allure-report --clean-alluredir
```

To check allure report:
```
allure serve path/to/allure/report/directory
```

Packages:
Python:

Pytest:

Selenium:

Allure-pytest:

## Allure:
wget https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.9.0/allure-commandline-2.9.0.zip
sudo unzip -q allure-commandline-2.9.0.zip -d /opt/
sudo ln -s /opt/allure-2.9.0/bin/allure /usr/bin/allure


## Sphinx
pip3 install sphinx
sphinx-quickstart
sphinx-apidoc -o docs source
.. module:: mymodule
   :synopsis: A brief description of what the module does.

.. automodule:: mymodule
   :members:

make html

