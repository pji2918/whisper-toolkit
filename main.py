import argparse
import json
import os
import time
import warnings
from pathlib import Path

import torch
import whisper
import whisper.utils
from tqdm import TqdmExperimentalWarning
from tqdm.rich import tqdm
from whisper.model import Whisper


def get_args() -> argparse.Namespace:
    """
    Returns arguments that used when launching program.

    Returns:
    argparse.Namespace containing:
    input: str, output: str, model: str, device: str.
    """
    parser = argparse.ArgumentParser(description="A wrapper for OpenAI Whisper.")
    parser.add_argument(
        "-i", "--input", help="Specifies input folder.", default="inputs"
    )
    parser.add_argument(
        "-o", "--output", help="Specifies output folder.", default="outputs"
    )
    parser.add_argument(
        "-m",
        "--model",
        help="Specifies which model used for inference.",
        default="turbo",
    )
    parser.add_argument(
        "-d",
        "--device",
        help="Specifies which device used for inference.",
        default="auto",
    )
    return parser.parse_args()


def get_available_device() -> torch.device:
    """
    Returns suitable torch.device for current hardware.

    Returns:
        torch.device: pytorch-ready device.

    Examples:
    >>> get_available_device() # When using NVIDIA, AMD GPU
        device(type='cuda')
    >>> get_available_device() # When using Apple Silicon
        device(type='mps')
    >>> get_available_device() # When GPU is unavailable
        device(type='cpu')
    """
    dev = str()
    if torch.cuda.is_available():
        dev = "cuda"
    elif torch.backends.mps.is_available():
        dev = "mps"
    else:
        dev = "cpu"
    return torch.device(dev)


def main() -> None:
    """
    Entrypoint for this python code.
    """
    warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)
    args: argparse.Namespace = get_args()

    flist: list[Path] = [
        f for f in Path("./inputs").iterdir() if f.is_file() and "README" not in f.name
    ]

    if args.device == "auto":
        dev = get_available_device()
    else:
        dev = torch.device(args.device)

    print("Configuring model...", end=" ")
    model: Whisper = whisper.load_model(args.model, device=dev)

    for idx, filePath in enumerate(tqdm(flist, position=1)):
        print(f"Running inference for {filePath.name}... ({idx + 1}/{len(flist)})")
        startTime: float = time.perf_counter()
        result = model.transcribe(str(filePath.resolve()), verbose=False)

        with open(
            os.path.join("outputs", "json", f"opt{idx + 1}.json"),
            mode="w",
            encoding="utf8",
        ) as f:
            json_str: str = json.dumps(result, indent=4, ensure_ascii=False)
            f.write(json_str)

        writer = whisper.utils.get_writer(
            "srt",
            os.path.join("outputs", "srt"),
        )
        writer(result, filePath, {})
        print(
            f"File {idx + 1} processing completed. took {time.perf_counter() - startTime:.2f}s"
        )


if __name__ == "__main__":
    main()
