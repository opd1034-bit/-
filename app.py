import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
import re

# ==========================================
# 頁面配置與核心知識庫定義
# ==========================================
st.set_page_config(page_title="台灣總體經濟歷史知識儀表板", layout="wide")

# 定義指標標準名稱（用於內部映射和介面顯示）
ID_利率 = '重貼現率 (%)'
ID_失業 = '失業率 (%)'
ID_通膨 = '通膨率 (CPI %)'
ID_成長 = '經濟成長率 (%)'
ID_GDP = '平均個人名目GDP (元)'
ID_貿易 = '貿易順逆差 (百萬美元)'
ID_M2 = 'M2供給成長率 (%)'

# 核心知識庫：分別顯示會影響各指標之公開事件及其影響機制
# 結構：{ 指標名稱: [ {事件詳情}, ... ] }
# type: 'negative' (紅色, 經濟面的負面衝擊/惡化), 'positive' (綠色, 經濟面的正面發展/改善), 'policy' (灰色, 政策工具調控)
MACRO_EVENTS_KNOWLEDGE_BASE = {
    ID_利率: [
        {"name": "全球金融海嘯", "start": 2008, "end": 2009, "type": "policy",
         "desc": "雷曼兄弟破產引發全球流動性枯竭。央行進入降息循環，大幅調降利率至歷史低點以提供市場流動性。"},
        {"name": "全球通膨升息潮", "start": 2022, "end": 2023, "type": "policy",
         "desc": "疫情後需求爆發及俄烏戰爭致原物料大漲，美聯準會激進升息。台灣央行為抑制輸入性通膨及縮小台美利差，連續調升利率。"}
    ],
    ID_M2: [
        {"name": "「台灣錢淹腳目」時期", "start": 1986, "end": 1989, "type": "positive",
         "desc": "長期鉅額貿易順差疊加《廣場協議》後新台幣升值壓力，熱錢湧入。央行進場買匯釋放新台幣，致M2供給率屢破20%，催生資產泡沫。"},
        {"name": "新冠疫情 QE 狂潮", "start": 2020, "end": 2021, "type": "positive",
         "desc": "全球央行實施無上限量化寬鬆(QE)，加上台灣受惠遠距商機出口極佳、企業資金回流，市場資金極度充沛。"}
    ],
    ID_成長: [
        {"name": "第一次石油危機", "start": 1973, "end": 1974, "type": "negative",
         "desc": "中東戰爭致油價暴漲，引發全球「停滯性通膨」。台灣高度依賴能源進口，生產成本飆升、外銷受阻，經濟成長斷崖式衰退。"},
        {"name": "第二次石油危機", "start": 1979, "end": 1980, "type": "negative",
         "desc": "伊朗革命引發第二次能源衝擊，全球經濟再度陷入衰退，台灣出口導向經濟受挫。"},
        {"name": "網際網路泡沫破裂", "start": 2000, "end": 2001, "type": "negative",
         "desc": "美國科技股崩盤，嚴重衝擊全球電子產業需求。台灣因電子零組件出口佔比極高，創下戰後首次全年經濟負成長(-1.26%)。"},
        {"name": "中美貿易戰 (台商回流)", "start": 2018, "end": 2021, "type": "positive",
         "desc": "美國對中加徵關稅，引發供應鏈重組。政府推動台商回流投資，帶動本土固定資產投資與高階製造產能上升。"}
    ],
    ID_失業: [
        {"name": "亞洲金融風暴與產業外移", "start": 1997, "end": 2000, "type": "negative",
         "desc": "風暴加速東亞供應鏈重組，台灣傳統勞力密集產業大量外移至中國大陸，面臨「結構性失業」，失業率基準線永久性抬升。"},
        {"name": "全球金融海嘯", "start": 2008, "end": 2009, "type": "negative",
         "desc": "出口訂單急凍，科技業與製造業廣泛實施「無薪假」與大量裁員，失業率創下 6.13% 的歷史新高。"}
    ],
    ID_通膨: [
        {"name": "第一次石油危機", "start": 1973, "end": 1974, "type": "negative",
         "desc": "原油價格短時間翻數倍，引發嚴重輸入性通膨。1974年台灣 CPI 年增率飆升超過 47%。"},
        {"name": "俄烏戰爭與供應鏈瓶頸", "start": 2022, "end": 2023, "type": "negative",
         "desc": "戰爭致穀物與能源價格大漲，疊加疫情造成的塞港與晶片短缺。台灣 CPI 多次突破 3% 警戒線。"}
    ],
    ID_GDP: [
        {"name": "《廣場協議》與台幣升值", "start": 1985, "end": 1989, "type": "positive",
         "desc": "美日等國協議逼迫美元貶值，新台幣兌美元大幅升值。在強勢匯率換算下，以美元計價的平均每人名目 GDP 呈現跳躍式翻倍成長。"},
        {"name": "中美貿易戰與 AI 浪潮", "start": 2018, "end": 2023, "type": "positive",
         "desc": "中美貿易戰促使高附加價值生產線回流，加上 AI 伺服器需求爆發，帶動產業升級與出口擴張，名目 GDP 突破 3 萬美元大關。"}
    ],
    ID_貿易: [
        {"name": "推動十大建設", "start": 1974, "end": 1978, "type": "negative",
         "desc": "政府為轉型推動重工業與基礎建設，需自國外大量進口重型機具、原物料與技術設備，龐大進口需求使貿易順差大幅收斂甚至出現短暫逆差。"},
        {"name": "疫情數位轉型與晶片荒", "start": 2020, "end": 2022, "type": "positive",
         "desc": "全球居家辦公與數位轉型狂潮，對半導體晶片與 ICT 硬體需求爆發。台灣憑藉供應鏈優勢，出口額屢創新高，創造史無前例的巨大貿易順差。"}
    ]
}

