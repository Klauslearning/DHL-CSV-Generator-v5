import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="UK Tariff Code Fuzzy Search", layout="centered")
st.title("UK Tariff Code Fuzzy Search")

st.write("Enter a product description in English (e.g. 'men's leather shoes', 'plastic bag', 'cotton shirt'). All similar commodity codes will be listed below.")

def fuzzy_search_tariff(query):
    url = f"https://www.trade-tariff.service.gov.uk/api/v2/search?q={query}"
    headers = {"User-Agent": "dhl-tariff-app/1.0 (contact@example.com)"}
    resp = requests.get(url, headers=headers)
    try:
        data = resp.json()
    except Exception:
        return []
    results = []
    if isinstance(data, dict) and isinstance(data.get('data', None), list):
        for item in data['data']:
            code = item.get('id', '')
            desc = item.get('attributes', {}).get('description', '')
            type_ = item.get('type', '')
            if code and desc and type_ == 'commodity':
                results.append({
                    'Commodity Code': code,
                    'Description': desc,
                    'Official Link': f"https://www.trade-tariff.service.gov.uk/commodities/{code}"
                })
    return results

query = st.text_input("Product Description", "")

if st.button("Search") and query.strip():
    with st.spinner("Searching..."):
        results = fuzzy_search_tariff(query.strip())
    if not results:
        st.warning("No results found. Please try a different description.")
    else:
        df = pd.DataFrame(results)
        st.write("### Similar Commodity Codes")
        st.dataframe(df, use_container_width=True)
        selected = st.multiselect(
            "Select codes to export:",
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
