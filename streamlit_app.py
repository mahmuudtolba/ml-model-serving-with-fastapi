# python -m streamlit run streamlit_app.py
# python -m streamlit run streamlit_app.py --server.enableXsrfProtection false

import streamlit as st
import requests
from scripts import s3

# Define the API endpoint
API_URL = "http://127.0.0.1:8502/api/v1/"
headers = {
  'Content-Type': 'application/json'
}

st.title("ML Model Serving Over REST API")

model = st.selectbox("Select Box" , 
                     ["Sentiment analysis" , "Tweet classification" , "Pose classifier"]) 




if model == "Sentiment analysis":
    text = st.text_area("Enter your review" )
    user_id = st.text_input("Enter user id" , "mahmuudtolba@gmail.com")
    data = {
        "text" : [text], 

        "user_id" : user_id

    }
    model_api = "sentiment_analysis"

elif model == "Tweet classification":
    text = st.text_area("Enter Your Tweet")
    user_id = st.text_input("Enter user id", "udemy@kgptalkie.com")

    data = {"text": [text], "user_id": user_id}
    model_api = "tweet_classification"


elif model == "Pose classifier":
    select_file = st.radio("Select the image source", ["Local", "URL"])
    if select_file=="URL":
        url = st.text_input("Enter Your Image Url")

    else:
        image = st.file_uploader('Upload the image' , type=["jpg" , "jpeg" , "png"])
        if image is not None :
            url = s3.upload_direct_image_to_s3(image )
        else :
            url = None

    user_id = st.text_input("Enter user id", "udemy@kgptalkie.com")

    data = {"url": [url], "user_id": user_id}
    model_api = "pose_classifier"

        

# predict buttom

if st.button("predict"):
    with st.spinner("Predicting ... Please wait !!"):
        response = requests.post(
            url=API_URL + model_api, headers=headers ,  
            json=data
        )
        output = response.json()

    st.write(output) 




    

