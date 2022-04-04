__version_info__ = ('0', '1', '1')
__version__ = '.'.join(__version_info__)

import glob
import json
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from time import time, sleep

from zipfile import ZipFile

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as Options_Chrome
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def json_config_check(_json_config, _key_list):
    """Checks if read json file contains all required keys
    exists when check is negative (key is missing)

    Args:
        _json_config (dict): the json dict to check
        _key_list (list): A list of given key names for checking

    Returns:
        bool: True if all is ok
    """
    logging.info(f'Checking json config')
    logging.debug(f'{_json_config}')
    for key_check in _key_list:
        if key_check not in _json_config.keys():
            logging.error(f"Json file looks incomplete - key:'{key_check}' is missing")
            sys.exit(99)
    return True


def download_package(type_dl, xpath_string):
    """Download a package

    Args:
        type_dl (str): a text for display in the logs
        xpath_string (str): The Xpath to the link

    Returns:
        A package name found in the innerText of the Xpath

    """
    dl_gracetime = 60
    packagename = driver.find_element(By.XPATH, xpath_string)
    packagename = packagename.get_property("innerText")
    logging.info(f"Packagename:{packagename}")
    dl_file = f"{user_data[0]['downloadfolder']}/{packagename}"
    logging.info(f"Full name:{dl_file}")
    if os.path.exists(f"{dl_file}"):
        logging.info(f"Skip, download of {packagename} - already existing in target")
        return packagename
    else:
        logging.info(f"Click now on the {type_dl} link, downloading {packagename}")
        driver.find_element(By.XPATH, xpath_string).click()
        sleep(1)
        result = wait_for_download(f"{dl_file}/*.crdownload", timeout=dl_gracetime)
        if result is False:
            logging.error(f"Download still not done after {dl_gracetime}s - skip steps after download")
            return 1
        else:
            process_dl_package(dl_file)

    return packagename


def process_dl_package(file_downloaded):
    """Process a downloaded file

    Args:
        file_downloaded (str): the full qualified name to downloaded file

    Returns:
        Returns 0 - success
        Returns 1 - error

    """
    with ZipFile(f'{file_downloaded}', 'r') as zipObj:
        # Extract all the contents of zip file in target directory
        if "setup" in file_downloaded:
            zipObj.extractall(f"{user_data[0]['downloadfolder']}")
            if f"-{user_data[0]['execute']}-" in file_downloaded:
                list_of_files = glob.glob(f"{user_data[0]['downloadfolder']}/*.exe")
                newest_file = max(list_of_files, key=os.path.getctime)
                logging.info(f"Newest file(exe) (assuming downloaded):{newest_file}")
                if ".exe" not in newest_file:
                    logging.warning(f"It looks like this extracted file is not a exe.")
                    return 1
                else:
                    logging.info(f"Starting now:{newest_file}")
                    os.system(f"{newest_file}")
                    return 0
        else:
            if f"-{user_data[0]['extract']}-" in file_downloaded:
                logging.info(f"Extract the portable to target:{user_data[0]['portabletarget']}")
                zipObj.extractall(f"{user_data[0]['portabletarget']}")
                return 0
            else:
                logging.info(f"Do not handle downloaded file:{user_data[0]['portabletarget']}")


def wait_for_download(filedownloadfullpath, timeout=30):
    """Will check if a partial download still exists

    Args:
        filedownloadfullpath (str): the full download name of the target/downloaded file, absolute path
        timeout (int, optional): Timeout given for wait until no partial files are seen anymore

    Returns:
        The return value. True for Download is complete, no partial files seen,
         False for Partial donwloaded file still seen after timeout.

    """
    logging.debug(f'Download timeout is:[{timeout}]')
    time_out = time() + 2
    while not os.path.exists(f'{filedownloadfullpath}') and time() < time_out:
        logging.debug(f'{filedownloadfullpath} not yet seen- waiting for first download')
        sleep(2)
    time_out = time() + timeout
    while os.path.exists(f'{filedownloadfullpath}') and time() < time_out:
        logging.debug(f'{filedownloadfullpath} Seen- waiting')
        sleep(1.5)
    if os.path.exists(f'{filedownloadfullpath}'):
        logging.warning('Download still in progress - may need recheck - aborting wait to continue'
                        ' - may complete in background')
        return False
    else:
        logging.info('Download done successful')
        return True


LOG_FILE = os.path.dirname(os.path.abspath(__file__)) + '/freeCommanderDownAndUp.log'

logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
fh = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=100000, backupCount=10)
sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - [%(name)s.%(funcName)s:%(lineno)d] - %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
sh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(sh)
loglvl_allowed = ['debug', 'info', 'warning', 'error', 'critical']

os.chdir(os.path.dirname(os.path.abspath(__file__)))

