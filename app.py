import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Quản Lý Điểm Sinh Viên", layout="wide")
st.title("🎓 QUẢN LÝ ĐIỂM SINH VIÊN")
st.write("---")

data = {
    'Ho_ten': ["An", "Bình", "Chi", "Dân", "Hải", "Tuấn", "Quân", "Hướng", "Sang", "Hưng"],
    'Chuyen_can': [9.0, 8.5, 7.0, 10.0, 7.5, 6.0, 9.5, 8.5, 10.0, 6.5],
    'Giua_ky': [7.5, 8.5, 10.0, 9.5, 9.0, 6.5, 7.0, 8.0, 6.0, 9.0],
    'Cuoi_ky': [8.0, 7.5, 9.0, 10.0, 6.0, 6.5, 7.0, 9.5, 8.5, 7.5],
}
df = pd.DataFrame(data)

df['Tong_ket'] = (0.2 * df['Chuyen_can'] + 0.3 * df['Giua_ky'] + 0.5 * df['Cuoi_ky']).round(2)

def xep_loai(diem):
    if diem >= 8.5: return 'Giỏi'
    elif diem >= 7.0: return 'Khá'
    elif diem >= 5.0: return 'Trung bình'
    else: return 'Yếu'

df['Xep_loai'] = df['Tong_ket'].apply(xep_loai)

st.subheader("📋 Bảng điểm sinh viên")
st.dataframe(df, use_container_width=True)

st.subheader("📊 Thống kê chung")
dtb_lop = df['Tong_ket'].mean().round(2)
sv_caonhat = df.loc[df['Tong_ket'].idxmax()]
sv_thapnhat = df.loc[df['Tong_ket'].idxmin()]
so_sv_dat = (df['Tong_ket'] >= 5.0).sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Điểm TB cả lớp", f"{dtb_lop}")
col2.metric("Cao nhất", f"{sv_caonhat['Ho_ten']} ({sv_caonhat['Tong_ket']})")
col3.metric("Thấp nhất", f"{sv_thapnhat['Ho_ten']} ({sv_thapnhat['Tong_ket']})")
col4.metric("Số SV đạt (>=5.0)", f"{so_sv_dat}/10")

st.write("---")

st.subheader("🔍 Tra cứu sinh viên")
selected_student = st.selectbox("Chọn tên sinh viên để xem chi tiết:", df['Ho_ten'])
student_info = df[df['Ho_ten'] == selected_student].iloc[0]

st.info(f"**Sinh viên:** {student_info['Ho_ten']} | "
        f"**Chuyên cần:** {student_info['Chuyen_can']} | "
        f"**Giữa kỳ:** {student_info['Giua_ky']} | "
        f"**Cuối kỳ:** {student_info['Cuoi_ky']} | "
        f"**Tổng kết:** {student_info['Tong_ket']} | "
        f"**Xếp loại:** {student_info['Xep_loai']}")

st.write("---")

st.subheader("📈 Biểu đồ điểm tổng kết")
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(df['Ho_ten'], df['Tong_ket'], color='skyblue', edgecolor='navy')

ax.set_title('BIỂU ĐỒ ĐIỂM TỔNG KẾT CỦA SINH VIÊN', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Điểm tổng kết', fontsize=12)
ax.set_ylabel('Tên sinh viên', fontsize=12)
ax.set_xlim(0, 11)
ax.invert_yaxis()

for bar in bars:
    xval = bar.get_width()
    ax.text(xval + 0.15, bar.get_y() + bar.get_height()/2, f'{xval}', ha='left', va='center')

ax.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()

st.pyplot(fig)

st.write("---")
