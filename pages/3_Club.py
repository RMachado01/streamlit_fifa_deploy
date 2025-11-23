import streamlit as st
import requests
import base64
from io import BytesIO

st.set_page_config(page_title="Clubes", layout="wide")

def url_to_base64(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        encoded = base64.b64encode(response.content).decode()
        return f"data:image/png;base64,{encoded}"
    except:
        return None

df_data = st.session_state["data"]

clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

df_filtered = df_data[df_data["Club"] == club]

# Logo
url_logo = df_filtered.iloc[0]["Club Logo"]
response = requests.get(url_logo, headers={"User-Agent": "Mozilla/5.0"})
img_bytes = BytesIO(response.content)
st.image(img_bytes, width=50)

st.markdown(f"## {club}")

# ---- LISTA CORRETA SEM FOTO/FLAG URL ----
columns = [
    "Age", "Photo_base64", "Flag_base64", "Overall", "Value", "Wage",
    "Joined", "Height", "Weight", "Contract Valid Until", "Release Clause"
]

df_filtered["Photo_base64"] = df_filtered["Photo"].apply(url_to_base64)
df_filtered["Flag_base64"] = df_filtered["Flag"].apply(url_to_base64)

st.dataframe(
    df_filtered.set_index("Name")[columns],
    column_config={
        "Overall": st.column_config.ProgressColumn(
            "Overall Rating",
            format="%d",
            min_value=0,
            max_value=100
        ),
        "Wage": st.column_config.ProgressColumn(
            "Weekly Wage",
            format="€ %.0f",
            min_value=int(df_filtered["Wage"].min()),
            max_value=int(df_filtered["Wage"].max())
        ),
        "Photo_base64": st.column_config.ImageColumn("Photo"),
        "Flag_base64": st.column_config.ImageColumn("Flag"),
    }
)
