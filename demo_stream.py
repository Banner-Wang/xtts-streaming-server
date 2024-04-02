import argparse
from datetime import datetime

import gradio as gr
import requests
import base64
import tempfile
import json
import os
import time
from typing import Iterator
import subprocess


def clone_speaker(upload_file, clone_speaker_name, cloned_speaker_names):
    files = {"wav_file": ("reference.wav", open(upload_file, "rb"))}
    embeddings = requests.post(SERVER_URL + "/clone_speaker", files=files).json()
    with open(os.path.join(OUTPUT, "cloned_speakers", clone_speaker_name + ".json"), "w") as fp:
        json.dump(embeddings, fp)
    cloned_speakers[clone_speaker_name] = embeddings
    cloned_speaker_names.append(clone_speaker_name)
    return upload_file, clone_speaker_name, cloned_speaker_names, gr.Dropdown.update(choices=cloned_speaker_names)


def tts(text, speaker_type, speaker_name_studio, speaker_name_custom, lang):
    print(time.localtime(time.time()))
    print("tts begin")
    # embeddings = STUDIO_SPEAKERS[speaker_name_studio] if speaker_type == 'Studio' else cloned_speakers[speaker_name_custom]
    generated_audio = requests.post(
        SERVER_URL + "/tts",
        json={
            "speaker": speaker_name_studio,
            "text": text,
            "language": lang
            # "speaker_embedding": embeddings["speaker_embedding"],
            # "gpt_cond_latent": embeddings["gpt_cond_latent"]

        }
    ).content
    generated_audio_path = os.path.join("demo_outputs", "generated_audios",
                                        next(tempfile._get_candidate_names()) + ".wav")
    print(time.localtime(time.time()))
    print("tts end")
    with open(generated_audio_path, "wb") as fp:
        fp.write(base64.b64decode(generated_audio))
        return fp.name


def tts_stream(text, speaker_type, speaker_name_studio, speaker_name_custom, lang):
    print("DEBUG2")
    start = time.perf_counter()
    speaker = speaker_name_studio if speaker_type == 'Studio' else speaker_name_custom
    res = requests.post(
        SERVER_URL + "/tts_stream",
        json={
            "text": text,
            "language": lang,
            # "speaker_embedding": embeddings["speaker_embedding"],
            # "gpt_cond_latent": embeddings["gpt_cond_latent"]
            "speaker": speaker
        },
        stream=True,
    )
    end = time.perf_counter()
    print(f"Time to make POST: {end - start}s")

    if res.status_code != 200:
        print("Error:", res.text)

    first = True
    for chunk in res.iter_content(chunk_size=512):
        if first:
            end = time.perf_counter()
            print(f"Time to first chunk: {end - start}s")
            first = False
        if chunk:
            end = time.perf_counter()
            yield chunk

    print("⏱️ response.elapsed:", res.elapsed)


def stream_ffplay(audio_stream, output_file, save=True):
    if not save:
        ffplay_cmd = ["ffplay", "-nodisp", "-probesize", "1024", "-autoexit", "-"]
    else:
        print("Saving to ", output_file)
        ffplay_cmd = ["ffmpeg", "-probesize", "1024", "-i", "-", output_file]

    ffplay_proc = subprocess.Popen(ffplay_cmd, stdin=subprocess.PIPE)
    for chunk in audio_stream:
        if chunk is not None:
            ffplay_proc.stdin.write(chunk)

    # close on finish
    ffplay_proc.stdin.close()
    ffplay_proc.wait()


def tts_play(text, speaker_type, speaker_name_studio, speaker_name_custom, lang):
    generated_audio_path = os.path.join("demo_outputs", "generated_audios",
                                        next(tempfile._get_candidate_names()) + ".wav")
    stream_ffplay(
        tts_stream(
            text,
            speaker_type,
            speaker_name_studio,
            speaker_name_custom,
            lang
        ),
        generated_audio_path,
        save=False
    )


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--host", default="localhost", type=str, help="host IP address.")
    parser.add_argument("--port", type=str, help="server port.")
    return parser.parse_args()


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
#         fn=tts_play,
#         inputs=[text, speaker_type, speaker_name_studio, speaker_name_custom, lang],
#         outputs=[generated_audio],
#     )
#
#     tts_button.click(
#         fn=tts_stream,
#         inputs=[text, speaker_type, speaker_name_studio, speaker_name_custom, lang],
#         outputs=[generated_audio],
#     )

if __name__ == "__main__":
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

    speaker_type = "Studio"
    speaker_name_studio = "Asya Anara"
    speaker_name_custom = []
    lang = "en"

    speaker = speaker_name_studio
    cost_time_all, i = 0, 0
    for text in jokes:
        res = requests.post(
            SERVER_URL + "/tts_stream",
            json={
                "text": text,
                "language": lang,
                "speaker": speaker
            },
            stream=True,
        )
        if res.status_code != 200:
            print("Error:", res.text)

        times = []
        for chunk in res.iter_content(chunk_size=512):
            if chunk:
                current_time = time.time()
                # print(chunk)
                times.append(current_time)
        cost_time = times[-1] - times[0]
        print(f"cost time: {cost_time}")
        i += 1
        cost_time_all += cost_time
    cost_time_avg = cost_time_all / i
    print(f"cost time avg: {cost_time_avg}")
