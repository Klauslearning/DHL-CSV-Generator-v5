import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="UK Tariff Code Lookup V2", layout="centered")
st.title("UK Tariff Code Lookup Tool (V2)")
st.write("Enter a product description in English to search for the most relevant UK tariff (commodity) codes. You can select results and export them to CSV.")

def fetch_tariff_codes(query):
    url = f"https://www.trade-tariff.service.gov.uk/api/v2/search?q={query}"
    headers = {"User-Agent": "dhl-tariff-app/1.0 (contact@example.com)"}
    resp = requests.get(url, headers=headers)
    try:
        data = resp.json()
    except Exception:
        return []
    if isinstance(data, dict) and isinstance(data.get('data', None), list):
        results = []
        for item in data['data']:
            if isinstance(item, dict) and item.get('type') == 'commodity':
                code = item.get('id', '')
                desc = item.get('attributes', {}).get('description', '')
                link = f"https://www.trade-tariff.service.gov.uk/commodities/{code}"
                results.append({
                    'Commodity Code': code,
                    'Description': desc,
                    'Official Link': link
                })
        return results
    else:
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
