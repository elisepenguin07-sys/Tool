import pandas as pd
import streamlit as st

st.title("Product Defect Analysis")

# 上傳檔案
uploaded_file = st.file_uploader("Please upload a file", type=["csv", "xlsx"])

if uploaded_file:
    # 讀取檔案
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # 清理欄位名稱
    df.columns = df.columns.str.strip()

    # 指定欄位名稱（根據你提供的）
    bug_column = "Bug's category"  # ← 根據你的資料名稱
    status_column = "狀態"

    if bug_column in df.columns and status_column in df.columns:
        # 建立交叉統計表
        pivot_df = pd.pivot_table(
            df,
            index=bug_column,
            columns=status_column,
            values=df.columns[0],  # 用第一欄作為計數
            aggfunc="count",
            fill_value=0
        )

        # 加總欄位
        pivot_df["Total"] = pivot_df.sum(axis=1)

        # 自訂欄位順序
        desired_order = [
            "New", "To be fixed", "To be verified", "To be comfirmed",
            "Resolved", "Feedback", "Unfinished Closed", "Closed", "Total"
        ]
        final_columns = [col for col in desired_order if col in pivot_df.columns]
        pivot_df = pivot_df[final_columns]

        # 顯示結果
        st.subheader("📊 Result")
        st.dataframe(pivot_df)

        # 匯出按鈕
        csv = pivot_df.reset_index().to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="bug_category_summary.csv",
            mime="text/csv"
        )

    else:
        st.error(f"❌ Missing column(s):'{bug_column}' or '{status_column}'， Please check the column names in your file.")



  


