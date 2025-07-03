
import streamlit as st
import pandas as pd
import math

# 식품 데이터 불러오기
@st.cache_data
def load_data():
    return pd.read_excel("식단매크로.xlsx", sheet_name="식품명단").dropna(subset=["식품"])

df = load_data()

st.title("🥗 식단 설계기 v0.2")
st.markdown("주차별 감량 목표에 맞춘 식단을 구성해보세요!")

# 사용자 입력
goal = st.selectbox("목표", ["벌크", "다이어트"])
body_weight = st.number_input("몸무게 (kg)", min_value=30.0, max_value=200.0, value=70.0)
week = st.number_input("감량 시작 후 몇 주차인가요?", min_value=1, max_value=12, value=1)

# 유지 칼로리 추정 (단순 공식: 33kcal × 체중)
maintain_kcal = round(body_weight * 33)
deficit_kcal = week * 100
target_kcal = maintain_kcal - deficit_kcal

# 단백질 목표 계산
protein_min = round(body_weight * 2.3, 1)
protein_max = round(body_weight * 2.8, 1)

st.write(f"📌 유지 칼로리: {maintain_kcal} kcal")
st.write(f"📉 이번 주 목표 칼로리: {target_kcal} kcal (주당 {deficit_kcal}kcal 감량)")

st.write(f"단백질 목표: {protein_min}g ~ {protein_max}g")

# 식품 선택
selected_foods = st.multiselect("식품 선택", df["식품"].unique())

# 식품 수량 입력 및 합산
total_protein, total_fat, total_carb, total_kcal = 0, 0, 0, 0
food_details = []

for food in selected_foods:
    info = df[df["식품"] == food].iloc[0]
    qty = st.number_input(f"{food} (기준 {info['기준량']}{info['단위']}) - 몇 개/단위?", min_value=0.0, value=1.0, step=0.1)
    food_kcal = info["칼로리"] * qty
    food_details.append((food, info["칼로리"], qty, food_kcal))
    total_protein += info["단"] * qty
    total_fat += info["지"] * qty
    total_carb += info["탄"] * qty
    total_kcal += food_kcal

# 결과 출력
st.subheader("총 섭취량")
st.write(f"단백질: {round(total_protein, 1)}g")
st.write(f"지방: {round(total_fat, 1)}g")
st.write(f"탄수화물: {round(total_carb, 1)}g")
st.write(f"칼로리: {round(total_kcal, 1)} kcal")

# 단백질 피드백
if protein_min <= total_protein <= protein_max:
    st.success("✅ 단백질 목표 범위에 들어왔어요!")
elif total_protein < protein_min:
    st.warning("⚠️ 단백질이 부족해요!")
else:
    st.warning("⚠️ 단백질이 너무 많아요!")

# 칼로리 피드백
diff = total_kcal - target_kcal
if abs(diff) <= 50:
    st.success("✅ 목표 칼로리에 근접했어요!")
elif diff > 0:
    st.warning(f"⚠️ {round(diff)} kcal 초과했어요. 아래 식품들 중 일부 줄여보세요:")
    suggestions = []
    for food, kcal_per_unit, qty, food_kcal in sorted(food_details, key=lambda x: -x[3]):
        if kcal_per_unit > 0:
            reduce_qty = math.ceil(diff / kcal_per_unit * 10) / 10
            if reduce_qty < qty:
                suggestions.append(f"- {food}: {reduce_qty} 단위 줄이기")
    if suggestions:
        for s in suggestions:
            st.write(s)
    else:
        st.info("줄일 수 있는 항목이 많지 않아요. 전체적으로 양을 줄여야 할 수 있어요.")
elif diff < 0:
    st.info(f"ℹ️ {round(-diff)} kcal 더 섭취해도 괜찮아요.")
