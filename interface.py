import gradio as gr
from functionality import main
from books_data import BOOKS

genres = ["All"] + sorted(set(b["genre"] for b in BOOKS))
languages = ["All"] + sorted(set(b["language"] for b in BOOKS))

with gr.Blocks() as demo:
    query = gr.Textbox(label="Your query", autofocus=True, placeholder="Type your query here...")
    with gr.Row():
        genre = gr.Dropdown(choices=genres, value="All", label="Genre")
        language = gr.Dropdown(choices=languages, value="All", label="Language")
    with gr.Row():
        min_year = gr.Slider(minimum=1800, maximum=2025, value=1800, step=1, label="Published after (year)")
        min_rating = gr.Slider(minimum=1.0, maximum=5.0, value=1.0, step=0.1, label="Minimum rating")
    award_winner_only = gr.Checkbox(value=False, label="Award winners only")
    with gr.Row():
        submit_btn = gr.Button("Submit", variant="primary")
        clear_btn = gr.ClearButton([query, genre, language, min_year, min_rating, award_winner_only])
    output = gr.Dataframe(label="Results")

    inputs = [query, genre, language, min_year, min_rating, award_winner_only]
    submit_btn.click(fn=main, inputs=inputs, outputs=output)
    demo.load(fn=main, inputs=inputs, outputs=output)

demo.launch(server_name="127.0.0.1", server_port=7900)
