import streamlit as st
import google.generativeai as genai
import PIL.Image

# ================= 配置區 (Configuration) =================
# 1. 這裡填入你的 API Key (請保留你原本那串 AIza...)
MY_API_KEY = "AIzaSyDYhvUcK1gq0J75ejGD_qWnyquYK1Cwqig" 

# 2. 付款連結 (目前暫時設為 Google，之後申請好 Stripe 再來這裡換)
PAYMENT_URL = "https://xuan13.gumroad.com/l/tcosqe"

# 3. 解鎖密碼 (設定為你想要的密碼)
VIP_PASSWORD = "5168"
# ========================================================

# 設定頁面
st.set_page_config(page_title="AI 面相財運分析", page_icon="🔮")

# 設定 API Key
try:
    # 自動去除可能誤複製的空白
    genai.configure(api_key=MY_API_KEY.strip()) 
    model = genai.GenerativeModel('gemini-flash-latest')
except:
    st.error("API Key 設定有誤，請檢查代碼。")

# --- 側邊欄 ---
with st.sidebar:
    st.header("🔮 關於大師")
    st.write("本工具採用最新 AI 視覺模型，結合傳統面相學數據庫。")
    st.info("💡 準確率說明：分析結果僅供娛樂與參考，命運掌握在自己手中。")

# --- 主頁面 ---
st.title("🔮 AI 面相財運探測器")
st.write("上傳照片，AI 將解析你的**潛在身價**與**近期機遇**。")

# 上傳區
uploaded_file = st.file_uploader("請上傳一張清晰的正面照...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = PIL.Image.open(uploaded_file)
    st.image(image, caption='已上傳照片', use_column_width=True)

    if st.button("🔍 開始分析面相"):
        with st.spinner('🔮 大師正在感應天庭與地閣...'):
            try:
                # 簡化版 Prompt
                prompt = """
                你是一位面相大師。請分析這張照片。
                請嚴格用【】符號分段。
                
                第一段公開內容：
                【整體氣場】：一句話形容。
                【性格亮點】：一個優點。
                
                第二段隱藏內容（請寫得非常誘人）：
                【財富運勢】：未來的賺錢機會。
                【貴人方位】：誰是貴人。
                【大師建議】：具體建議。
                """
                
                response = model.generate_content([prompt, image])
                st.session_state['result'] = response.text
                st.session_state['analyzed'] = True
            except Exception as e:
                st.error(f"分析失敗：{e}")

# --- 顯示結果邏輯 ---
if st.session_state.get('analyzed'):
    full_text = st.session_state['result']
    
    # 嘗試切割文字
    try:
        parts = full_text.split("【財富運勢】")
        public_part = parts[0]
        vip_part = "【財富運勢】" + parts[1] if len(parts) > 1 else full_text
    except:
        public_part = full_text[:100] + "..."
        vip_part = full_text
    
    # 1. 顯示免費部分
    st.success("✅ 分析完成！")
    st.subheader("🔓 免費預覽")
    st.write(public_part)
    
    st.divider()
    
    # 2. VIP 鎖定區
    st.subheader("🔒 VIP 深度報告")
    
    # 檢查是否已解鎖
    if st.session_state.get('is_vip'):
        st.balloons()
        st.write(vip_part)
        st.info("感謝您的支持，祝您財源廣進！")
    else:
        # 鎖定狀態
        st.warning("⚠️ 檢測到『下半年財運』有重大訊號，內容已被鎖定。")
        st.write("💰 解鎖後查看：**財富爆發點、貴人方位、避坑指南**")
        
        col1, col2 = st.columns(2)
        
        # 按鈕 1: 去付款
        with col1:
            st.link_button("👉 點此支付 $99 獲取解鎖碼", PAYMENT_URL)
        
        # 按鈕 2: 輸入密碼
        with col2:
            input_code = st.text_input("輸入解鎖碼 (VIP Code)", placeholder="例如：5168")
            if st.button("🔓 確認解鎖"):
                if input_code == VIP_PASSWORD:
                    st.session_state['is_vip'] = True
                    st.rerun()
                else:
                    st.error("❌ 密碼錯誤，請確認或是重新支付。")
