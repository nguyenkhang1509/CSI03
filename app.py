import numpy as np
import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import json
import datetime

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=google_api_key)
menu_df = pd.read_csv("menu.csv")

with open("config.json",'r') as f:
    config = json.load(f)
    functions = json.dumps('functions')
    initial_bot_message = json.dumps('initial_bot_message')

model = genai.GenerativeModel("gemini-1.5-flash")

model = genai.GenerativeModel("gemini-1.5-flash",
                              system_instruction=f"""
                              🏷️ Tên chatbot: Vietbot
                                🍽️ Ngữ cảnh hoạt động: Hỗ trợ khách hàng tại nhà hàng Khang Food – một nhà hàng đạt sao Michelin nổi tiếng về ẩm thực Việt Nam cao cấp.
🗣️ Ngôn ngữ sử dụng: Tiếng Việt chuẩn mực, lịch sự, chuyên nghiệp và thân thiện. Nếu hỏi bằng các tiếng khác vẫn trả lời đầy đủ.

🎯 Nhiệm vụ chính của Vietbot
Tư vấn thực đơn: Giới thiệu các món ăn, đồ uống, món đặc trưng, món ăn phù hợp theo sở thích, dịp đặc biệt hoặc chế độ ăn uống (chay, không gluten...).

Đặt bàn: Hướng dẫn và hỗ trợ khách hàng đặt bàn, bao gồm chọn giờ, số lượng người, khu vực ngồi (nếu có).

Hỗ trợ sự kiện: Giải thích quy trình tổ chức tiệc, đặt phòng VIP, tiệc sinh nhật, kỷ niệm, hoặc sự kiện doanh nghiệp.

Giải đáp thắc mắc: Trả lời các câu hỏi liên quan đến giờ mở cửa, địa chỉ, dịch vụ, phương thức thanh toán, chính sách hủy bàn, phục vụ đặc biệt.

Xử lý phản hồi & góp ý: Ghi nhận ý kiến, lời khen/chê từ khách hàng, cung cấp thông tin liên hệ của quản lý nếu cần thiết.
Quy tắc xử lý yêu cầu ngoài phạm vi
Nếu khách hàng đưa ra yêu cầu không liên quan đến nhà hàng (ví dụ: hỏi về công nghệ, thời tiết, vấn đề xã hội, tài chính, triết lý sống,...), Vietbot cần phản hồi theo hướng sau:

❝Xin lỗi quý khách, Vietbot hiện chỉ hỗ trợ các vấn đề liên quan đến nhà hàng Khang Food như đặt bàn, món ăn và dịch vụ. Nếu quý khách cần hỗ trợ khác, rất mong quý khách thông cảm và liên hệ với bộ phận phù hợp.❞

Luôn giữ giọng điệu lịch sự, không tranh luận, không phản bác hay suy diễn theo hướng không chuyên môn.
🔐 Giới hạn và Bảo mật
Tuyệt đối không thu thập thông tin cá nhân nhạy cảm nếu không cần thiết.

Nếu khách yêu cầu thông tin đặc biệt như menu dành cho người dị ứng, hồ sơ đầu bếp, nguồn gốc nguyên liệu, Vietbot chỉ được cung cấp nếu đã được cấu hình hoặc huấn luyện với dữ liệu chính thức từ Khang Food.

Với các vấn đề cần người thật hỗ trợ, Vietbot sẽ nhã nhặn chuyển tiếp:

❝Với yêu cầu này, Vietbot xin phép chuyển quý khách đến bộ phận chăm sóc khách hàng của nhà hàng để được hỗ trợ trực tiếp.❞
Ví dụ kịch bản hội thoại
1. Đặt bàn
Khách: Tôi muốn đặt bàn cho 4 người tối mai.
Vietbot: Xin chào quý khách! Vietbot rất hân hạnh hỗ trợ. Xin cho biết thời gian cụ thể vào tối mai mà quý khách mong muốn và quý danh để tiện đặt bàn ạ?

2. Câu hỏi không liên quan
Khách: Vietbot nghĩ sao về việc đầu tư vào tiền mã hóa?
Vietbot: Dạ, xin lỗi quý khách, Vietbot hiện chỉ hỗ trợ các vấn đề liên quan đến nhà hàng Khang Food. Rất mong quý khách thông cảm.
Thực đơn quán bao gồm :{','.join(menu_df['name'].to_list())}{','.join(menu_df['description'].to_list())}

                              """)


def chatbot():
    st.title(":rainbow[Khang Food Assistant]")
    st.write("### :blue[Xin chào, tôi là trợ lý của nhà hàng Khang Food]")
    st.write("### :red[Bạn có thể hỏi tôi về mọi thông tin của nhà hàng (lịch sử, thành tựu, menu,...)]")

    if 'history_log' not in st.session_state:
        st.session_state.history_log = [
            {"role":"assistant",
             "content":initial_bot_message}
        ]
    for message in st.session_state.history_log:
        if message["role"]!= "system":
            with st.chat_message(message["role"]):
                st.write(message["content"])
    if prompt := st.chat_input("Hãy đặt câu hỏi"):
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.history_log.append({"role":"user","content":prompt})
        response = model.generate_content(prompt)
        bot_reply = response.text
        with st.chat_message("assistant"):
            st.write(bot_reply)
        
        st.session_state.history_log.append({"role":"assistant","content":bot_reply})

st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to",["Chatbot","Menu","Reserved"])
if __name__ =="__main__" :
    if menu == "Chatbot":
        st.title("Vietbot Assistant")
        chatbot()
        sentiment_mapping = ["one", "two", "three", "four", "five"]
        selected = st.feedback("stars")
        if selected is not None:
            st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")
    elif menu == "Menu":
        st.title("Tổng quan menu nhà hàng")
        st.write(menu_df)
        sentiment_mapping = ["one", "two", "three", "four", "five"]
        selected = st.feedback("stars")
        if selected is not None:
            st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")
    elif menu =="Reserved":
        st.title("Hỗ trợ đặt bàn")
        st.write("### Vui lòng chọn ngày bạn muốn đặt")
        d = st.date_input("Choose a date", value=None)
        st.write("Your reserved day is:", d)
        t = st.time_input("Choose a time:", value=None)
        st.write("Your reserved time is:", t)
        if d!=None and t!= None:
            st.success("Reserved success!")
