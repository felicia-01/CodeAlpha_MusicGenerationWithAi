import ipywidgets as widgets
from IPython.display import display, Audio

style_selector = widgets.RadioButtons(
    options=["Jazz", "Classical", "Calm"],
    description="🎼 Style:"
)

duration_selector = widgets.RadioButtons(
    options=[15, 30, 60],
    description="⏱️ Duration:"
)

generate_button = widgets.Button(
    description="Generate & Play",
    icon="music",
    button_style="success"
)

status_box = widgets.VBox()  # Holds multiple outputs

def on_click(b):
    style = style_selector.value.lower()
    duration = duration_selector.value
    filename = f"{style}_output_{np.random.randint(10000)}.mid"  # Unique filename

    out = widgets.Output()
    with out:
        print(f"🎼 Style: {style.capitalize()}")
        print(f"⏱️ Duration: {duration} seconds")
        print("🎶 Generating... Please wait...")
    display(out)
    try:
            generate_music(style, seconds=duration, filename=filename)
            print(f"✅ Music generated: {filename}")
            convert_and_play(filename)  # Assumes this plays and returns Audio widget
    except Exception as e:
            print(f"❌ Error: {str(e)}")



generate_button.on_click(on_click)

# Final UI Layout
ui = widgets.VBox([style_selector, duration_selector, generate_button, status_box])
display(ui)
