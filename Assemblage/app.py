import streamlit as st
from PIL import Image
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Stylisation.styling import perform_style_transfer, image_from_prompt
from Classification.imageClassifier import predictClass
from Correction.correction import correction
import glob
from collections import defaultdict
import subprocess

content_path = 'input/'
style_path = 'input/'
output_path = 'output/'



# if current_page.txt does not exist, create it and write "Classification" in it
if not os.path.exists("current_page.txt"):
    with open("current_page.txt", "w") as f:
        f.write("Classification")

# write actual page name to corrent_page.txt
def setPage(page):
    with open("current_page.txt", "w") as f:
        f.write(page)
def getPage():
    with open("current_page.txt", "r") as f:
        return f.read()



# Define the function to display the content for page 1
def Classification():
    st.title("Classification")

    # Upload a folder of images
    image_files = st.file_uploader("Upload one or more image files", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if image_files:
        # Create a dictionary to store the paths of the output folders for each class
        class_folders = {}
        class_images = defaultdict(list)

        output_dir = os.path.join(os.getcwd(), "classification")

        os.makedirs(output_dir, exist_ok=True)
        # Loop through each uploaded file
        for file in image_files:
            # Get the name and content of the uploaded file
            file_name = file.name
            file_content = file.read()

            # Write the content of the uploaded file to a temporary file
            temp_file = os.path.join(os.getcwd(), file_name)
            with open(temp_file, "wb") as f:
                f.write(file_content)

            # Predict the class of the image
            predicted_class = predictClass(temp_file)

            # Create the output folder if it doesn't exist
            if predicted_class not in class_folders:
                class_folders[predicted_class] = os.path.join(output_dir, predicted_class)
                os.makedirs(class_folders[predicted_class], exist_ok=True)

            # Move the image to the output folder
            output_path = os.path.join(class_folders[predicted_class], file_name)
            os.rename(temp_file, output_path)

            # Add the path of the image to the dictionary to display it later sorted by class
            class_images[predicted_class].append(output_path)

        st.warning('Vos images sont dans: '+os.getcwd()+"/classification")
        for class_name, images in class_images.items():
            st.write("Class:", class_name)
            for image_path in images:
                st.image(image_path)
        
# Define the function to display the content for page 2
def Correction():
    st.title("Correction")
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1,1])
    text_input1 = ""
    text_input2 = ""
    with col1:
        st.write("Replace")
    with col2:
        text_input1 = st.text_input("")
    with col3:
        st.write("by")
    with col4:
        text_input2 = st.text_input(" ")
    with col5:
        st.write("in image")
    image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    st.write("Replace " + text_input1 + " by " + text_input2 + " in image")
    if image_file is not None:
        st.image(image_file, use_column_width=True)
    if image_file is not None and text_input1 != "" and text_input2 != "":
        #print("image_file.name: ", image_file.name)
        correction(image_file, text_input1, text_input2, 0.1)
        st.image("output/mask_"+image_file.name)
        st.image("output/image_"+image_file.name)


# Define the function to display the content for page 3
def Stylisation2():
    show_button = False
    st.title("Stylisation lente mais qualitative")
    image1 = False
    image2 = False
    name_image1 = None
    name_image2 = None
    def show_button():
        if(st.button("Générer une image à partir d'un filtre")):
            #perform_style_transfer(content_path+name_image1, style_path+name_image2)
            style_weight = "2e2"
            content_weight = "1e4"   
            command = f"python3 ../models/pytorchNeuralStyleTransfer/neural_style_transfer.py --content_img_name {name_image1} --style_img_name {name_image2} --style_weight {style_weight} --content_weight {content_weight}"
            subprocess.call(command, shell=True)
            #load image at output_path+"output_"+name_image1
            name_image = name_image1.split(".")[0]+"_"+name_image2.split(".")[0]+'.'+name_image1.split(".")[1]
            image = Image.open(output_path+name_image)
            st.image(image, caption="Image stylisée")
    # make a text input


    col1, col2 = st.columns(2)
    with col1:        
        param1 = st.text_input("Alpha", "")   
        uploaded_file = st.file_uploader("Choisissez une image...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image")
            image.save(content_path+uploaded_file.name)
            name_image1 = uploaded_file.name
            image1 = True

    with col2:
        param2 = st.text_input("Beta", "")   
        uploaded_file2 = st.file_uploader("Choisissez un filtre...", type=["jpg", "jpeg", "png"])
        if uploaded_file2 is not None:
            image = Image.open(uploaded_file2)
            st.image(image, caption="Uploaded Image")
            image.save(content_path+uploaded_file2.name)
            name_image2 = uploaded_file2.name
            image2 = True
    if(image2 and image1):
        show_button()


# Define the function to display the content for page 3
def Stylisation():
    show_button = False
    st.title("Stylisation rapide mais peu qualitative")
    image1 = False
    image2 = False
    name_image1 = None
    name_image2 = None
    def show_button():
        if(st.button("Générer une image à partir d'un filtre")):
            perform_style_transfer(content_path+name_image1, style_path+name_image2)
            # load image at output_path+"output_"+name_image1
            nb_files = len(glob.glob("./output/*"))
            name_image = "result"+str(nb_files)+'.jpg'
            image = Image.open(output_path+name_image)
            st.image(image, caption="Image stylisée")
    # make a text input
    textinput = st.text_input("Entrez un prompt", "")

    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("Choisissez une image...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image")
            image.save(content_path+uploaded_file.name)
            name_image1 = uploaded_file.name
            image1 = True

    with col2:
        uploaded_file2 = st.file_uploader("Choisissez un filtre...", type=["jpg", "jpeg", "png"])
        if uploaded_file2 is not None:
            image = Image.open(uploaded_file2)
            st.image(image, caption="Uploaded Image")
            image.save(content_path+uploaded_file2.name)
            name_image2 = uploaded_file2.name
            image2 = True

    if len(textinput)>0 and image1:
        button_prompt = st.button("Générer une image à partir du prompt")
        if(button_prompt):
            # generate image
            image_from_prompt(content_path+name_image1, textinput)
            nb_files = len(glob.glob("./output/*"))
            name_image = "result"+str(nb_files)+'.jpg'
            image = Image.open(output_path+name_image)
            st.image(image, caption="Image stylisée")
    if(image2 and image1):
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
    section[data-testid="stSidebar"]{
        width:0 !important;
    }
    section[data-testid="stSidebar"] button[kind="secondary"]{
        width:100%!important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Define the menu buttons
classification_button = st.sidebar.button("Classification")
correction_button = st.sidebar.button("Correction")
stylisation_button = st.sidebar.button("Stylisation")
stylisation2_button = st.sidebar.button("Stylisation2")

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
if stylisation2_button:
    current_page = "Stylisation2"
    setPage("Stylisation2")
# show current page
locals()[current_page]()


