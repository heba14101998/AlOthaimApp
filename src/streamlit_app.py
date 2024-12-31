#! <D:\Heba\Practical\AlOthaimApp\src\streamlit_app.py>
import os
import numpy as np
import base64
import pyodbc
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from typing import Optional

from base import Base
from data_processing import DataProcessor
from check_backup import BackupChecker
from check_logsize import CheckLogSize
from open_branch import OpenNewBranch

class AlOthaimApp(Base):
    """
    Main application class for Abdullah AlOthaim Markets Egypt sales data analysis and backup checks.

    This application provides functionality to:
      - Upload and process Excel files containing sales data
      - Display analysis of branch upload status
      - Highlight branches with delayed or missing uploads
      - Check the last SQL Server backup date
    """

    def __init__(self):
        super().__init__()
        self.data_processor = DataProcessor()
        self.backup_checker = BackupChecker()
        self.logsize_checker = CheckLogSize()
        self.new_branch = OpenNewBranch() 
    
    def display_image(self, path):
        # Get the absolute path of the image
        img_path = os.path.abspath(path)
        # Read the image file in binary mode
        with open(img_path, "rb") as file:
            img = file.read()
        # Encode the binary data to base64
        img_url = base64.b64encode(img).decode("utf-8")
        #display the image in the UI
        st.markdown(
                f'<div style="text-align:center">'
                f'<img src="data:image/png;base64,{img_url}" alt="image" '
                f'</div>',
                unsafe_allow_html=True,
            )
    
    def upload_excel_file(self) -> Optional[st.runtime.uploaded_file_manager.UploadedFile]:
        """
        Provide interface for Excel file upload.
        Returns:
            Optional[UploadedFile]: The uploaded file object if successful, None otherwise
        """
        with st.container():
            st.subheader("Upload Excel File (Sales Data)")
            st.caption("Please upload the Excel file exported from Dynamics 365 Upload Sessions screen")
            return st.file_uploader(
                "Upload Excel File",
                type=["xlsx"],
                help="Drag and drop file here or click to upload.",
                label_visibility="hidden",
                accept_multiple_files=False
            )
    
    def display_sales(self, uploaded_branches: pd.DataFrame, missed_branches: pd.DataFrame) -> None:
        """
        Displays uploaded and missed sales analysis in a Streamlit container with two columns.
        Parameters:
            uploaded_branches: DataFrame of all branches' sales status
            missed_branches: DataFrame of branches with missing/late uploaded sales
        """
        with st.container():
            left_col, right_col = st.columns([1, 1])

            # Get current time in Cairo timezone using pd.Timestamp for better timezone handling
            current_time = pd.Timestamp.now(tz=self.cairo_tz).strftime("%Y-%m-%d %H:%M %p")

            # Left column - Uploaded Branches
            with left_col:
                st.write("\n" * 2)  # Add spacing
                st.subheader("Uploaded Branches", divider="green")
                st.caption(current_time)
                st.markdown(f"<div class='uploaded-branches-box'>{len(uploaded_branches)}</div>", unsafe_allow_html=True)
                st.dataframe(uploaded_branches, use_container_width=False, hide_index=True)

            # Right column - Missed Branches
            with right_col:
                st.write("\n" * 2)  # Add spacing
                st.subheader("Missed Branches", divider="red")
                st.caption(current_time)
                st.markdown( f"<div class='missed-branches-box'>{len(missed_branches)}</div>", unsafe_allow_html=True)

                if not missed_branches.empty:
                    st.dataframe(missed_branches, use_container_width=False, hide_index=True)
                else:
                    st.markdown(
                        """
                        <div style="text-align: center; font-size: 20px; font-weight: bold; ">
                        All branches have successfully uploaded their sales! ☁️🎉
                        </div>
                        """, unsafe_allow_html=True
                    )
                    st.balloons()

    def display_backup(self, healthy_branches: pd.DataFrame, unhealthy_branches: pd.DataFrame) -> None:
        """
        This method displays the analysis results of backup status for all branches in a visually appealing layout. 
        It separates the branches into two categories: healthy branches that have successfully taken their backups 
        and unhealthy branches that have not. 

        Parameters:
            healthy_branches (pd.DataFrame): DataFrame containing the backup status of healthy branches.
            unhealthy_branches (pd.DataFrame): DataFrame containing the backup status of unhealthy branches.
        """
        with st.container():
            left_col, right_col = st.columns([1, 1])

            # Get current time in Cairo timezone using pd.Timestamp for better timezone handling
            current_time = pd.Timestamp.now(tz=self.cairo_tz).strftime("%Y-%m-%d %H:%M %p")

            # Left column - Healthy Branches
            with left_col:
                st.write("\n" * 2)  # Add spacing
                st.subheader("Healthy Branches", divider="green")
                st.caption(current_time)
                st.markdown(f"<div class='uploaded-branches-box'>{len(healthy_branches)}</div>", unsafe_allow_html=True)
                st.dataframe(healthy_branches, use_container_width=False, hide_index=True)

            # Right column - UnHealthy Branches
            with right_col:
                st.write("\n" * 2)  # Add spacing
                st.subheader("Un-Healthy Branches", divider="red")
                st.caption(current_time)
                st.markdown(f"<div class='missed-branches-box'>{len(unhealthy_branches)}</div>", unsafe_allow_html=True)
                
                if not unhealthy_branches.empty:
                    st.dataframe(unhealthy_branches, use_container_width=False, hide_index=True)
                else:
                    st.markdown(
                        """
                        <div style="text-align: center; font-size: 20px; font-weight: bold; ">
                        All Branches Successfully Took Their Backups! 📦🎉
                        </div>
                        """, unsafe_allow_html=True
                    )
                    st.balloons()

    def display_logsize(self, healthy_branches: pd.DataFrame, largelog_branches: pd.DataFrame) -> None:
        """
        This method displays the analysis results of log file sizes for all branches in a visually appealing layout. 
        It separates the branches into two categories: healthy branches that have a normal log file size 
        and unhealthy branches that have a large log file size. 

        Parameters:
            healthy_branches (pd.DataFrame): DataFrame containing the log file size status of healthy branches.
            largelog_branches (pd.DataFrame): DataFrame containing the log file size status of unhealthy branches.
        """
        with st.container():
            left_col, right_col = st.columns([1, 1])

            # Get current time in Cairo timezone using pd.Timestamp for better timezone handling
            current_time = pd.Timestamp.now(tz=self.cairo_tz).strftime("%Y-%m-%d %H:%M %p")

            # Left column - Healthy Branches
            with left_col:
                st.write("\n" * 2)  # Add spacing
                st.subheader("Healthy Branches", divider="green")
                st.caption(current_time)
                
                st.markdown(
                    f"<div class='uploaded-branches-box'>{len(healthy_branches)}</div>",
                    unsafe_allow_html=True
                )
                st.dataframe(healthy_branches, use_container_width=False, hide_index=True)

            # Right column - UnHealthy Branches
            with right_col:
                st.write("\n" * 2)  # Add spacing
                st.subheader("Un-Healthy Branches", divider="red")
                st.caption(current_time)

                st.markdown(
                    f"<div class='missed-branches-box'>{len(largelog_branches)}</div>",
                    unsafe_allow_html=True
                )
                

                if not largelog_branches.empty:
                    st.dataframe(largelog_branches, use_container_width=False, hide_index=True)
                else:
                    st.markdown(
                        """
                        <div style="text-align: center; font-size: 18px; font-weight: bold; color: green;">
                        All Branches Have a Healthy Logfile Size! ✅🎉
                        </div>
                        """, unsafe_allow_html=True
                    )
                    st.balloons()

    def display_opening_steps(self) -> None:
        """
        Displays the steps with checkboxes and handles saving/loading checkbox states.
        """
        
        # Load checkbox states from the database only once
        br_steps_data = self.new_branch.load_checkbox_states()

        # Initialize session state for checkbox states if not already done
        if 'checkbox_states' not in st.session_state:
            st.session_state['checkbox_states'] = br_steps_data.groupby('Category')['Completed'].apply(list).to_dict()

        # Icons for each section
        icons = [":material/cloud:", ":material/warehouse:",  ":material/settings:",
                 ":material/storefront:", ":material/request_quote:", #":material/settings:", 
                 ":material/devices:", ":material/security:", ":material/sync:"]
        
        # Group the data by header to iterate through sections
        grouped_data = br_steps_data.groupby('Category', sort=False)

        # Iterate through each section and its steps
        for myicon, (category, group) in zip(icons, grouped_data):
            with st.expander(f'{category}', icon=myicon): 
                # Iterate through each step in the group for this header
                for index, row in group.reset_index(drop=True).iterrows():
                    is_checked = st.session_state.checkbox_states[category][index]                    

                    # Ensure the checkbox is in sync with the database value
                    st.session_state.checkbox_states[category][index] = st.checkbox(
                        row['Description'],
                        value = is_checked,  # Set initial checkbox state from the database
                        key=f"{category}_{row['StepID']}",
                    )
                    
        # Save button to save the progress
        if st.button("Save"):
            self.new_branch.save_checkbox_states(st.session_state.checkbox_states)
            st.success("Progress saved!")
            # st.balloons()

    def main(self) -> None:
        """
        This method orchestrates the main application flow.
        handling user selection from the sidebar menu and executing the corresponding actions. 
        It consists of the following steps:

        1. Sidebar Menu Configuration: Configures the sidebar menu with options for the user to select from.
        2. User Selection Handling: Handles the user's selection from the sidebar menu and directs the application flow accordingly.
        3. Welcoming Page Display: Displays a welcoming page with the company logo and a brief introduction if the user selects "Home".
        4. Content Display Based on Selection: Executes the following actions based on the user's selection:
            - Sales: Uploads an Excel file, processes the data, and displays sales analysis.
            - Backup: Checks the last backup date and displays the result.
            - Logfile Size: Checks the logfile size and displays the result.
            - Branch Opening: Displays the branch opening checklist.
            - Leave Note: Displays a placeholder for leaving notes (currently under development).
        """
        self.logger.info("Starting application")

        # --- Sidebar Menu ---
        with st.sidebar:
            selected = option_menu(
                        "Main Menu", ["Home","Sales", 'Backup', 'Logfile Size', 'New Branch', 'Leave Note'],
                        icons=['house','cloud-upload', 'database', 'file-earmark-text', 'shop-window', 'pen'],
                        menu_icon="cast", default_index=0, orientation="vertical",
                        styles={"nav-link": {"font-size": "14px"},
                                "nav-link-selected": {"background-color": "green"}}
                    )
        # --- Welcoming Page ---
        if selected == "Home":            
            st.markdown( "<h1 style='text-align: center;'>Abdullah AlOthaim Markets Egypt</h1>", unsafe_allow_html=True)
            self.display_image(os.path.join("assets", "logo.png"))
            
        # --- Review Sales Page ---
        elif selected == "Sales":
            st.markdown("<h1 style='text-align: center;'>Review Sales for Uploaded Branches</h1>", unsafe_allow_html=True)

            uploaded_file = self.upload_excel_file()
            if uploaded_file:

                results_df = self.data_processor.process_data(uploaded_file)
                all_branches, missed_branches = self.data_processor.check_missing_branches(results_df)

                if all_branches is not None and missed_branches is not None:
                    self.display_sales(all_branches, missed_branches)
                else:
                    st.warning("Check The uploaded excel sheet")

        # --- Review Last Backup Date Page ---
        elif selected == "Backup":
            st.markdown("<h1 style='text-align: center;'>Review Last Backup Date</h1>", unsafe_allow_html=True)   
            st.markdown(
                """
                <div style='text-align: center; color: gray;" >
                Verifying the Last Backup Date for Channels Databases on the Staging Server 
                </div>
                """, unsafe_allow_html=True 
            )     
            
            results = self.backup_checker.check_last_backup_date()
            # bar.progress(100, text="Completed")            
            if not results:
                st.error("Turn On your VPN")
            else:
                self.display_backup(results[0], results[1])

        # --- Review Logfile Size Page ---
        elif selected == "Logfile Size":
            st.markdown( "<h1 style='text-align: center;'>Review Logfile Size</h1>", unsafe_allow_html=True )
            st.markdown(
                """
                <div style='text-align: center; color: gray;" >
                Verifying the Logfile Size for Channels Databases on the Staging Server 
                </div>
                """, unsafe_allow_html=True 
            )    
            results = self.logsize_checker.check_logfile_size()
            if not results:
                st.error("Turn On your VPN")
            else:
                self.display_logsize(results[0], results[1])

        # --- New Branch Opening Page ---
        elif selected == "New Branch":
            st.markdown("<h1 style='text-align: center;'>New Branch Opening Checklist</h1>", unsafe_allow_html=True)
            st.markdown(
                f"<div style='text-align: center; color: gray;'>{self.br_name} will open in date: {self.br_date}</div>", 
                unsafe_allow_html=True
            )
            self.display_opening_steps()
            
        elif selected == 'Leave Note':
            st.text("Coming soon!")
            # from streamlit_chat import message

            # st.session_state.setdefault('generated', [])
            # st.title("Leave Note for your Colleagues")
            # chat_placeholder = st.empty()


            # # Function to handle input change
            # def on_input_change():
            #     user_input = st.session_state.user_input
            #     # Only append generated responses, no user message in chat history
            #     st.session_state.generated.append({'type': 'normal', 'data': f"{user_input}"})
            #     # Clear input field after submission
            #     st.session_state.user_input = ''

            # # Function to clear the chat history
            # def on_btn_click():
            #     # Clear only generated responses (no user input displayed)
            #     st.session_state.generated = []

            # with chat_placeholder.container():
            #     # Loop through generated responses and display only those
            #     for i in range(len(st.session_state['generated'])):
            #         message(
            #             st.session_state['generated'][i]['data'], 
            #             key=f"{i}_response", 
            #             allow_html=True,
            #             is_table=True if st.session_state['generated'][i]['type'] == 'table' else False
            #         )

            #     # Button to clear messages
            #     st.button("Clear message", on_click=on_btn_click)

            # # Input field for user to type messages
            # with st.container():
            #     st.text_input("Your Message:", on_change=on_input_change, key="user_input")


if __name__ == "__main__":
        
    st.set_page_config(
        page_title="Abdullah AlOthaim Markets Egypt",
        layout="wide",
        initial_sidebar_state="auto",
        page_icon=os.path.join("assets", "icon.ico")
    )
    
    # Load and apply CSS styling
    css_path = os.path.join("src", "style.css")
    with open(css_path, encoding='utf-8') as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)

    app = AlOthaimApp()
    app.main()
