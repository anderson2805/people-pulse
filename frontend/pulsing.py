import streamlit as st
from datetime import datetime as dt
from backend.generate_output import update_output_excel
from io import BytesIO
from st_download_button import download_button
# Add upload excel file
st.subheader("Enhancing Data with Perplexity and LinkedIn Contexts: LLM Classification of Technology Domains and SSOC (see guide for more info)")

def process_excel(uploaded_file):
    return update_output_excel(uploaded_file)

def to_excel(_workbook):
    buffer = BytesIO()
    _workbook.save(buffer)
    buffer.seek(0)
    return buffer

st.session_state['uploaded_file'] = st.file_uploader("Upload updated template that can be downloaded [here](https://drive.google.com/uc?export=download&id=1lcKRFtCSTrQ08PAigFJb1as5TKU822L6)", type=["xlsx"])

if st.session_state['uploaded_file'] is not None:
    st.write("File uploaded, please wait for processing. This may take a while.")
    
    # Process the workbook and cache the result
    processed_wb = process_excel(st.session_state['uploaded_file'])
    
    # Convert to excel and cache the result
    excel_data = to_excel(processed_wb)
    
    # File datetime
    file_datetime = dt.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Create a download button for the Excel file
    st.session_state['download_click'] = download_button(
        button_text="Download Enriched Output file",
        object_to_download=processed_wb,
        download_filename=f'Output_{file_datetime}.xlsx',

    )

    st.markdown(st.session_state['download_click'], unsafe_allow_html=True)