# 側邊欄：檔案狀態
st.sidebar.header("🛠️ 數據源狀態")
current_files = os.listdir('.')
excel_files = [f for f in current_files if f.endswith('.xlsx') or f.endswith('.xls') or f.endswith('.csv')]
st.sidebar.info(f"📂 目錄下找到 {len(excel_files)} 個潛在資料檔。")


# ==========================================
# 數據解析與處理引擎
# ==========================================
def parse_year(y):
    if pd.isna(y): return np.nan
    s = str(y)
    match = re.search(r'\d{2,4}', s)
    if not match: return np.nan
    y_int = int(match.group())
    return y_int + 1911 if y_int < 1500 else y_int


def parse_value(v):
    if pd.isna(v): return np.nan
    s = str(v).replace(',', '').strip()
    if s == '-': return np.nan
    match = re.search(r'-?(?:\d+\.?\d*|\.\d+)', s)
    if not match: return np.nan
    return float(match.group())


def read_any_format(file_path):
    try:
        df = pd.read_excel(file_path, header=None, dtype=str)
        if len(df.columns) >= 2: return df
    except:
        pass
    encodings = ['utf-8-sig', 'big5', 'cp950', 'utf-8']
    for enc in encodings:
        try:
            df = pd.read_csv(file_path, header=None, dtype=str, encoding=enc, on_bad_lines='skip')
            if len(df.columns) >= 2: return df
        except:
            continue
    return None


def extract_from_matrix(df, col_mapping):
    merged_df = pd.DataFrame(columns=['年份'])
    for std_name, kws in col_mapping.items():
        found = False
        for r in range(min(50, len(df))):
            for c in range(len(df.columns)):
                val = str(df.iat[r, c]).replace(' ', '').lower()
                if val in ['nan', 'none', '']: continue
                if any(kw.lower() in val for kw in kws):
                    val_col_idx = c
                    year_col_idx = -1
                    for yc in range(len(df.columns)):
                        if any(k in str(df.iat[r, yc]) for k in ['年', '期', '月']):
                            year_col_idx = yc
                            break
                    if year_col_idx == -1:
                        for yc in range(len(df.columns)):
                            col_text = "".join(df.iloc[:min(10, len(df)), yc].astype(str)).replace(' ', '')
                            if any(k in col_text for k in ['年', '期', '月']):
                                year_col_idx = yc
                                break
                    if year_col_idx != -1:
                        years = [parse_year(y) for y in df.iloc[r + 1:, year_col_idx]]
                        vals = [parse_value(v) for v in df.iloc[r + 1:, val_col_idx]]
                        temp_df = pd.DataFrame({'年份': years, std_name: vals})
                        temp_df = temp_df.dropna(subset=['年份', std_name], how='any')
                        if not temp_df.empty:
                            temp_df = temp_df.groupby('年份').first().reset_index()
                            if merged_df.empty or '年份' not in merged_df.columns:
                                merged_df = temp_df
                            else:
                                merged_df = pd.merge(merged_df, temp_df, on='年份', how='outer')
                        found = True
                        break
            if found: break
    if not merged_df.empty:
        merged_df['年份'] = merged_df['年份'].astype(int)
    return merged_df


