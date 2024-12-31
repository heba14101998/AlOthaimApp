#! <AlOthaimApp/src/data_processing.py>
import pandas as pd
from datetime import timedelta

from base import Base


class DataProcessor(Base):

    def __init__(self):
        super().__init__()

    def get_branch_name(self, branch_id):
        """This method returns the branch English and Arabic name for a given branch ID."""
        return self.branch_data.get(str(branch_id), "Unknown Branch")

    def process_data(self, uploaded_file):
        """
        Processes uploaded Excel data and returns a DataFrame following these steps:
            1. Reads the Excel file.
            2. Checks for required columns.
            3. Filters and processes the data.

        Return (pd.DataFrame): Processed DataFrame with branch upload status
        """
        required_columns = {"Channel database", "Date uploaded", "Status"}

        try:
            df = pd.read_excel(uploaded_file)
            if df.empty:
                self.logger.error("Uploaded Excel file is empty")
                raise pd.errors.EmptyDataError(
                    "Uploaded Excel file contains no data")

            # Check for required columns
            missing_cols = required_columns - set(df.columns)
            if missing_cols:
                self.logger.error(f"Missing required columns: {missing_cols}")
                raise ValueError(
                    f"Excel file missing required columns: {missing_cols}")
            else:
                self.logger.info("Excel file successfully loaded")

            # Filter needed columns only
            df = df[list(required_columns)]
            # Filter rows where the status is 'Applied' and drop the 'Status' column
            df_filtered = df[df["Status"] == "Applied"].drop(columns=["Status"])
            
            # Convert 'Date uploaded' to datetime and localize to Cairo timezone
            time_now = pd.Timestamp.utcnow().tz_convert(self.cairo_tz)
            df_filtered["Uploaded Date"] = pd.to_datetime(df_filtered["Date uploaded"], errors='coerce')
            df_filtered["Uploaded Date"] = df_filtered["Uploaded Date"].dt.tz_localize(self.cairo_tz, ambiguous='NaT')
            df_filtered = df_filtered.dropna(subset=["Uploaded Date"]) # Drop rows with invalid dates

            # Extract Branch ID from the index and convert it to string
            df_filtered["Branch ID"] = df_filtered["Channel database"].str.extract(r"(\d+)")[0].astype(str)

            if df_filtered.empty:
                self.logger.error("No valid data remains after filtering")
                return "No valid branch upload data found after processing"

            df_filtered = (df_filtered.sort_values(by=["Channel database", "Uploaded Date"])
                           .drop_duplicates(subset=["Channel database"], keep='last')
                           .reset_index(drop=True))

            # Calculate time difference
            df_filtered["Time Difference"] = time_now - df_filtered["Uploaded Date"]

            self.logger.info("Data processed successfully")
            
            return df_filtered

        except pd.errors.EmptyDataError as e:
            self.logger.error(f"Empty Excel file: {e}")
            return 'Empty Excel file'
        except ValueError as e:
            self.logger.error(f"Invalid data format: {e}")
            return 'Invalid data format'


    def check_missing_branches(self, results_df):
        """
        Analyzes branch status and returns a DataFrame with uploaded sales branches.
        This method checks for branches with a time difference greater than 60 minutes.
        identifies missed branches, and returns two DataFrames: one for the results and one for the missed branches.
        """
        # Check if the DataFrame is empty
        if results_df.empty:
            self.logger.warning("The results DataFrame is empty. No branches to check.")
            return None, None

        # Check if 'Branch ID' column exists
        if "Branch ID" not in results_df.columns:
            self.logger.error("The 'Branch ID' column is missing from the results DataFrame.")
            return None, None

        # Convert 'Time Difference' to timedelta
        results_df['Time Difference'] = pd.to_timedelta(results_df['Time Difference'])
        
        # condition for missed branches based on long period from noe to last uploaded
        condition = results_df["Time Difference"] > timedelta(minutes=60)
        missed_df1 = results_df[condition]
        self.logger.info("Apply condition1 (not outdated)")

        # Identify missed branches using set operations for faster performance
        missed_branches = set(self.branch_data) - set(results_df["Branch ID"])
        self.logger.info("Branch data loaded and filtered.")

        # Create DataFrame for missed branches not exist in the uploaded excel sheet if any
        if missed_branches:
            self.logger.info(f"Missed branches: {', '.join(missed_branches)}")
            missed_df2 = pd.DataFrame({"Branch ID": list(missed_branches)})
            missed_branches_df = pd.concat([missed_df1, missed_df2], axis=0, ignore_index=True)
        else:
            missed_branches_df = missed_df1

        # Select relevant columns for the final DataFrames
        missed_branches_df = missed_branches_df[["Branch ID", "Uploaded Date", "Time Difference"]]

        results_df = results_df[["Branch ID", "Uploaded Date", "Time Difference"]]
        results_df = results_df[~results_df["Branch ID"].isin(missed_branches_df["Branch ID"])]

        return results_df, missed_branches_df
