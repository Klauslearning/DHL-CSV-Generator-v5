import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="UK Tariff Code Lookup V2", layout="centered")
st.title("UK Tariff Code Lookup Tool (V2)")
st.write("Enter a product description in English to search for the most relevant UK tariff (commodity) codes. You can select results and export them to CSV.")

def fetch_tariff_codes(query):
    # Try /search_references first
    url1 = f"https://www.trade-tariff.service.gov.uk/api/v2/search_references?query={query}"
    resp1 = requests.get(url1)
    if resp1.status_code == 200:
        data1 = resp1.json().get('data', [])
        if data1:
            return [
                {
                    'Commodity Code': item.get('attributes', {}).get('reference', ''),
                    'Description': item.get('attributes', {}).get('title', ''),
                    'Type': item.get('type', ''),
                    'Official Link': f"https://www.trade-tariff.service.gov.uk/commodities/{item.get('attributes', {}).get('reference', '')}"
                }
                for item in data1 if item.get('attributes', {}).get('reference', '')
            ]
    # Fallback to /search
    url2 = f"https://www.trade-tariff.service.gov.uk/api/v2/search?q={query}"
    resp2 = requests.get(url2)
    if resp2.status_code == 200:
        data2 = resp2.json().get('data', [])
        return [
            {
                'Commodity Code': item.get('id', ''),
                'Description': item.get('attributes', {}).get('description', ''),
                'Type': item.get('type', ''),
                'Official Link': f"https://www.trade-tariff.service.gov.uk/commodities/{item.get('id', '')}"
            }
            for item in data2 if item.get('id', '')
        ]
    return []

query = st.text_input("Product Description", "")

if st.button("Search") and query.strip():
    with st.spinner("Searching UK Tariff Codes..."):
        try:
            results = fetch_tariff_codes(query.strip())
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            results = []
    if not results:
        st.warning("No results found. Please try a different description.")
    else:
        df = pd.DataFrame(results)
        st.write("### Search Results")
        st.dataframe(df, use_container_width=True)
        selected = st.multiselect(
            "Select one or more codes to export:",
            options=df.index,
            format_func=lambda i: f"{df.iloc[i]['Commodity Code']} - {df.iloc[i]['Description']}"
        )
        if selected:
            export_df = df.iloc[selected]
            csv = export_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Export Selected to CSV",
                data=csv,
                file_name="selected_uk_tariff_codes.csv",
                mime="text/csv"
            ) 
