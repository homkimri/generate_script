import streamlit as st
from utils import generate_script

# 页面标题
st.title("🎬 视频脚本生成器")
# 页面侧边栏
with st.sidebar:
    openai_api_key = st.text_input("请输入OpenAI API密钥：",type="password")
    st.markdown("[获取OpenAI API密钥](https://platform.openai.com/account/api-keys)")
# 主体输入框
subject = st.text_input("💡 请输入视频的主题")
# 时长输入框
video_lenght = st.number_input("⏱️ 请输入视频的大致时长（单位：分钟）",min_value=0.1,step=0.1)
# 模型创造力大小拖动条
creativity = st.slider("✨ 请输入视频脚本的创造力（数字小说明更严谨，数字大说明更多样）",min_value=0.0,
                       max_value=1.0,value=0.5,step=0.1)
# 提交按钮
submit = st.button("生成脚本")
# 点击提交按钮，但没输API 密钥，提示用户，程序结束请求的提交
if submit and not openai_api_key:
    st.info("请输入您的 API 密钥")
    st.stop()
# 点击提交按钮，但没主题，提示用户，程序结束请求的提交
if submit and not subject:
    st.info("请输入视频的主题")
    st.stop()
# 点击提交按钮，但没长度小于 0.1分钟，提示用户，程序结束请求的提交
if submit and not video_lenght >= 0.1:
    st.info("视频长度需要大于或等于0.1分钟")
    st.stop()
# 所以前置条件都已满足
if submit:
    with st.spinner("AI正在思考中，请稍等..."):
        search_result,title,script = generate_script(subject,video_lenght,creativity,openai_api_key)
    st.success("视频脚本已生成！")
    st.subheader("🔥 标题：")
    st.write(title)
    st.subheader("📝 视频脚本：")
    st.write(script)
    with st.expander("维基百科搜索结果 👀"):
        st.info(search_result)