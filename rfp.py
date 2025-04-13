import streamlit as st
import requests
import json
import time

base_url = st.secrets["base_url"]
bearer_token = st.secrets["bearer_token"]
headers = {"Authorization": f"Bearer {bearer_token}"}
polling_time = 10

def poll_status(kickoff_id):
    max_polling_time = 240 # seconds

    while max_polling_time > 0: 
        status_response = requests.get(f"{base_url}/status/{kickoff_id}", headers=headers)
        if status_response.ok:
            status_data = status_response.json()
            if status_data["state"] == "SUCCESS":
                print(status_data)
                result = status_data["result"]
                
                return result
        else:
            # st.error(f"Error: {status_response.text}")
            pass
        time.sleep(polling_time)
        max_polling_time -= polling_time
    
    if max_polling_time == 0:
        st.error("Timeout: The agent did not complete the conversation within the allowed time.")

def submit_message(message):
    inputs = {
        "rfp_question": message,
    }

    response = requests.post(
        f"{base_url}/kickoff",
        json={ "inputs": inputs },
        headers=headers
    )

    if response.ok:
        kickoff_id = response.json().get("kickoff_id", "N/A")
        response = poll_status(kickoff_id)
        return response
    else:
        st.error(f"Error: {response.text}") 

st.title("RFP Helper")


with st.form("rfp_form"):
    rfp_question = st.text_area("RFP Question")
    submit = st.form_submit_button("Submit")

if submit:
    with st.spinner(text="Thinking...", show_time=True):
        response = submit_message(rfp_question)
        st.write(response)