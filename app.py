import streamlit as st
from PIL import Image
import numpy as np


def fake_predict(image):
    return np.random.randint(0, 10)  


if "history" not in st.session_state:
    st.session_state.history = []

st.title("Image Classification with History")


uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, width=150)
    
    if st.button("Classify"):
       
        prediction = fake_predict(uploaded_file)

        
        st.success(f"Predicted Class: {prediction}")

        
        st.session_state.history.append({
            "image_name": uploaded_file.name,
            "prediction": prediction
        })


st.subheader("Classification History")
if st.session_state.history:
    for item in st.session_state.history:
        st.write(f"🖼️ {item['image_name']} ➡️ **{item['prediction']}**")
else:
    st.info("Chưa có dự đoán nào.")
