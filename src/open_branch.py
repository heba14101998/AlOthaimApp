#! <D:\Heba\Practical\AlOthaimApp\src\open_branch.py>

import pyodbc
import pandas as pd
import numpy as np
from base import Base

class OpenNewBranch(Base):
    
    def __init__(self):
        super().__init__()
        
    # Load checkbox states from SQL Server
    def load_checkbox_states(self):
        """
        Load checkbox states from the SQL Server database.

        Returns:
            pd.DataFrame: A DataFrame containing headers, step indices, step titles, and their checked states.
        """
        self.logger.info(f"Connecting to SQL Server: {self.stag_connection}")

        try:
            with pyodbc.connect(self.stag_connection) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Category, StepID, Description, Completed FROM OpenBranchSteps")
                results = cursor.fetchall()

            # Convert results to a DataFrame
            br_steps_data = pd.DataFrame(
                np.array(results), columns=["Category", "StepID", "Description", "Completed"]
            )

            # br_steps_data["Category"] = br_steps_data["Category"].apply(lambda x: x.split('.')[-1].strip())
            br_steps_data[["StepID", "Completed"]] = br_steps_data[["StepID", "Completed"]].astype(np.int8)
            br_steps_data['Completed'] = br_steps_data['Completed'].map({1: True, 0: False})
            br_steps_data["Completed"] = br_steps_data["Completed"].astype(bool)
            
            return br_steps_data
        
        except pyodbc.Error as e:
            self.logger.error(f"Error loading checkbox states: {e}")
            return None

    def save_checkbox_states(self, checkbox_states):
        """
        Save the current checkbox states back to the database.

        Args:
            checkbox_states (dict): A dictionary containing the checkbox states grouped by headers.
        """
        self.logger.info(f"Connecting to SQL Server: {self.stag_connection}")
        try:
            with pyodbc.connect(self.stag_connection) as conn:
                cursor = conn.cursor()

                for category, states in checkbox_states.items():
                    # Log the category and states being processed
                    self.logger.info(f"Processing category: {category} with states: {states}")

                    # Update each checkbox state directly using the index
                    for step_id, completed in enumerate(states, start=1):  # Assuming StepID starts from 1
                        print(f"Updating {category} StepID {step_id} to {completed}")
                        self.logger.info(f"Updating {category} StepID {step_id} to {completed}")
                        cursor.execute(
                            """
                            UPDATE OpenBranchSteps
                            SET Completed = ?
                            WHERE Category = ? AND StepID = ?
                            """,
                            completed,
                            category,
                            step_id,
                        )

                conn.commit()  # Ensure changes are committed
                self.logger.info("Checkbox states saved successfully.")
        except pyodbc.Error as e:
            self.logger.error(f"Error saving checkbox states: {e}")
        except Exception as ex:
            self.logger.error(f"An unexpected error occurred: {ex}")