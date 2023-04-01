import streamlit as st
from PIL import Image
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Stylisation.styling import perform_style_transfer
from Classification.imageClassifier import predictClass

content_path = '../Stylisation/input/'
style_path = '../Stylisation/input/'
output_path = '../Stylisation/output/'


# write actual page name to corrent_page.txt
def setPage(page):
    with open("current_page.txt", "w") as f:
        f.write(page)
def getPage():
    with open("current_page.txt", "r") as f:
        return f.read()



# Define the function to display the content for page 1
def page1():
    st.title("Classification")
    uploaded_file = st.file_uploader("Choisissez une image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        col1, col2 = st.columns(2)
        image.save(content_path+uploaded_file.name)
        classe = predictClass(content_path+uploaded_file.name)
        with col2:
            st.write("La classe prédite est: "+classe)

        with col1:
            st.image(image, caption="Image uploadée", use_column_width=True)
        # save image to input folder
        
# Define the function to display the content for page 2
def page2():
    st.title("Correction")

# Define the function to display the content for page 3
def page3():
    st.title("Stylisation")
    image1 = False
    image2 = False
    name_image1 = None
    name_image2 = None
    def show_button():
        if(st.button("Fusionner!")):
            perform_style_transfer(content_path+name_image1, style_path+name_image2, output_path+"output_"+name_image1)
            # load image at output_path+"output_"+name_image1
            image = Image.open(output_path+"output_"+name_image1)
            st.image(image, caption="Image stylisée")
            
            
    uploaded_file = st.file_uploader("Choisissez une image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")
        print(uploaded_file)
        image.save(content_path+uploaded_file.name)
        name_image1 = uploaded_file.name
        image1 = True
        if(image2):
            show_button()
    uploaded_file2 = st.file_uploader("Choisissez un filtre...", type=["jpg", "jpeg", "png"])
    if uploaded_file2 is not None:
        image = Image.open(uploaded_file2)
        st.image(image, caption="Uploaded Image")
        image.save(content_path+uploaded_file2.name)
        name_image2 = uploaded_file2.name
        image2 = True
        if(image1):
            show_button()

  
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
current_page = getPage()

# Update the current page based on which button was clicked
if classification_button:
    current_page = "Classification"
    setPage("Classification")
if correction_button:
    current_page = "Correction"
    setPage("Correction")
if stylisation_button:
    current_page = "Stylisation"
    setPage("Stylisation")

# Display the selected page
if current_page == "Classification":
    page1()
elif current_page == "Correction":
    page2()
else:
    page3()

