import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

st.set_page_config(page_title="台積電(2330)估值動態分析儀", layout="wide")

# Streamlit Cloud 是 Linux 環境，不能使用 Windows 的 C:\Users\... 絕對路徑。
# 因此改成讀取 GitHub repository 根目錄的資料檔。
BASE_DIR = Path(__file__).resolve().parent
FILE_QUARTERLY = BASE_DIR / "20261006112135.txt"
FILE_DAILY = BASE_DIR / "20261006111625.txt"


@st.cache_data
def load_and_process_data():
    """讀取 TXT 檔案並轉換為季度資料。"""
    df_q = pd.read_csv(FILE_QUARTERLY, sep="\t")
    df_d = pd.read_csv(FILE_DAILY, sep="\t")

    # 日資料：每季取最後一筆交易資料
    df_d["年月日"] = pd.to_datetime(
        df_d["年月日"].astype(str).str.strip(), format="%Y%m%d"
    )
    df_d = df_d.sort_values("年月日")
    df_d["Quarter"] = df_d["年月日"].dt.to_period("Q")
    df_d_q = df_d.groupby("Quarter", as_index=False).last()
    df_d_q["Quarter_str"] = df_d_q["Quarter"].astype(str)

    # 季資料
    df_q["年月"] = df_q["年月"].astype(str).str.strip()
    df_q["Year"] = df_q["年月"].str[:4]
    df_q["Quarter_str"] = (
        df_q["Year"] + "Q" + df_q["季別"].astype(str).str.strip()
    )

    merged_df = pd.merge(df_d_q, df_q, on="Quarter_str", how="inner")
    merged_df["估值指標(PB/MB)"] = pd.to_numeric(
        merged_df["股價淨值比-TEJ"], errors="coerce"
    )

    return merged_df.sort_values("Quarter_str").reset_index(drop=True)


def main():
    st.title("📈 台積電 (2330) 估值動態分析與決策系統")
    st.markdown(
        "本系統整合**市值淨值比 (M/B)** 與 **股價淨值比 (P/B)**，"
        "透過歷史分位數模型，動態評估當前股價位階。"
    )

    # 雲端部署時，兩個 TXT 必須和 app.py 一起放在 GitHub repository。
    missing = [p.name for p in (FILE_QUARTERLY, FILE_DAILY) if not p.exists()]
    if missing:
        st.error("❌ GitHub repository 尚缺少資料檔：" + ", ".join(missing))
        st.info(
            "請將上述 TXT 檔放到 GitHub repository 根目錄；"
            "Streamlit Community Cloud 會在 GitHub 更新後自動重新部署。"
        )
        st.stop()

    try:
        df = load_and_process_data()

        pb_series = df["估值指標(PB/MB)"].dropna()
        if pb_series.empty:
            st.error("❌ 找不到有效的『股價淨值比-TEJ』資料。")
            st.stop()

        pb_25 = pb_series.quantile(0.25)
        pb_75 = pb_series.quantile(0.75)

        latest_data = df.dropna(subset=["估值指標(PB/MB)"]).iloc[-1]
        latest_q = latest_data["Quarter_str"]
        latest_pb = latest_data["估值指標(PB/MB)"]
        latest_cap = latest_data["市值(百萬元)"]
        latest_pe = latest_data["當季季底P/E"]
        latest_growth = latest_data["淨值成長率"]

        st.divider()
        st.subheader(f"📊 最新季度估值診斷 ({latest_q})")

        if latest_pb <= pb_25:
            status = "便宜 (Undervalued)"
            reason = f"""
            **判斷原因 (便宜)：**
            1. **跌破歷史估值下緣**：當前 P/B 為 **{latest_pb:.2f} 倍**，已低於歷史 25% 分位數（{pb_25:.2f} 倍）。
            2. **安全邊際較高**：從資產估值角度來看，市場定價處於相對低位。
            3. **基本面輔助**：目前本益比(P/E)為 {latest_pe} 倍，淨值成長率為 {latest_growth}%。
            """
            st.success(f"### 目前股價位階：【{status}】")
        elif latest_pb >= pb_75:
            status = "昂貴 (Overvalued)"
            reason = f"""
            **判斷原因 (昂貴)：**
            1. **突破歷史估值上緣**：當前 P/B 為 **{latest_pb:.2f} 倍**，已高於歷史 75% 分位數（{pb_75:.2f} 倍）。
            2. **市場溢價較高**：此位階代表市場對未來成長的預期已反映較多。
            3. **基本面輔助**：最新本益比(P/E)為 {latest_pe} 倍，淨值成長率為 {latest_growth}%。
            """
            st.error(f"### 目前股價位階：【{status}】")
        else:
            status = "合理區間 (Fair Value)"
            reason = f"""
            **判斷原因 (合理)：**
            當前 P/B 為 **{latest_pb:.2f} 倍**，落在歷史 25%~75% 區間（{pb_25:.2f} ~ {pb_75:.2f} 倍）內。
            市場給予的估值處於合理中性水位。
            """
            st.warning(f"### 目前股價位階：【{status}】")

        st.info(reason)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("最新 P/B（M/B）", f"{latest_pb:.2f} 倍")
        col2.metric("最新季底總市值", f"{latest_cap:,.0f} 百萬元")
        col3.metric("歷史 25% 分位數", f"{pb_25:.2f} 倍")
        col4.metric("歷史 75% 分位數", f"{pb_75:.2f} 倍")

        st.divider()
        st.subheader("📈 趨勢互動圖表（支援游標懸浮、縮放）")

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Bar(
                x=df["Quarter_str"],
                y=df["市值(百萬元)"],
                name="季底總市值 (百萬元)",
                opacity=0.7,
            ),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(
                x=df["Quarter_str"],
                y=df["估值指標(PB/MB)"],
                name="P/B & M/B",
                mode="lines+markers",
                line=dict(width=3),
                marker=dict(size=8),
            ),
            secondary_y=True,
        )

        fig.add_hline(
            y=pb_75,
            line_dash="dash",
            annotation_text=f"昂貴線 75% ({pb_75:.2f})",
            secondary_y=True,
        )
        fig.add_hline(
            y=pb_25,
            line_dash="dash",
            annotation_text=f"便宜線 25% ({pb_25:.2f})",
            secondary_y=True,
        )

        fig.update_layout(
            title_text="台積電 季度市值與淨值比估值走勢",
            hovermode="x unified",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02,
                xanchor="right", x=1
            ),
            height=650,
        )
        fig.update_yaxes(
            title_text="總市值 (百萬元)", secondary_y=False, tickformat=","
        )
        fig.update_yaxes(
            title_text="淨值比倍數 (P/B & M/B)", secondary_y=True
        )

        st.plotly_chart(fig, use_container_width=True)

        with st.expander("📂 展開查看完整歷史季資料明細"):
            st.dataframe(
                df[
                    [
                        "Quarter_str",
                        "市值(百萬元)",
                        "估值指標(PB/MB)",
                        "淨值成長率",
                        "當季季底P/E",
                    ]
                ],
                use_container_width=True,
            )

    except Exception as e:
        st.error(f"❌ 發生資料處理錯誤：{e}")


if __name__ == "__main__":
    main()