key_list_gsjson = ['log_level', 'login_url', 'browser_display', 'downloadfolder', 'portabletarget',
                   'download', 'execute', 'extract',
                   'close_browser']

# read config from json file
json_config_file = 'freeCommanderDownAndUp.json'
if not os.path.exists(json_config_file):
    logging.error(f'Sorry, but config file [{json_config_file}] was not found in dir.')
    sys.exit(96)
with open(json_config_file, 'r') as file:
    user_data = json.loads(file.read())

# read credentials from json
json_credential_file = 'freeCommanderDownAndUp_credential.json'
if not os.path.exists(json_credential_file):
    logging.error(f'Sorry, but credential file [{json_credential_file}] was not found in dir.')
    sys.exit(96)
with open(json_credential_file, 'r') as file:
    user_credential = json.loads(file.read())

log_level = logging.getLevelName('DEBUG')
if user_data[0]['log_level'].lower() in loglvl_allowed:
    log_level = logging.getLevelName(user_data[0]['log_level'].upper())
else:
    logging.debug("Switch back to Debug Level as user used a unexpected value in log level")
logger.setLevel(log_level)

browser_display = user_data[0]['browser_display'].lower()

logging.info(f"freeCommanderDownAndUp Version:{__version__}")
# Precheck
json_config_check(user_data[0], key_list_gsjson)
for x in [user_credential[0]['username'], user_credential[0]['password']]:
    if 'edit_your_' in x:
        logging.error(f"Sorry, you forget to edit the {json_credential_file} - "
                      f"it still contains the dummy user/password "
                      f"[{user_credential[0]['username']}/{user_credential[0]['password']}].")
        sys.exit(98)
# Chrome
chrome_options = Options_Chrome()
if not browser_display == "yes":
    chrome_options.add_argument("--headless")
prefs = {"download.default_directory": f"{user_data[0]['downloadfolder']}"}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chrome_options, executable_path='chromedriver')

try:

    url = f"{user_data[0]['login_url']}"
    wait = WebDriverWait(driver, 10)

    # open browser and login
    logging.info(f"Browser now open on ip:{url}")
    driver.get(url)
    # wait for login field
    logging.info("Wait for Login Page fully displayed")
    wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="amember-login"]')))

    logging.info("Login Page fully displayed3")
    # type in password from json
    driver.find_element(By.XPATH, '//*[@id="amember-login"]').send_keys(user_credential[0]['username'])
    driver.find_element(By.XPATH, '//*[@id="amember-pass"]').send_keys(user_credential[0]['password'])
    logging.info("Typed in User and Password")
    driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div[1]/div[2]/div[1]/div/form/fieldset'
                                  '/div[4]/div/input').click()

    wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="resource-link-page-1"]')))

    # click on login
    logging.info(f"Click now on login button")
    driver.find_element(By.XPATH, '//*[@id="resource-link-page-1"]').click()

    logging.info(f"Download path set to:{user_data[0]['downloadfolder']}")
    if not os.path.exists(f"{user_data[0]['downloadfolder']}"):
        logging.info(f"Create folder {user_data[0]['downloadfolder']}")
        os.makedirs(f"{user_data[0]['downloadfolder']}")

    logging.info(f"Wait for LINK element")
    wait.until(ec.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div[1]/div[2]/div/table[2]/'
                                                           'tbody/tr[1]/td[3]/p[2]/a')))

    downloads = user_data[0]['download'].split(',')
    for download_type in downloads:
        logging.info(f"Processing now {download_type}")
        tr_var = 1
        if f"{download_type}" == "setup32":
            setup32_name = download_package('SETUP 32', '/html/body/div[1]/div[3]/div/div[1]/div[2]/div/table[2]/'
                                                        f'tbody/tr[{tr_var}]/td[2]/p[2]/a')
        elif f"{download_type}" == "setup64":
            setup64_name = download_package('SETUP 64', '/html/body/div[1]/div[3]/div/div[1]/div[2]/div/table[2]/'
                                                        f'tbody/tr[{tr_var}]/td[3]/p[2]/a')
        elif f"{download_type}" == "portable32":
            portable32_name = download_package('Portable 32', '/html/body/div[1]/div[3]/div/div[1]/div[2]/div/table[2]/'
                                                              f'tbody/tr[{tr_var}]/td[2]/p[1]/a')
        elif f"{download_type}" == "portable64":
            portable64_name = download_package('Portable 64', '/html/body/div[1]/div[3]/div/div[1]/div[2]/div/table[2]/'
                                                              f'tbody/tr[{tr_var}]/td[3]/p[1]/a')
        else:
            logging.error("A not supported download type in the json file -"
                          " allowed (portable32, portable64, setup32, setup64)")
    if user_data[0]['close_browser'] == "yes":
        driver.quit()
except Exception as err:
    logging.info('a fatal exception:', err)
finally:
    exit()
