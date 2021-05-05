# mcmk
API testing

## How to setup
1. Install python3.9, pip
2. git clone https://github.com/lofmat/mcmk.git
3. cd mcmk
4. pip install -r requirements.txt
5. Download last stable build of Selenium WebDriver https://github.com/mozilla/geckodriver/releases
6. Add WebDriver path to **config/test.ini** as **selenium_driver_path**

## How to run tests
1. Include selenium driver directory to **PATH**:
 export PATH=$PATH:%selenium_driver_path%
2. python3.9 -m pytest -s -v

NOTE: Tested with Ubuntu18 and Python3.9

 