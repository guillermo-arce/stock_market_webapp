# Statement for enabling the development environment
DEBUG = False

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__)) 

DB_HOST = "db-stock-api.ctzh0vubgmat.eu-west-3.rds.amazonaws.com"
DB_USER = "db_client"
DB_PASS = "mFP71F9PTrdDoSnnK3XCD"
DB_PORT = 3306
DB_NAME = "stock_api"