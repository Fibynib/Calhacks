from pathlib import Path
from typing import Any, Dict, List
from urllib.request import urlretrieve


def download_file(url: str) -> Path:
    example_dirpath = Path(__file__).parent
    data_dirpath = example_dirpath / "data"
    data_dirpath.mkdir(exist_ok=True)
    filepath = data_dirpath / Path(url).name
    urlretrieve(url, filepath)
    return filepath
# def print_emotions(emotions: List[Dict[str, Any]]) -> None:
#     emotion_map = {e["name"]: e["score"] for e in emotions}
#     for emotion in ["Joy", "Sadness", "Anger"]:
#         print(f"- {emotion}: {emotion_map[emotion]:4f}")
def print_emotions(emotions: List[Dict[str, Any]]) -> None:
    emotion_map = {e["score"]: e["name"] for e in emotions}
    scores = list(emotion_map.keys())
    scores.sort(reverse=True)
    for i in range(5):
        print(f"- {emotion_map[scores[i]]}: {scores[i]:4f}")









