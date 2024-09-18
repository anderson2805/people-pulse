import streamlit as st

with st.expander("## **Pulsing Process**", expanded=True):
    st.markdown("""The Pulsing process is a series of steps that enriches the data in the output Excel file with data from the web.\nThe process involves the following steps:
                
1. Fill in the [Template](https://drive.google.com/uc?export=download&id=1lcKRFtCSTrQ08PAigFJb1as5TKU822L6), to obtain the "Perplexity Search Query" (Column N).
2. Search on [Perplexity.AI](https://perplexity.ai) using the prompt.
3. Fill up the Perplexity Context columns in the template.
4. Upload the filled template to the Enrichment page. Our program will do the following:

    a. Automatically fill in LinkedIn context based on the LinkedIn URLs given.
    
    b. Classify the Technology Domains and SSOC based on the Perplexity and LinkedIn contexts.
5. You will receive the enriched output Excel file for download. Copy the data to the repo file in teamsite on eworkplace.""")
     
with st.expander("## **Technology Domains Definition**"):
    # Read markdown file
    with open("about/technology-list.md", "r") as file:
        com_b = file.read()
    st.markdown(com_b)
with st.expander("**SSOC Classification**"):
    st.write("""The SSOC Classification process involves classifying individuals to the Singapore Standard Occupational Classification (SSOC) 2024. The process uses the OpenAI Chat API to classify individuals based on specific segments of the SSOC.
             
Detail can be found from the website [here](https://www.singstat.gov.sg/standards/standards-and-classifications/ssoc) or directly via the [SSOC details](https://www.singstat.gov.sg/-/media/files/standards_and_classifications/occupational_classification/ssoc2024-detailed-definitions.ashx).""")