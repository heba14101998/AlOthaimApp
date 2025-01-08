# **AlOthaimApp**
![LinkedIn](https://www.linkedin.com/in/heba-mohamed-14101998/)  
![GitHub](https://github.com/heba14101998)  

An on-premises web application designed to streamline daily tasks, monitor server health, and track store sales uploads to the cloud. Built with **Python** and **Streamlit**, this app ensures robust security and efficient data management through seamless integration with **MS SQL Server**.

---

## **Features**
- **Sales Data Tracking:** Monitor the last time stores uploaded their sales data to the cloud.  
- **Daily Task Automation:** Automate repetitive tasks, reducing manual effort and improving productivity.  
- **User-Friendly Interface:** Built with **Streamlit** for an intuitive and easy-to-navigate experience.  
- **Secure On-Premises Deployment:** Ensures data security and compliance with organizational policies.  

---

## **Technologies Used**
- **Programming Language:** Python  
- **Web Framework:** Streamlit  
- **Database:** MS SQL Server  
- **Version Control:** Git, GitHub  
---

## **Installation**
To run **AlOthaimApp** locally, follow these steps:

1. **Clone the Repository:**  
   ```bash
   git clone https://github.com/heba14101998/AlOthaimApp.git
   cd AlOthaimApp
   ```

2. **Set Up a Virtual Environment:**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Database and Security Keys:**  
   - Ensure **MS SQL Server** is installed and running.  
   - Update the database connection settings by copying the .streamlit/config-example.toml file to new file called .streamlit/config.toml.
   - Update .env-example file to new file called .env and add the securty keys.

5. **Run the Application:**  
   ```bash
   streamlit run src/streamlit-app.py
   ```

6. **Access the App:**  
   Open your browser and navigate to `http://localhost:8501`.

---

## **Usage**
1. **Server Health Monitoring:**  
   - View real-time server performance metrics.  
   - Set up alerts for critical issues.  

2. **Sales Data Tracking:**  
   - Monitor the last time each store uploaded sales data.  
   - Generate reports for data synchronization status.  

3. **Daily Task Automation:**  
   - Automate repetitive tasks such as report generation and data backups.  

---

## **Contact**
For questions or feedback, feel free to reach out:  
- **Name:** Heba Mohamed Abdelmonam  
- **Email:** hebamohamed14101998@gmail.com  
- **LinkedIn:** [linkedin.com/in/heba-mohamed-14101998](https://www.linkedin.com/in/heba-mohamed-14101998/)  
- **GitHub:** [github.com/heba14101998](https://github.com/heba14101998)  
