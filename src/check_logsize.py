#! <D:\Heba\Practical\AlOthaimApp\src\check_logsize.py>

import pyodbc
import pandas as pd
import numpy as np
from base import Base

class CheckLogSize(Base):
    def __init__(self):
        super().__init__()

    def check_logfile_size(self):
        """
        Connects to a SQL Server and retrieves the logfile size for each specific channel database.
        This method checks the log file size for each branch and categorizes them into healthy and large log branches.
        """
        self.logger.info(f"Connecting to SQL Server: {self.stag_connection}")

        try:
            with pyodbc.connect(self.stag_connection) as conn:
                cursor = conn.cursor()
                # SQL query to fetch branches with log file size greater than the specified limit
                sql1 = """SELECT Server, SizeMB/1024, physical_name FROM logfile_size WHERE SizeMB > ?*1024"""
                cursor.execute(sql1, self.logsize_limit)
                data = cursor.fetchall()
                large_log_branches = pd.DataFrame(np.array(data), columns=['Server ID', 'Size (GB)', 'File Path'])
                
                # SQL query to fetch all branches ordered by server
                sql2 = """SELECT Server, SizeMB/1024, physical_name FROM logfile_size ORDER BY Server"""
                cursor.execute(sql2)
                data = cursor.fetchall()
                tmp = pd.DataFrame(np.array(data), columns=['Server ID', 'Size (GB)', 'File Path'])
                
                # Filter out branches with large log files to get healthy branches
                healthy_branches = tmp[~tmp['Server ID'].isin(large_log_branches['Server ID'])]
                
            healthy_branches.sort_values('Server ID', inplace=True)
            large_log_branches.sort_values('Server ID', inplace=True)

            self.logger.info(f"Number of Healthy Log file Branches: {len(healthy_branches)}")
            self.logger.info(f"Number of un-Healthy Log file Branches: {len(large_log_branches)}")

            return healthy_branches, large_log_branches

        except pyodbc.OperationalError as ex:
            self.logger.error(f"VPN is OFF: {ex}")
            return None