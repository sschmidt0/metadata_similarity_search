import gradio as gr
from functionality import main

interface = gr.Interface(
    fn=main,
    inputs=[
        gr.Textbox(label="Your query", autofocus=True, placeholder="Type your query here..."),
        gr.Textbox(label="Metadata"),
    ],
    outputs=gr.Dataframe(label="Results"),
)



interface.launch(server_name="127.0.0.1", server_port= 7900)

