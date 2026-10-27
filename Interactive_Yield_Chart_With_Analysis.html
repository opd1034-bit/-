<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>台積電現金殖利率與總經利率互動圖表</title>
    <script src="https://cdn.plot.ly/plotly-2.24.1.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 p-4 md:p-8 font-sans text-gray-800">

    <div class="max-w-6xl mx-auto bg-white p-4 md:p-8 rounded-xl shadow-lg border border-gray-100">
        <h1 class="text-2xl md:text-3xl font-bold mb-2 text-center text-gray-800">台積電現金殖利率 vs 總體經濟利率環境</h1>
        <p class="text-gray-500 mb-6 text-center text-sm md:text-base">
            👉 <b>互動提示：</b>請在圖表上點擊「<b>台積電(2330) 現金股利率</b>」或「<b>美債10年期殖利率</b>」的數據點，下方將自動分析當期升降原因。
        </p>

        <div id="plotly-chart" class="w-full h-[400px] md:h-[550px] mb-8"></div>

        <div id="analysis-panel" class="hidden transform transition-all duration-300">
            <div class="bg-blue-50 border-l-4 border-blue-500 p-6 rounded-r-lg shadow-sm">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-xl font-bold text-blue-900 flex items-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <span id="analysis-title">分析結果</span>
                    </h3>
                </div>
                <div id="analysis-content" class="text-gray-700 leading-relaxed text-base md:text-lg"></div>
            </div>
        </div>
    </div>

    <script>
        const dates = ["2016-03", "2016-06", "2016-09", "2016-12", "2017-03", "2017-06", "2017-09", "2017-12", "2018-03", "2018-06", "2018-09", "2018-12", "2019-03", "2019-06", "2019-09", "2019-12", "2020-03", "2020-06", "2020-09", "2020-12", "2021-03", "2021-06", "2021-09", "2021-12", "2022-03", "2022-06", "2022-09", "2022-12", "2023-03", "2023-06", "2023-09", "2023-12", "2024-03", "2024-06", "2024-09", "2024-12", "2025-03", "2025-06", "2025-09", "2025-12", "2026-03", "2026-06"];
        const tsmcYield = [3.7, 3.69, 3.29, 3.86, 3.7, 3.36, 3.23, 3.49, 3.23, 3.7, 3.05, 3.55, 3.26, 3.35, 2.94, 2.87, 3.47, 3.04, 2.19, 1.89, 1.7, 1.68, 1.72, 1.79, 1.84, 2.31, 2.61, 2.45, 2.06, 1.91, 2.1, 2.19, 1.67, 1.35, 1.36, 1.58, 1.87, 1.6, 1.3, 1.42, 1.25, 0.98];
        const us10yYield = [1.77, 1.47, 1.59, 2.44, 2.39, 2.3, 2.33, 2.41, 2.74, 2.86, 3.06, 2.68, 2.41, 2.0, 1.66, 1.92, 0.67, 0.66, 0.68, 0.91, 1.74, 1.47, 1.49, 1.51, 2.34, 3.01, 3.83, 3.88, 3.47, 3.84, 4.57, 3.86, 4.2, 4.4, 3.8, 4.1, 4.2, 4.3, 4.25, 4.15, 4.1, 4.05];
        const tw1yFixed = [1.16, 1.16, 1.04, 1.04, 1.04, 1.04, 1.04, 1.04, 1.04, 1.04, 1.04, 1.04, 1.04, 1.04, 1.04, 1.04, 0.79, 0.79, 0.79, 0.79, 0.79, 0.79, 0.79, 0.79, 1.09, 1.22, 1.35, 1.47, 1.6, 1.6, 1.6, 1.6, 1.72, 1.72, 1.72, 1.72, 1.72, 1.72, 1.72, 1.72, 1.72, 1.72];
        const twDemand = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.15, 0.25, 0.35, 0.45, 0.55, 0.55, 0.55, 0.55, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65];

        const traceTsmc = { x: dates, y: tsmcYield, type: 'scatter', mode: 'lines+markers', name: '台積電(2330) 現金股利率', line: {color: 'blue', width: 2}, marker: {size: 6} };
        const traceUs10y = { x: dates, y: us10yYield, type: 'scatter', mode: 'lines+markers', name: '美債10年期殖利率', line: {color: 'red', width: 2, dash: 'dash'}, marker: {size: 6, symbol: 'square'} };
        const traceTw1y = { x: dates, y: tw1yFixed, type: 'scatter', mode: 'lines+markers', name: '台灣銀行一年期定存', line: {color: 'green', width: 2, dash: 'dashdot'}, marker: {size: 6, symbol: 'triangle-up'} };
        const traceTwDemand = { x: dates, y: twDemand, type: 'scatter', mode: 'lines+markers', name: '台灣銀行活存', line: {color: 'orange', width: 2, dash: 'dot'}, marker: {size: 6, symbol: 'x'} };

        const layout = {
            title: '', xaxis: { title: '時間 (年份與季度)', tickangle: -45 },
            yaxis: { title: '利率 / 殖利率 (%)' }, hovermode: 'closest', legend: { orientation: 'h', y: -0.2 },
            margin: { t: 20, l: 50, r: 20, b: 80 }
        };

        Plotly.newPlot('plotly-chart', [traceTsmc, traceUs10y, traceTw1y, traceTwDemand], layout, {responsive: true});

        function getExplanation(traceName, date, val, diff) {
            const direction = diff > 0 ? "<span class='text-red-600 font-bold'>上升 ↗</span>" : (diff < 0 ? "<span class='text-green-600 font-bold'>下降 ↘</span>" : "<span class='text-gray-600 font-bold'>持平 →</span>");
            const diffStr = Math.abs(diff).toFixed(2);
            const year = date.substring(0, 4);
            let reason = "";

            if (traceName === '台積電(2330) 現金股利率') {
                if (diff > 0) { 
                    reason = "台積電現金殖利率短期回升，通常原因包含：<br><ul class='list-disc pl-6 mt-2'><li><b>公司決議提高每股配息</b>。</li><li><b>股價經歷修正與下跌</b>：分母變小導致殖利率被動攀升。</li></ul>"; 
                }
                else if (diff < 0) { 
                    reason = "台積電現金殖利率下降，通常原因包含：<br><ul class='list-disc pl-6 mt-2'><li><b>股價大幅上漲</b>：股價漲幅遠超越股息成長幅度，使得殖利率下降。</li></ul>"; 
                }
                else { 
                    reason = "殖利率與前一季度持平，顯示配息政策與股價表現處於相對穩定的狀態。"; 
                }

                // 擴充深度分析：投資增加因素與美債脫鉤關係
                reason += `<br><div class='mt-4 p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded'>
                           <p class='font-bold text-yellow-800 mb-2'>💡 深度分析：投資擴張與美債殖利率的脫鉤現象</p>
                           <ul class='list-disc pl-5 text-sm text-yellow-900 space-y-2'>
                               <li><b>投資增加因素 (高資本支出)：</b>台積電近年積極投入先進製程研發與全球佈局（如美、日、德廠），這類龐大的資本支出需要保留大量盈餘作為成長動能，因此配息的增長速度刻意放緩，進而壓低了現金殖利率。</li>
                               <li><b>與美債利率走勢的關係：</b>自 2022 年起，美債殖利率因激進升息而飆升。傳統上，無風險利率走高會使低殖利率股票失去資金吸引力。然而，台積電憑藉強大的 AI 成長動能，股價逆勢狂飆，導致其現金殖利率持續走低，甚至與高檔的美債殖利率呈現<b>「黃金交叉（美債殖利率 > 台積電殖利率）」</b>。這顯示市場資金已將台積電視為<b>純粹的成長股</b>，投資人追求的是未來的資本利得，而非眼前的現金配息。</li>
                           </ul>
                           </div>`;

            } else if (traceName === '美債10年期殖利率') {
                if (diff > 0) {
                    if (year === "2022" || year === "2023" || year === "2024") { reason = "核心驅動因素為 <b>美國聯準會 (Fed) 啟動激進升息循環</b> 對抗高通膨。市場拋售美債使得債券價格大跌，推升殖利率。"; }
                    else { reason = "反映市場對未來 <b>經濟成長前景樂觀</b> 或 <b>通膨預期升溫</b>，預期央行貨幣政策將趨於緊縮。資金自債市流出，導致殖利率走高。"; }
                } else if (diff < 0) {
                    if (year === "2020") { reason = "主因為 <b>COVID-19 疫情爆發</b>，聯準會緊急降息至零並啟動無限量化寬鬆 (QE)。資金為求避險大量湧入公債，推升債券價格。"; }
                    else { reason = "反映市場擔憂 <b>經濟放緩或衰退風險</b>，或是通膨數據降溫。投資人預期央行將採取降息等寬鬆政策，避險資金推升債券價格，使殖利率下滑。"; }
                } else { reason = "美債殖利率持平，市場可能正處於觀望重大經濟數據或聯準會決策的階段。"; }
            }

            return `<div class="mb-3"><p class="mb-1"><b>當期數值：</b> <span class="text-xl">${val.toFixed(2)}%</span></p><p class="mb-3"><b>相較前期：</b> ${direction} (變化量: ${diffStr}%)</p></div><div class="bg-white p-4 rounded border border-blue-100 shadow-sm"><p class="font-bold text-gray-800 mb-2">📊 總經與市場分析：</p><p class="text-gray-700">${reason}</p></div>`;
        }

        const chart = document.getElementById('plotly-chart');
        const panel = document.getElementById('analysis-panel');
        const analysisTitle = document.getElementById('analysis-title');
        const analysisContent = document.getElementById('analysis-content');

        // 當點擊圖表數據點時觸發分析面板
        chart.on('plotly_click', function(data){
            const pt = data.points[0];
            if (pt.data.name !== '台積電(2330) 現金股利率' && pt.data.name !== '美債10年期殖利率') return;
            const diff = pt.pointIndex > 0 ? pt.y - pt.data.y[pt.pointIndex - 1] : 0;
            panel.classList.remove('hidden');
            analysisTitle.textContent = `${pt.x} - ${pt.data.name} 數據分析`;
            analysisContent.innerHTML = getExplanation(pt.data.name, pt.x, pt.y, diff);
            panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        });
    </script>
</body>
</html>
