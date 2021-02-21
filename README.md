### Instructions to Run

1. Install requirements.txt
    - `pip install -r requirements.txt`

    if pattern failed to install, then run
    - `pip install git+https://github.com/uob-vil/pattern.git`

2. Set Expert.ai Auth as Environment variables or Use .env file

    For expert.ai acccount, register @ https://developer.expert.ai/ui/login

    - `export EAI_USERNAME="uuuu@email.com"`
    - `export EAI_PASSWORD="pppp"`

3. Run the streamlit app
    - `streamlit run app.py`