async function send() {

    // 顯示 loading modal
    document.getElementById("loadingModal").style.display = "flex";

    // 取得表單資料
    const payload = {
        user_name: document.getElementById("user_name").value,
        partner_name: document.getElementById("partner_name").value,
        context: document.getElementById("context").value,
        chat_logs: document.getElementById("chat_logs").value,
    };

    try {
        // 發送 API
        const r = await fetch("/analyze", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        });

        const data = await r.json();

        // 關閉 loading modal
        document.getElementById("loadingModal").style.display = "none";

        // 顯示報告
        document.getElementById("output").textContent = data.report;

        // 顯示下載按鈕
        if (data.download_url) {
            const btn = document.getElementById("downloadBtn");
            btn.href = data.download_url;
            btn.style.display = "block";
        }

    } catch (err) {
        // 發生錯誤也要關掉 loading
        document.getElementById("loadingModal").style.display = "none";

        document.getElementById("output").textContent = 
            "⚠ 發生錯誤，請稍後再試。\n\n" + err;
    }
}
