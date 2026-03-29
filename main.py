import whisper
import os
import json
from pathlib import Path

import opt2srt


def main():
    flist = [f for f in Path("./inputs").iterdir() if f.is_file()]

    print("Configuring model...", end=" ")
    model = whisper.load_model("turbo")
    print("done.")

    for idx, f in enumerate(flist):
        print("Running inference...", end=" ")
        result = model.transcribe(str(f.resolve()), word_timestamps=True)
        print("done.")

        with open(
            os.path.join("outputs", "json", f"opt{idx + 1}.txt"),
            mode="w",
            encoding="utf8",
        ) as f:
            json_str = json.dumps(result, indent=4, ensure_ascii=False)
            f.write(json_str)

        opt2srt.transcribe_audio(result["segments"], f"opt{idx + 1}.srt")


if __name__ == "__main__":
    main()
