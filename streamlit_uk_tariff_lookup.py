import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="UK Tariff Code Lookup", layout="centered")
st.title("UK Tariff Code Lookup Tool")

st.write("Enter a product description in English to search for the most relevant UK tariff (commodity) codes.")

@st.cache_data(show_spinner=False)
def search_tariff_code(query):
    url = f"https://www.trade-tariff.service.gov.uk/api/v2/search_references?query={query}"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    data = response.json()
    results = []
    for item in data.get('data', []):
        attrs = item.get('attributes', {})
        code = attrs.get('reference', '')
        desc = attrs.get('title', '')
        if code and desc:
            results.append({'Commodity Code': code, 'Description': desc})
    return results

def results_to_df(results):
    return pd.DataFrame(results)

query = st.text_input("Product Description", "")

if st.button("Search") and query.strip():
    with st.spinner("Searching UK Tariff Codes..."):
        results = search_tariff_code(query.strip())
    if not results:
        st.warning("No results found. Please try a different description.")
    else:
        df = results_to_df(results)
        st.write("### Search Results")
        selected = st.multiselect(
            "Select one or more codes to export:",
            options=df.index,
            format_func=lambda i: f"{df.iloc[i]['Commodity Code']} - {df.iloc[i]['Description']}"
        )
        st.dataframe(df, use_container_width=True)
        if selected:
            export_df = df.iloc[selected]
            csv = export_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Export Selected to CSV",
                data=csv,
                file_name="selected_uk_tariff_codes.csv",
                mime="text/csv"
            ) 
