---
name: whisper-toolkit-usage
description: Explain how to use main.py in whisper-toolkit. Use this skill whenever the user requests media transcription, asks how to run transcription from the CLI, asks about options, asks about input/output path behavior, or wants runnable command examples.
license: MIT
metadata:
    author: pji2918
compatibility: Requires `uv` & Python 3.13.
---

# Whisper model wrapper
This repository provides `whisper-toolkit`, a wrapper around OpenAI Whisper (an audio transcription model).
## Prerequisites
You will need `uv`.  
Run this:
```bash
uv --version
```
If it prints text like `uv 0.11.6`, uv is installed.  
If it prints text like `uv: command not found`, uv is not installed. See `references/uv.md` to install.

If `uv` is installed, run `uv sync --no-dev` to install dependencies. Python 3.13 will be installed in this step.
## Command guide
This is the help message from `uv run main.py --help`.
```bash
main.py [-h] [-o OUTPUT] [-m MODEL] [-d DEVICE] [--json JSON] [INPUTS ...]
```
### `--json JSON`: string
You can use this option to provide parameters in JSON format. When this option is used, the output format will also be JSON.  
If you use this option, other options passed on the CLI may be ignored.
### `-o OUTPUT`: string
Specifies the output folder. This option can be used only once.  
If not provided, it defaults to `outputs`.
### `-m MODEL`: string
Specifies which model is used for inference.  
If not provided, it defaults to `turbo`.

Possible values are described in `references/models.md`.
### `-d DEVICE`: string
Specifies which device (CPU, GPU, etc.) is used for inference (in `torch.device` format).  
If not provided, it defaults to `auto`. It is not recommended to change this option.
### `INPUTS ...`: string[]
Specifies input files/folders.  
If not provided, it defaults to the `inputs` folder.
## Using JSON mode
If you are familiar with JSON, you can pass parameters in JSON (and receive JSON output).

Create an object and pass option names as keys with correctly typed values.

Example:
```json
{
    "input": ["test.opus", "videos/"],
    "output": "output_folder"
}
```

Most shells do not accept multi-line JSON. You can pass JSON like this:
```bash
uv run main.py --json '{"input": ["test.opus", "videos/"], "output": "output_folder"}'
```

The output will be JSON like this:
```json
{
    "files": [
        {
            "name": "test.opus",
            "success": true,
            "elapsedTime": 20.33175520900022,
            "outputPath": "outputs/srt/test.srt"
        }
    ],
    "model": "turbo"
}
```
You can use this JSON to report the result to the user like this:
```markdown
<!-- Round down to 2 decimal places. -->
Transcription succeeded for file "test.opus" in 20.33 seconds.

The caption file is now available at "outputs/srt/test.srt".

Do you need any other help?
```

Or another example:

```json
{
    "files": [
        {
            "name": "test.opus",
            "success": true,
            "elapsedTime": 20.33175520900022,
            "outputPath": "outputs/srt/test.srt"
        },
        {
            "name": "test2.mkv",
            "success": true,
            "elapsedTime": 11.33175520900022,
            "outputPath": "outputs/srt/test2.srt"
        }
    ],
    "model": "turbo"
}
```
You can use this JSON to report the result to the user like this:
```markdown
<!-- Round down to 2 decimal places. -->
<!-- elapsed time: 20.33 + 11.33 = 31.66 -->
Transcription succeeded for files "test.opus" and "test2.mkv" in 31.66 seconds.

Caption files are now available at "outputs/srt/test.srt" and "outputs/srt/test2.srt".

Do you need any other help?
```

## Examples
Transcribes all media files in the `inputs` folder to the `outputs/` folder.
```bash
uv run main.py
```
Transcribes `test.mkv` to the `subtitles/` folder.
```bash
uv run main.py --json '{"input": ["test.mkv"], "output": "subtitles/"}'
```
Transcribes all media files in the `test` folder to the `subtitles/` folder.
```bash
uv run main.py --json '{"input": ["test/"], "output": "subtitles/"}'
```
Transcribes all media files in the `test` folder and `test.opus` to the `subtitles/` folder.
```bash
uv run main.py --json '{"input": ["test", "test.opus"], "output": "subtitles/"}'
```
## Troubleshooting
If you have any problems, see `references/troubleshoot.md`.