def find_file(keyword):
    for f in excel_files:
        if keyword.lower() in f.lower(): return f
    return None


@st.cache_data
def load_all_data():
    dfs = []
    # 映射表，使用標準定義的 ID
    tasks = [
        {'kw': '重貼現', 'map': {ID_利率: ['重貼現']}},
        {'kw': '失業', 'map': {ID_失業: ['失業']}},
        {'kw': 'cpi', 'map': {ID_通膨: ['總指數', 'cpi']}},
        {'kw': 'gdp', 'map': {ID_成長: ['經濟成長'], ID_GDP: ['名目', '每人', 'gdp']}},
        {'kw': '貿易', 'map': {ID_貿易: ['出(入)超', '出超', '差額']}},
        {'kw': 'm2', 'map': {ID_M2: ['年增率', 'm2']}}
    ]

    for task in tasks:
        file_name = find_file(task['kw'])
        if file_name:
            raw_df = read_any_format(file_name)
            if raw_df is not None:
                df = extract_from_matrix(raw_df, task['map'])
                if not df.empty and len(df.columns) > 1:
                    dfs.append(df)
                    st.sidebar.success(f"✅ 成功萃取：{file_name}")
                else:
                    st.sidebar.warning(f"⚠️ `{file_name}` 無有效數據。")
            else:
                st.sidebar.error(f"❌ 解析失敗：`{file_name}`")
        else:
            st.sidebar.error(f"❌ 找不到包含「{task['kw']}」的檔案。")

    if not dfs: return pd.DataFrame()

    df_merged = pd.DataFrame({'年份': range(1970, 2026)})
    for df in dfs:
        df_merged = pd.merge(df_merged, df, on='年份', how='outer')

    df_merged = df_merged.sort_values('年份').reset_index(drop=True)
    df_merged = df_merged.dropna(subset=[c for c in df_merged.columns if c != '年份'], how='all')
    return df_merged


# ==========================================
# 主介面與繪圖邏輯
# ==========================================
st.title("📈 台灣總體經濟 7 大指標歷史知識儀表板")
st.markdown("自 1970 年至今，重大公開事件對核心經濟指標的影響分析。")

data = load_all_data()
current_indicators = [col for col in data.columns if col != '年份']

