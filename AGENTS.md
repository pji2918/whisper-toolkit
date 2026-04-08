# Whisper-toolkit

## About

해당 프로젝트는 [OpenAI Whisper](github.com/openai/whisper)를 사용자 친화적으로 만드는 Wrapper입니다.

## Run

- CLI
    - `uv run main.py INPUTS`
- GUI
    - `uv run gui.py`

## Code styles

1. 주석/Docstring은 영어로 작성할 것.

2. 변수/함수 선언 시 Type을 명시할 것.

    ```python
    # Example
    def add(a: int, b: int) -> int:
        return a + b

    variable: int = 5
    ```

3. 함수에는 Docstring(Google 스타일)을 작성할 것.

    ```python
    # Example
    def power(base: int, exp: int) -> int:
        """
        Returns base ** exp.

        Args:
            base (int): base.
            exp (int): exp.

        Returns:
            int: base ** exp.

        Examples:
            >>> power(2, 2)
                4
        """
        return base ** exp
    ```

## General rules

1. 작업 후에는 `ty check && ruff check`를 통해 문법 문제를 검사할 것.
2. _추후 추가 예정..._
