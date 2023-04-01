import streamlit as st
from PIL import Image



# Define the function to display the content for page 1
def page1():
    st.title("Classification")
    uploaded_file = st.file_uploader("Choisissez une image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Image uploadée")

# Define the function to display the content for page 2
def page2():
    st.title("Correction")

# Define the function to display the content for page 3
def page3():
    st.title("Stylisation")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")
# Define the layout of the app
st.set_page_config(page_title="My Streamlit App", page_icon=":smiley:")

# Set the CSS styles for the page
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Define the menu buttons
classification_button = st.sidebar.button("Classification")
correction_button = st.sidebar.button("Correction")
stylisation_button = st.sidebar.button("Stylisation")

# Define a variable to store the current page
current_page = "Classification"

# Update the current page based on which button was clicked
if classification_button:
    current_page = "Classification"
if correction_button:
    current_page = "Correction"
if stylisation_button:
    current_page = "Stylisation"

# Display the selected page
if current_page == "Classification":
    page1()
elif current_page == "Correction":
    page2()
else:
    page3()