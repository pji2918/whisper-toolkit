#!/usr/bin/env python

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
    input: list[str], output: str, model: str, device: str.
    """
    parser = argparse.ArgumentParser(description="A wrapper for OpenAI Whisper.")
    parser.add_argument(
        "-o",
        "--output",
        help='Specifies output folder. if not provided, it uses "outputs"',
        default="outputs",
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
    parser.add_argument(
        "input",
        metavar="INPUTS",
        nargs="*",
        default="inputs",
        help='Specifies output files/folders. if not provided, it uses "inputs".',
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
    try:
        """
        Entrypoint of this python code.
        """
        warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)
        args: argparse.Namespace = get_args()

        flist: list[Path] = []

        for f in args.input:
            if Path(f).is_dir():
                for i in Path(f).iterdir():
                    if i.is_file() and "README" not in i.name:
                        flist.append(i)
            elif Path(f).is_file():
                flist.append(Path(f))

        Path(args.output).joinpath("json").mkdir(exist_ok=True, parents=True)
        Path(args.output).joinpath("srt").mkdir(exist_ok=True, parents=True)

        if args.device == "auto":
            dev: torch.device = get_available_device()
        else:
            dev = torch.device(args.device)

        print(f"Configuring model with {dev.type}...")
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
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
