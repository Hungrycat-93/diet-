
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_excel("식단매크로.xlsx", sheet_name="식품명단")
    df = df.set_index("식품")
    return df

st.title("🔥 식단 칼로리 계산기")
df = load_data()

selected_foods = st.multiselect("식품 선택", df.index.tolist())

total_kcal = 0
for food in selected_foods:
    if food in df.index:
        unit = df.loc[food, "단위"]
        base_qty = df.loc[food, "기준량"]
        kcal = df.loc[food, "칼로리"]
        qty = st.number_input(f"{food} (기준: {base_qty}{unit})", min_value=0, max_value=1000, step=1)
        total_kcal += kcal * (qty / base_qty)
    else:
        st.warning(f"⚠️ '{food}' 정보가 식품명단에 없습니다.")

st.markdown("---")
st.subheader(f"총 섭취 칼로리: **{total_kcal:.2f} kcal**")