if len(current_indicators) > 0:
    st.header("1. 指標走勢與重大事件傳導機制分析")

    # 使用介面上的標準名稱映射回知識庫 Key
    selected_indicator = st.selectbox("請選擇您要觀察的經濟指標：", current_indicators)

    plot_data = data.dropna(subset=[selected_indicator])

    if not plot_data.empty:
        # 繪製標準折線圖
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=plot_data['年份'],
            y=plot_data[selected_indicator],
            mode='lines+markers',
            name=selected_indicator,
            line=dict(width=3, color='#3366CC'),
            hovertemplate="<b>%{x}年</b><br>" + selected_indicator + ": %{y}<extra></extra>"
        ))

        # --- 動態載入並繪製與該指標相關的事件 ---
        related_events = MACRO_EVENTS_KNOWLEDGE_BASE.get(selected_indicator, [])

        for event in related_events:
            # 依據影響類型決定顏色
            if event["type"] == "positive":
                fill_color = "rgba(0, 200, 0, 0.15)"  # 正向：綠色
                label_color = "green"
            elif event["type"] == "negative":
                fill_color = "rgba(230, 0, 0, 0.15)"  # 負向：紅色
                label_color = "red"
            else:
                fill_color = "rgba(100, 100, 100, 0.1)"  # 政策/中性：灰色
                label_color = "black"

            # 添加垂直背景區間
            fig1.add_vrect(
                x0=event["start"], x1=event["end"],
                fillcolor=fill_color, layer="below", line_width=0
            )

            # 添加事件名稱標籤 (直書)
            fig1.add_annotation(
                x=(event["start"] + event["end"]) / 2,  # 區間中間
                y=1, yref="paper",  # 畫布頂端
                text=event["name"],
                showarrow=False,
                textangle=-90,
                xanchor="center", yanchor="top",
                font=dict(color=label_color, size=12),
                yshift=-10
            )

            # 添加無形跡象用於 Hover 顯示詳細傳導機制
            # 在區間內建立透明的散點，並將 description 放入 hover
            dummy_years = list(range(event["start"], event["end"] + 1))
            y_pos = plot_data[selected_indicator].max() if not plot_data.empty else 0

            fig1.add_trace(go.Scatter(
                x=dummy_years,
                y=[y_pos] * len(dummy_years),
                mode='markers',
                marker=dict(opacity=0, size=1),  # 完全透明
                name=event["name"],
                # 核心需求： Hover 顯示詳細傳導機制
                hovertemplate=f"<b>【{event['name']}】</b><br>{event['start']}-{event['end']}<br>影響機制：{event['desc']}<extra></extra>",
                showlegend=False
            ))

        fig1.update_layout(
            title=f"<b>{selected_indicator}</b> 歷史走勢與重大事件映射",
            xaxis_title="年份",
            yaxis_title=selected_indicator,
            hovermode="closest",  # 點對點 Hover，利於顯示事件說明
            height=600,
            xaxis=dict(tickmode='linear', dtick=5)
        )
        st.plotly_chart(fig1, use_container_width=True)

        # 顯示說明面板
        with st.expander("💡 如何查看事件影響機制？", expanded=True):
            st.markdown(f"""
            1.  圖表中**紅色陰影**區間表示該事件對「{selected_indicator}」造成**負面衝擊或導致指標惡化**。
            2.  **綠色陰影**區間表示該事件對指標有**正面推升或導致指標改善**的影響。
            3.  將滑鼠懸停在陰影區間內的折線或上方標籤附近，將會浮現視窗顯示**具體的「影響機制（傳導機制）」**詳細說明。
            """)

    st.markdown("---")

    # 第 2 部分：標準化疊圖
    st.header("2. 總經指標綜合疊圖觀測 (Z-Score 標準化)")
    st.markdown("此圖用以觀察各指標間的長期相關性與領先落後關係。陰影僅標示全球級特大事件。")

    df_overlap = data.dropna(subset=current_indicators).copy()
    if not df_overlap.empty:
        start_yr = df_overlap.iloc[0]['年份']
        st.caption(f"數據交集起算年份：{int(start_yr)}")

        df_std = df_overlap.copy()
        for col in current_indicators:
            df_std[col] = (df_overlap[col] - df_overlap[col].mean()) / df_overlap[col].std()

        fig2 = go.Figure()
        for col in current_indicators:
            fig2.add_trace(go.Scatter(x=df_std['年份'], y=df_std[col], mode='lines', name=col))

        # 綜合圖僅標示最著名的全球事件以防視覺混亂
        GLOBAL_MAJOR_EVENTS = [
            {"name": "第一次石油危機", "start": 1973, "end": 1974},
            {"name": "網路泡沫", "start": 2000, "end": 2001},
            {"name": "全球金融海嘯", "start": 2008, "end": 2009},
            {"name": "新冠疫情爆發", "start": 2020, "end": 2021},
        ]

        for event in GLOBAL_MAJOR_EVENTS:
            if event["end"] >= start_yr:
                fig2.add_vrect(
                    x0=max(event["start"], start_yr), x1=event["end"],
                    fillcolor="rgba(100, 100, 100, 0.1)", layer="below", line_width=0,
                    annotation_text=event["name"], annotation_textangle=-90,
                    annotation_position="top left",
                    annotation_font=dict(size=10, color="gray")  # 已修正此處
                )

        fig2.update_layout(yaxis_title="標準化分數 (Z-Score)", hovermode="x unified", height=650)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("目前載入的數據無共同年份可繪製疊圖。")
else:
    st.error("⚠️ 無法讀取任何指標資料，請確認本機目錄下有符合關鍵字的 Excel/CSV 檔案。")

