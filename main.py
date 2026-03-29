from tqdm.rich import tqdm
import whisper
import whisper.utils
import os
import json
import warnings
from pathlib import Path
from tqdm import TqdmExperimentalWarning


def main():
    warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)
    flist = [
        f for f in Path("./inputs").iterdir() if f.is_file() and "README" not in f.name
    ]

    print("Configuring model...", end=" ")
    model = whisper.load_model("turbo")

    for idx, filePath in enumerate(tqdm(flist, position=1)):
        print(f"Running inference for {filePath.name}... ({idx + 1}/{len(flist)})")
        result = model.transcribe(
            str(filePath.resolve()),
            word_timestamps=True,
            verbose=False,
            fp16=False,
        )

        with open(
            os.path.join("outputs", "json", f"opt{idx + 1}.json"),
            mode="w",
            encoding="utf8",
        ) as f:
            json_str = json.dumps(result, indent=4, ensure_ascii=False)
            f.write(json_str)

        writer = whisper.utils.get_writer(
            "srt",
            os.path.join("outputs", "srt"),
        )
        writer(result, filePath, {})


if __name__ == "__main__":
    main()
