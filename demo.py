import argparse
import time

import gradio as gr
import requests
import base64
import tempfile
import json
import os


def clone_speaker(upload_file, clone_speaker_name, cloned_speaker_names):
    files = {"wav_file": ("reference.wav", open(upload_file, "rb"))}
    embeddings = requests.post(SERVER_URL + "/clone_speaker", files=files).json()
    with open(os.path.join(OUTPUT, "cloned_speakers", clone_speaker_name + ".json"), "w") as fp:
        json.dump(embeddings, fp)
    cloned_speakers[clone_speaker_name] = embeddings
    cloned_speaker_names.append(clone_speaker_name)
    return upload_file, clone_speaker_name, cloned_speaker_names, gr.Dropdown.update(choices=cloned_speaker_names)


def tts(text, speaker_name_studio, lang):
    # embeddings = STUDIO_SPEAKERS[speaker_name_studio] if speaker_type == 'Studio' else cloned_speakers[
    #     speaker_name_custom]
    start_time = time.time()
    generated_audio = requests.post(
        SERVER_URL + "/tts",
        json={
            "text": text,
            "language": lang,
            "speaker": speaker_name_studio
        }
    ).content
    rsp_time = time.time()
    rsp_cost_time = rsp_time - start_time
    generated_audio_path = os.path.join("demo_outputs", "generated_audios",
                                        next(tempfile._get_candidate_names()) + ".wav")
    with open(generated_audio_path, "wb") as fp:
        fp.write(base64.b64decode(generated_audio))
        wav_save_cost_time = time.time() - rsp_time
        print(f"fname: {fp.name} rsp_cost_time: {rsp_cost_time} ,  wav_save_cost_time: {wav_save_cost_time} ")
        return fp.name, rsp_cost_time, wav_save_cost_time


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--host", default="localhost", type=str, help="host IP address.")
    parser.add_argument("--port", type=str, help="server port.")
    return parser.parse_args()


jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "Parallel lines have so much in common. It's a shame they'll never meet.",
    "I'm reading a book on anti-gravity. It's impossible to put down!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Why did the math book look sad? Because it had too many problems.",
    "Why did the bicycle fall over? Because it was two-tired!",
    "Why was the math book sad? It had too many problems.",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "What do you call fake spaghetti? An impasta!",
    "Why did the golfer bring two pairs of pants? In case he got a hole in one!",
    "Why don't skeletons fight each other? They don't have the guts.",
    "What do you get when you cross a snowman and a vampire? Frostbite!",
    "Why did the scarecrow become a successful neurosurgeon? Because he was outstanding in his field!",
    "Why did the chicken join a band? Because it had the drumsticks!",
    "Why was the math book sad? It had too many problems.",
    "What do you call a fish wearing a bowtie? SoFISHticated!",
    "Why don't skeletons fight each other? They don't have the guts.",
    "Why couldn't the bicycle stand up by itself? It was two-tired!",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "What do you call fake spaghetti? An impasta!",
    "Why did the golfer bring two pairs of pants? In case he got a hole in one!",
    "Why don't scientists trust atoms? Because they make up everything!",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "Parallel lines have so much in common. It's a shame they'll never meet.",
    "I'm reading a book on anti-gravity. It's impossible to put down!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Why did the math book look sad? Because it had too many problems.",
    "Why did the bicycle fall over? Because it was two-tired!",
    "Why was the math book sad? It had too many problems.",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "What do you call fake spaghetti? An impasta!",
    "Why did the golfer bring two pairs of pants? In case he got a hole in one!",
    "Why don't skeletons fight each other? They don't have the guts.",
    "What do you get when you cross a snowman and a vampire? Frostbite!",
    "Why did the scarecrow become a successful neurosurgeon? Because he was outstanding in his field!",
    "Why did the chicken join a band? Because it had the drumsticks!",
    "Why was the math book sad? It had too many problems.",
    "What do you call a fish wearing a bowtie? SoFISHticated!",
    "Why don't skeletons fight each other? They don't have the guts.",
    "Why couldn't the bicycle stand up by itself? It was two-tired!",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "What do you call fake spaghetti? An impasta!",
    "Why did the golfer bring two pairs of pants? In case he got a hole in one!",
    "Why don't scientists trust atoms? Because they make up everything!",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "Parallel lines have so much in common. It's a shame they'll never meet.",
    "I'm reading a book on anti-gravity. It's impossible to put down!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Why did the math book look sad? Because it had too many problems.",
    "Why did the bicycle fall over? Because it was two-tired!",
    "Why was the math book sad? It had too many problems.",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "What do you call fake spaghetti? An impasta!",
    "Why did the golfer bring two pairs of pants? In case he got a hole in one!",
    "Why don't skeletons fight each other? They don't have the guts.",
    "What do you get when you cross a snowman and a vampire? Frostbite!",
    "Why did the scarecrow become a successful neurosurgeon? Because he was outstanding in his field!",
    "Why did the chicken join a band? Because it had the drumsticks!",
    "Why was the math book sad? It had too many problems.",
    "What do you call a fish wearing a bowtie? SoFISHticated!",
    "Why don't skeletons fight each other? They don't have the guts.",
    "Why couldn't the bicycle stand up by itself? It was two-tired!",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "What do you call fake spaghetti? An impasta!",
    "Why did the golfer bring two pairs of pants? In case he got a hole in one!",
    "Why don't scientists trust atoms? Because they make up everything!",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "Parallel lines have so much in common. It's a shame they'll never meet.",
    "I'm reading a book on anti-gravity. It's impossible to put down!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Why did the math book look sad? Because it had too many problems.",
    "Why did the bicycle fall over? Because it was two-tired!",
    "Why was the math book sad? It had too many problems.",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "What do you call fake spaghetti? An impasta!",
    "Why did the golfer bring two pairs of pants? In case he got a hole in one!",
    "Why don't skeletons fight each other? They don't have the guts.",
    "What do you get when you cross a snowman and a vampire? Frostbite!",
    "Why did the scarecrow become a successful neurosurgeon? Because he was outstanding in his field!",
    "Why did the chicken join a band? Because it had the drumsticks!",
    "Why was the math book sad? It had too many problems.",
    "What do you call a fish wearing a bowtie? SoFISHticated!",
    "Why don't skeletons fight each other? They don't have the guts.",
    "Why couldn't the bicycle stand up by itself? It was two-tired!",
    "Why did the tomato turn red? Because it saw the salad dressing!"]

