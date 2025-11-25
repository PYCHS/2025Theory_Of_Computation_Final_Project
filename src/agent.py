import os
import markdown
from datetime import datetime
from src.llm_client import get_completion
from src.prompts import ANALYSIS_SYSTEM_PROMPT
from src.knowledge import get_concept_guide

class PsychAgent:
    def __init__(self):
        self.user_name = ""
        self.partner_name = ""
        self.context = ""
        self.chat_logs = ""

    def ask(self, question):
        print(f"\n🤖 諮商師: {question}")
        return input(f">> ").strip()

    def ask_multiline(self, question):
        print(f"\n🤖 諮商師: {question}")
        print("(輸入完畢請換行輸入 'DONE' 送出)")
        buffer = []
        while True:
            line = input(">> ")
            if line.strip().upper() == "DONE":
                break
            if line.strip():
                buffer.append(line)
        return "\n".join(buffer)

    def run_interview(self):
        print("\n" + "="*50)
        print("歡迎來到 AI 情感諮商室 ❤️")
        print("我是你的專屬分析師，在開始分析前，我想先認識你們。")
        print("="*50)

        # 1. Basic Info
        self.user_name = self.ask("請問怎麼稱呼您？")
        self.partner_name = self.ask(f"嗨 {self.user_name}，請問讓您感到煩惱的對象叫什麼名字？")

        # 2. Context (Subjective)
        self.context = self.ask_multiline(
            f"好的，{self.user_name}。能不能跟我說說，最近您跟 {self.partner_name} 之間發生了什麼情感問題？\n(您可以盡情抱怨或描述當下的情境)"
        )

        # 3. Chat Logs (Objective)
        self.chat_logs = self.ask_multiline(
            f"了解... 聽起來確實不容易。為了讓我分析得更準確，\n我可以看一下您跟 {self.partner_name} 的聊天紀錄嗎？\n(請直接複製貼上對話內容)"
        )

        # 4. Analysis
        print(f"\n(收到。正在統整描述與對話紀錄，進行分析中...)\n")
        self.generate_report()

    def generate_report(self):
        # Format prompt
        final_prompt = ANALYSIS_SYSTEM_PROMPT.format(
            user_name=self.user_name,
            partner_name=self.partner_name,
            context=self.context,
            chat_logs=self.chat_logs
        )
        
        # Call LLM
        messages = [{"role": "user", "content": final_prompt}]
        llm_analysis = get_completion(messages)

        if llm_analysis:
            # Combine: Knowledge Guide + Analysis
            full_report = get_concept_guide() + "\n" + llm_analysis
            
            # Print to console
            print(full_report)
            
            # Save to file
            self.save_report(full_report)

    def save_report(self, content):
        # Ensure directory exists
        if not os.path.exists("reports"):
            os.makedirs("reports")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"reports/report_{self.user_name}_vs_{self.partner_name}_{timestamp}"
        
        # 1. Save Raw Markdown
        md_path = f"{base_filename}.md"
        try:
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(content)
        except IOError as e:
            print(f"Error saving MD: {e}")

        # 2. Save Styled HTML
        html_path = f"{base_filename}.html"
        
        # Convert MD to HTML
        html_body = markdown.markdown(content)

        # CSS: Warm & Professional Theme
        html_content = f"""
        <!DOCTYPE html>
        <html lang="zh-TW">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Relationship Analysis - {self.user_name}</title>
            <style>
                :root {{
                    --primary-color: #d65d7a; 
                    --bg-color: #fff9fa;      
                    --card-bg: #ffffff;       
                    --text-color: #4a4a4a;    
                    --accent-color: #ffafbd;  
                }}
                
                body {{
                    font-family: "Microsoft JhengHei", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                    line-height: 1.8;
                    background-color: var(--bg-color);
                    color: var(--text-color);
                    margin: 0;
                    padding: 40px 20px;
                }}

                /* Container Layout & Animation */
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background-color: var(--card-bg);
                    padding: 50px;
                    border-radius: 20px;
                    box-shadow: 0 10px 30px rgba(214, 93, 122, 0.1);
                    transition: transform 0.3s ease;
                }}
                .container:hover {{
                    transform: translateY(-5px);
                }}

                /* Typography */
                h1 {{
                    color: var(--primary-color);
                    text-align: center;
                    font-size: 2.2em;
                    margin-bottom: 40px;
                    border-bottom: 3px solid var(--accent-color);
                    padding-bottom: 15px;
                }}

                h2 {{
                    color: #c44569;
                    margin-top: 50px;
                    padding-left: 15px;
                    border-left: 5px solid var(--primary-color);
                    background: linear-gradient(to right, #fff0f3, #fff);
                    padding: 10px 15px;
                    border-radius: 0 10px 10px 0;
                    position: relative;
                }}

                h3 {{
                    color: #57606f;
                    margin-top: 30px;
                    font-weight: bold;
                }}

                /* Quote Block */
                blockquote {{
                    background-color: #fff8e1;
                    border-left: 5px solid #ffc107;
                    margin: 20px 0;
                    padding: 20px;
                    border-radius: 8px;
                    color: #665c4b;
                    font-style: italic;
                }}

                /* List Styling */
                ul, ol {{
                    padding-left: 25px;
                    margin-bottom: 20px;
                }}
                
                ol {{
                    list-style-type: decimal;
                    font-weight: bold;
                    color: #b33955;
                }}

                ul {{
                    list-style-type: disc;
                    font-weight: normal;
                    color: var(--text-color);
                    margin-top: 5px;
                }}
                
                li {{
                    margin-bottom: 8px;
                    padding: 5px;
                    border-radius: 5px;
                    transition: background-color 0.2s;
                }}
                
                li:hover {{
                    background-color: #fff0f3;
                }}

                li strong {{
                    color: #b33955;
                    font-weight: 700;
                }}

                /* Highlight Code Blocks */
                code {{
                    background-color: #ffe3e8;
                    color: #d63031;
                    padding: 2px 6px;
                    border-radius: 4px;
                    font-family: inherit; 
                    font-size: 0.95em;
                }}

                /* Status Badges */
                .badge {{
                    display: inline-block;
                    padding: 3px 8px;
                    border-radius: 12px;
                    font-size: 0.75em;
                    font-weight: bold;
                    color: white;
                    margin-left: 8px;
                    vertical-align: middle;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .badge-danger {{ background-color: #ff6b6b; }}
                .badge-warn {{ background-color: #feca57; color: #5c4b1e; }}
                .badge-success {{ background-color: #1dd1a1; }}

                /* Links */
                a {{
                    color: var(--primary-color);
                    text-decoration: none;
                    border-bottom: 1px dotted var(--primary-color);
                    transition: all 0.2s;
                }}
                a:hover {{
                    border-bottom: 1px solid var(--primary-color);
                    background-color: #fff0f3;
                }}

                .footer {{
                    margin-top: 60px;
                    text-align: center;
                    font-size: 0.9em;
                    color: #999;
                    border-top: 1px dashed #ffafbd;
                    padding-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                {html_body}
                <div class="footer">
                    Generated with ❤️ by AI Relationship Analyst Agent © 2025
                </div>
            </div>
        </body>
        </html>
        """

        try:
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"\n\n[System] Report saved successfully.")
            print(f"MD:   {md_path}")
            print(f"HTML: {html_path}")
        except IOError as e:
            print(f"Error saving HTML: {e}")