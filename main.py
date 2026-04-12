#!/usr/bin/env python

import argparse
import json
import os
import time
import warnings
from pathlib import Path
from collections.abc import Callable
from typing import Optional

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
    """
    Entrypoint of this python code.
    """
    warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)
    args: argparse.Namespace = get_args()
    process(input=args.input, output=args.output, device=args.device, model=args.model)


def process(
    input: tuple[str] = ("inputs",),
    output: str = "outputs",
    device: str = "auto",
    model: str = "turbo",
    log_callback: Optional[Callable[[str], None]] = None,
    progress_callback: Optional[Callable[[int, int, Path], None]] = None,
    file_status_callback: Optional[Callable[[str, int, int, Path], None]] = None,
) -> int:
    """Runs Whisper transcription for input files.

    Args:
        input (tuple[str]): Input file or directory paths.
        output (str): Output directory path.
        device (str): Inference device name. Uses auto-detection when set to "auto".
        model (str): Whisper model name.
        log_callback (Optional[Callable[[str], None]]): Optional callback for log text.
        progress_callback (Optional[Callable[[int, int, Path], None]]):
            Optional callback for overall progress.
        file_status_callback (Optional[Callable[[str, int, int, Path], None]]):
            Optional callback for per-file status updates.

    Returns:
        int: 0 if processing succeeded, 1 when no input file is found.

    Examples:
        >>> process(input=("inputs",), output="outputs", model="turbo")
        0 # UI output is ignored on this example
    """

    def emit_log(message: str) -> None:
        """Prints and forwards log messages through callback."""
        print(message)
        if log_callback is not None:
            log_callback(message)

    flist: list[Path] = []
    for f in input:
        if Path(f).is_dir():
            for i in Path(f).iterdir():
                if i.is_file() and "README" not in i.name:
                    flist.append(i)
        elif Path(f).is_file():
            flist.append(Path(f))

    if not flist:
        emit_log("No input file was provided.")
        return 1

    Path(output).joinpath("json").mkdir(exist_ok=True, parents=True)
    Path(output).joinpath("srt").mkdir(exist_ok=True, parents=True)

    if device == "auto":
        dev: torch.device = get_available_device()
    else:
        dev = torch.device(device)

    emit_log(f"Configuring model with {dev.type}...")
    whisper_model: Whisper = whisper.load_model(model, device=dev)

    total_files = len(flist)
    for idx, filePath in enumerate(tqdm(flist, position=1), start=1):
        if file_status_callback is not None:
            file_status_callback("start", idx, total_files, filePath)

        emit_log(f"Running inference for {filePath.name}... ({idx}/{total_files})")
        startTime: float = time.perf_counter()
        result = whisper_model.transcribe(str(filePath.resolve()), verbose=False)

        with open(
            os.path.join(output, "json", f"opt{idx}.json"),
            mode="w",
            encoding="utf8",
        ) as f:
            json_str: str = json.dumps(result, indent=4, ensure_ascii=False)
            f.write(json_str)

        writer = whisper.utils.get_writer(
            "srt",
            os.path.join(output, "srt"),
        )
        writer(result, filePath, {})
        emit_log(
            f"File {idx} processing completed. took {time.perf_counter() - startTime:.2f}s"
        )
        if file_status_callback is not None:
            file_status_callback("done", idx, total_files, filePath)
        if progress_callback is not None:
            progress_callback(idx, total_files, filePath)

    return 0


if __name__ == "__main__":
    main()
