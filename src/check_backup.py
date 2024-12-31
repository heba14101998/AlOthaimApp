#! <D:\Heba\Practical\AlOthaimApp\src\check_backup.py>

import pyodbc
import pandas as pd
import numpy as np
import streamlit as st
from base import Base

class BackupChecker(Base):
    def __init__(self):
        super().__init__()
        self.bar = None

    def check_br_connection(self, br_name):
        """
        Checks the database connection for a given branch name.
        Parameters:
            br_name (str): The name of the branch to check the connection for.
        Returns:
            str: "Success" if the connection is successful, "Fail" otherwise.
        """
        br_number = int(br_name.split('-')[0].split("BR5")[-1])
        server = f"10.20.{br_number}.10"
        channel_connection = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"UID=itops;"
            f"PWD=itops;"
        )
        
        try:
            with pyodbc.connect(channel_connection) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT @@SERVERNAME")
                output = cursor.fetchone()[0]
            
            return "Success"
            
        except pyodbc.OperationalError as ex:
            self.logger.info(f"{server} is down! {ex}")
            return "Fail"
            

    def check_last_backup_date(self):
        """
        Connects to a SQL Server and retrieves the last backup date for a Review_Backup database from Staging Server(10.20.0.10).
        It also checks the connection status for branches with missed backups.

        Returns (pd.DataFrames, pd.DataFrames): 
            Returns unhealthy branches (branches with missed backups), and healthy branches (branches with recent backups).
        """
        self.logger.info(f"Connecting to SQL Server: {self.stag_connection}")
        self.bar = st.progress(0)
        
        try:
            with pyodbc.connect(self.stag_connection) as conn:
                # Initialize healthy_branches as an empty DataFrame
                healthy_branches = pd.DataFrame(columns=['Server ID', 'Last Backup Date'])
                unhealthy_branches = pd.DataFrame(columns=['Server ID', 'Last Backup Date'])
                
                cursor = conn.cursor()
                
                sql1 = """SELECT * FROM Backup_DB ORDER BY server"""
                cursor.execute(sql1)
                all_data = cursor.fetchall()
                healthy_branches = pd.DataFrame(np.array(all_data), columns=['Server ID', 'Last Backup Date'])
                
                sql2 = """SELECT * FROM BACKUP_DB WHERE DATEDIFF(HOUR, last_db_backup_date, GETDATE()) > 1"""
                cursor.execute(sql2)
                missed_data = cursor.fetchall()
                
                if missed_data:
                    
                    unhealthy_branches = pd.DataFrame(np.array(missed_data), columns=['Server ID', 'Last Backup Date'])
                    self.bar.progress(50, text="Get Last Backup Date for all Branches")

                    # Add column for the time difference from now till last backup
                    now = pd.Timestamp.utcnow().tz_convert(self.cairo_tz)
                    back_date = pd.to_datetime(unhealthy_branches['Last Backup Date']).dt.tz_localize(self.cairo_tz, ambiguous='NaT', nonexistent='shift_forward')
                    unhealthy_branches['Time Difference'] = now - back_date
                    self.logger.info(f"Missed Backup Branches: \n{unhealthy_branches}")

                    # Check connection for unhealthy branches
                    results = []
                    progress = 50 + int(50 / len(unhealthy_branches['Server ID']))
                    for br_name in unhealthy_branches['Server ID']:
                        self.bar.progress(progress, text=f"Pinging {br_name}")
                        result = self.check_br_connection(br_name)
                        results.append(result)

                    self.bar.progress(99, text="Checking Backup Completed ✅")
                    unhealthy_branches['Ping Status'] = results
                
                    healthy_branches = healthy_branches[~healthy_branches['Server ID'].isin(unhealthy_branches['Server ID'])] if not unhealthy_branches.empty else all_branches
                
                healthy_branches.sort_values(by='Server ID', inplace=True)
                unhealthy_branches.sort_values(by='Server ID', inplace=True)

                self.logger.info(f"Number of Branches that take Backup: {len(healthy_branches)}")
                self.logger.info(f"Missed Backup Branches: \n{unhealthy_branches}")
                self.bar.progress(100)
                
                return healthy_branches, unhealthy_branches

        except pyodbc.OperationalError as ex:
            self.logger.error(f"VPN is OFF: {ex}")
            return None, None