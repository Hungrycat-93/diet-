
import streamlit as st
import pandas as pd

st.set_page_config(page_title="식단 설계 도우미", layout="centered")

@st.cache_data
def load_data():
    df = pd.read_excel("식단매크로.xlsx", sheet_name="식품명단")
    df = df.dropna(subset=["식품"])       # 빈 행 제거
    df = df.set_index("식품")            # 식품명을 인덱스로 설정
    return df

st.title("💪 식단 설계 도우미")

df = load_data()

st.subheader("식품 선택")
food_list = st.multiselect("식품을 선택하세요", df.index.tolist())

total_kcal = 0
diet_plan = []

for food in food_list:
    unit = df.loc[food, "단위"]
    kcal_per_unit = df.loc[food, "열량(kcal)"]

    qty = st.number_input(f"{food} ({unit} 기준)", min_value=0.0, step=1.0, key=food)

    kcal = qty * kcal_per_unit
    total_kcal += kcal

    diet_plan.append((food, qty, unit, kcal))

st.divider()
st.subheader("🍱 총 섭취 열량")
st.metric("총 열량 (kcal)", f"{total_kcal:.1f} kcal")

st.subheader("📋 식단 구성")
if diet_plan:
    diet_df = pd.DataFrame(diet_plan, columns=["식품", "수량", "단위", "kcal"])
    st.dataframe(diet_df.set_index("식품"))
else:
    st.info("선택된 식품이 없습니다.")
