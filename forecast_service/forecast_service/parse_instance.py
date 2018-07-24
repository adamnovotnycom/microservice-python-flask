import configparser
import os

MODE = os.environ["APP_MODE"]
CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 
    "instance", "secrets.ini")))

app_url = CONFIG[MODE]["APP_URL"]
app_user = CONFIG[MODE]["APP_USER"]
app_password = CONFIG[MODE]["APP_PASSWORD"]
dataservice_url = CONFIG[MODE]["DATASERVICE_URL"]
dataservice_user = CONFIG[MODE]["DATASERVICE_USER"]
dataservice_password = CONFIG[MODE]["DATASERVICE_PASSWORD"]
google_creds_file = CONFIG[MODE]["GOOGLE_CREDS"]
google_creds = str(os.path.abspath(os.path.join(os.path.dirname( __file__ ),
    "instance", google_creds_file)))
google_project = CONFIG[MODE]["GOOGLE_PROJECT"]
optimal_portfolio_update_url = CONFIG[MODE]["OPTIMAL_PORTFOLIO_UPDATE_URL"]
optimal_portfolio_update_key = CONFIG[MODE]["OPTIMAL_PORTFOLIO_UPDATE_KEY"]
slack_url = CONFIG[MODE]["SLACK_URL"]