args = get_args()
SERVER_URL = f'http://{args.host}:{args.port}'
OUTPUT = "./demo_outputs"
cloned_speakers = {}

print("Preparing file structure...")
if not os.path.exists(OUTPUT):
    os.mkdir(OUTPUT)
    os.mkdir(os.path.join(OUTPUT, "cloned_speakers"))
    os.mkdir(os.path.join(OUTPUT, "generated_audios"))
elif os.path.exists(os.path.join(OUTPUT, "cloned_speakers")):
    print("Loading existing cloned speakers...")
    for file in os.listdir(os.path.join(OUTPUT, "cloned_speakers")):
        if file.endswith(".json"):
            with open(os.path.join(OUTPUT, "cloned_speakers", file), "r") as fp:
                cloned_speakers[file[:-5]] = json.load(fp)
    print("Available cloned speakers:", ", ".join(cloned_speakers.keys()))

try:
    print("Getting metadata from server ...")
    LANUGAGES = requests.get(SERVER_URL + "/languages").json()
    print("Available languages:", ", ".join(LANUGAGES))
    STUDIO_SPEAKERS = requests.get(SERVER_URL + "/studio_speakers").json()
    print("Available studio speakers:", ", ".join(STUDIO_SPEAKERS.keys()))
except:
    raise Exception("Please make sure the server is running first.")

# with gr.Blocks() as demo:
#     cloned_speaker_names = gr.State(list(cloned_speakers.keys()))
#     with gr.Tab("TTS"):
#         with gr.Column() as row4:
#             with gr.Row() as col4:
#                 speaker_name_studio = gr.Dropdown(
#                     label="Studio speaker",
#                     choices=STUDIO_SPEAKERS.keys(),
#                     value="Asya Anara" if "Asya Anara" in STUDIO_SPEAKERS.keys() else None,
#                 )
#                 speaker_name_custom = gr.Dropdown(
#                     label="Cloned speaker",
#                     choices=cloned_speaker_names.value,
#                     value=cloned_speaker_names.value[0] if len(cloned_speaker_names.value) != 0 else None,
#                 )
#             speaker_type = gr.Dropdown(label="Speaker type", choices=["Studio", "Cloned"], value="Studio")
#         with gr.Column() as col2:
#             lang = gr.Dropdown(label="Language", choices=LANUGAGES, value="en")
#             text = gr.Textbox(label="text", value="A quick brown fox jumps over the lazy dog.")
#             tts_button = gr.Button(value="TTS")
#         with gr.Column() as col3:
#             generated_audio = gr.Audio(label="Generated audio", autoplay=True)
#     with gr.Tab("Clone a new speaker"):
#         with gr.Column() as col1:
#             upload_file = gr.Audio(label="Upload reference audio", type="filepath")
#             clone_speaker_name = gr.Textbox(label="Speaker name", value="default_speaker")
#             clone_button = gr.Button(value="Clone speaker")
#
#     clone_button.click(
#         fn=clone_speaker,
#         inputs=[upload_file, clone_speaker_name, cloned_speaker_names],
#         outputs=[upload_file, clone_speaker_name, cloned_speaker_names, speaker_name_custom],
#     )
#
#     tts_button.click(
#         fn=tts,
#         inputs=[text, speaker_name_studio, lang],
#         outputs=[generated_audio],
#     )

rsp_cost_all, wav_save_cost_all, i = 0, 0, 0
for text in jokes:
    # speaker_type = "Studio"
    speaker_name_studio = "Asya Anara"
    speaker_name_custom = []
    lang = "en"
    fname, rsp_cost_time, wav_save_cost_time = tts(text, speaker_name_studio, lang)
    rsp_cost_all += rsp_cost_time
    wav_save_cost_all += wav_save_cost_time
    i += 1
rsp_cost_avg = rsp_cost_all / i
wav_save_cost_avg = wav_save_cost_all / i
print(f"Average RSP cost: {rsp_cost_avg:.2f} seconds")
print(f"Average WAV save cost: {wav_save_cost_avg:.2f} seconds")
