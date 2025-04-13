import gradio as gr
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from llm.prompt_tuning import ask_gpt  # Import prompttuning from the llm file

# 初始化聊天历史
def chat_function(user_input, history):
    """处理用户输入，并更新聊天历史"""
    response = ask_gpt(user_input, history)
    history.append((user_input, response))
    return history, ""

# 重新发送上一个问题
def retry_function(history):
    """重新提交上一次的问题"""
    if history:
        last_question = history[-1][0]  # 获取最后一个问题
        return chat_function(last_question, history[:-1])  # 重新发送，不重复存入
    return history, ""

# 创建 Gradio 界面
with gr.Blocks() as demo:
    gr.Markdown("## 📦 AI Supply Chain Assistant")
    
    with gr.Row():
        gr.Markdown("""
        💡 **Task Introduction**
        - Analyze supply chain optimization solutions  
        - Answer **What-if** questions  
        - Provide feasibility analysis based on optimization calculations  
        - Support multiple rounds of interaction, keeping context in mind.  
        """)

    chatbot = gr.Chatbot()  # 使用 Gradio 官方推荐的 Chatbot 组件
    user_input = gr.Textbox(
        placeholder="Type your What-If question here...", 
        label="User Input"
    )

    with gr.Row():
        send_button = gr.Button("🚀 Send")
        retry_button = gr.Button("🔄 Retry")  # 重新发送按钮
        clear_button = gr.Button("🗑️ Clear Chat")

    # 绑定事件：回车发送
    user_input.submit(chat_function, inputs=[user_input, chatbot], outputs=[chatbot, user_input])

    # 绑定按钮事件
    send_button.click(chat_function, inputs=[user_input, chatbot], outputs=[chatbot, user_input])
    retry_button.click(retry_function, inputs=chatbot, outputs=[chatbot, user_input])
    clear_button.click(lambda: [], inputs=[], outputs=chatbot)

# 运行 Gradio 界面
demo.launch()