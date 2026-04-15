# uv
## What is `uv`?
> An extremely fast Python package and project manager, written in Rust.
>
> Astral
## How to install?
First, check your operating system. The installation command is different for each OS.


Run this in your terminal:
```shell
uname
```
If it returns text like `Linux`, your operating system is Linux.

If it returns text like `Darwin`, your operating system is macOS.

If `command not found` is returned, your operating system is Windows.

If it returns text like `GNU` or `FreeBSD`, your operating system may not be supported by `uv`.

Follow the instructions below for your operating system.

When the script returns text like `everything's installed!`, you can move to the next step.

## macOS or Linux
Run this:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
## Windows
Run this:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
