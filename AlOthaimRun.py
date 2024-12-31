# ! <D:\Heba\Practical\AlOthaimApp\AlOthaimRun.py>
import streamlit.web.cli as stcli

if __name__ == '__main__':
    stcli._main_run_clExplicit('src/streamlit_app.py', args=['run'], is_hello=False)
