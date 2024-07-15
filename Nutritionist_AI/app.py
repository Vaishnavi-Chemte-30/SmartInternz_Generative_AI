# Health Management App
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load all environment variables
load_dotenv()

# Configure the Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, image[0], prompt])
    return response

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                # Get the mime type of the uploaded file
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")

# Initialize our Streamlit app
input_prompt = """
You need to see the food items and provide the details of every food item.
"""    

st.set_page_config(page_title="AI Nutritionist App")
st.header("AI Nutritionist App")
input_text = st.text_input("Input Prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
submit = st.button("Tell me the total calories")    

# If submit button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input_text)
    st.subheader("The Response is")
    
    # Print and inspect the response object
    st.write(response)
    
    # Print all attributes and methods of the response object
    st.write(dir(response))
    
    # Attempt to access the content of the response object
    try:
        # Inspect possible attributes of response object
        if hasattr(response, 'content'):
            response_text = response.content
        elif hasattr(response, 'text'):
            response_text = response.text
        else:
            response_text = 'No content found in the response.'
        st.write(response_text)
    except AttributeError as e:
        st.error(f"Error in processing response: {e}")
