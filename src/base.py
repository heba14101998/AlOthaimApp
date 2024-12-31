#! <D:\Heba\Practical\AlOthaimApp\src\base.py>

import pytz
import json
import logging
import os
import toml
from datetime import datetime
from dotenv import load_dotenv

class Base:
    
    def __init__(self):

        # Load environment variables
        env_path = os.path.join("..", ".env")
        load_dotenv(env_path)
        
        try:
            # Load Configuration file
            config = toml.load('.streamlit/config.toml')
            self.br_name = config['new_branch'].get('br_name', '') 
            self.br_date = config['new_branch'].get('br_date', '')  
            self.logsize_limit = config['new_branch'].get('logsize_limit', 20) 
            
            # load LLM model from the configuration file
            self.model_name = config['othaimy_chatbot'].get('model_name', 'gemini-1.5-flash')
            self.temperature= config['othaimy_chatbot'].get('temperature', 1)

            # Load database connection details from environment variables
            self.server_ip = os.getenv('DB_SERVER_IP', "10.20.0.10") 
            self.db_name = os.getenv('DB_NAME', "AlOthaimApp") 
            self.uid = os.getenv('DB_USERNAME', "sa")
            self.pwd = os.getenv('DB_PASSWORD', "sa")

            # Load Google API Key for Gemini from environment variables
            self.api_key = os.getenv('GEMINI_API_KEY', '')
        
        except Exception as e:
            logging.error(f"Error loading configuration file or environment variables: {e}. Using default values.")
            self.br_name = ''
            self.br_date = ''
            self.logsize_limit = 50
            self.server_ip = "10.20.0.10"
            self.db_name = "AlOthaimApp"
            self.uid = "sa"
            self.pwd = "sa"

        # Connecting to SQL Server
        self.stag_connection = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={self.server_ip};"
            f"UID={self.uid};"
            f"PWD={self.pwd};"
            f"DATABASE={self.db_name};"
        )

        # Set up logger
        self.cairo_tz = pytz.timezone('Africa/Cairo')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(config['logger'].get('level', 'INFO'))
        formatter = logging.Formatter(
            config['logger'].get('format', "%(asctime)s - [%(levelname)s] - %(filename)s:%(lineno)d - %(message)s")
        )
        # Create the log file path using absolute paths
        log_path = os.path.abspath("logs")
        os.makedirs(log_path, exist_ok=True)
        log_file_path = os.path.join(log_path, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
        # Logger configuration
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Load Branches data from json file 
        self.branch_data_file = os.path.join("assets", "branch_data.json")
        self.branch_data_file = os.path.abspath(self.branch_data_file)
        with open(self.branch_data_file, "r", encoding="utf-8") as f:
            self.branch_data = json.load(f)