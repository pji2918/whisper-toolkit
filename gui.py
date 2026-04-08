import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk


class WhisperToolkitGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Whisper Toolkit")
        self.root.geometry("900x600")
        self.root.minsize(760, 480)

        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.progress_value = tk.IntVar(value=0)
        self.is_running = False

        self._build_ui()

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=16)
        container.pack(fill="both", expand=True)

        input_frame = ttk.LabelFrame(container, text="Input", padding=12)
        input_frame.pack(fill="x", pady=(0, 10))

        input_entry = ttk.Entry(input_frame, textvariable=self.input_path)
        input_entry.pack(side="left", fill="x", expand=True)

        input_button = ttk.Button(
            input_frame, text="파일 선택", command=self.select_input_file
        )
        input_button.pack(side="left", padx=(8, 0))

        output_frame = ttk.LabelFrame(container, text="Output", padding=12)
        output_frame.pack(fill="x", pady=(0, 10))

        output_entry = ttk.Entry(output_frame, textvariable=self.output_path)
        output_entry.pack(side="left", fill="x", expand=True)

        output_button = ttk.Button(
            output_frame, text="폴더 선택", command=self.select_output_dir
        )
        output_button.pack(side="left", padx=(8, 0))

        progress_frame = ttk.LabelFrame(container, text="Progress", padding=12)
        progress_frame.pack(fill="x", pady=(0, 10))

        self.progressbar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_value,
            mode="determinate",
            maximum=100,
        )
        self.progressbar.pack(fill="x")

        self.progress_label = ttk.Label(progress_frame, text="0%")
        self.progress_label.pack(anchor="e", pady=(6, 0))

        button_frame = ttk.Frame(container)
        button_frame.pack(fill="x", pady=(0, 10))

        self.start_button = ttk.Button(
            button_frame, text="시작", command=self.start_process
        )
        self.start_button.pack(side="left")

        clear_button = ttk.Button(
            button_frame, text="로그 지우기", command=self.clear_log
        )
        clear_button.pack(side="left", padx=(8, 0))

        log_frame = ttk.LabelFrame(container, text="Log", padding=12)
        log_frame.pack(fill="both", expand=True)

        self.log_text = scrolledtext.ScrolledText(
            log_frame, height=14, state="disabled", wrap="word"
        )
        self.log_text.pack(fill="both", expand=True)

        self.add_log("프로그램이 시작되었습니다.")

    def select_input_file(self) -> None:
        file_path = filedialog.askopenfilename(
            title="입력 파일 선택",
            filetypes=[
                ("Audio/Video", "*.wav *.mp3 *.m4a *.flac *.mp4 *.mkv"),
                ("All Files", "*.*"),
            ],
        )
        if file_path:
            self.input_path.set(file_path)
            self.add_log(f"입력 파일 선택: {file_path}")

    def select_output_dir(self) -> None:
        dir_path = filedialog.askdirectory(title="출력 폴더 선택")
        if dir_path:
            self.output_path.set(dir_path)
            self.add_log(f"출력 폴더 선택: {dir_path}")

    def clear_log(self) -> None:
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", tk.END)
        self.log_text.configure(state="disabled")
        self.add_log("로그를 초기화했습니다.")

    def add_log(self, message: str) -> None:
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state="disabled")

    def start_process(self) -> None:
        if self.is_running:
            self.add_log("이미 작업이 실행 중입니다.")
            return

        if not self.input_path.get().strip():
            self.add_log("입력 파일을 먼저 선택해 주세요.")
            return

        if not self.output_path.get().strip():
            self.add_log("출력 폴더를 먼저 선택해 주세요.")
            return

        self.is_running = True
        self.start_button.configure(state="disabled")
        self.progress_value.set(0)
        self.progress_label.configure(text="0%")

        self.add_log("작업을 시작합니다.")
        self._run_progress_step()

    def _run_progress_step(self) -> None:
        value = self.progress_value.get()
        if value >= 100:
            self.progress_label.configure(text="100%")
            self.add_log("작업이 완료되었습니다.")
            self.start_button.configure(state="normal")
            self.is_running = False
            return

        next_value = value + 5
        self.progress_value.set(next_value)
        self.progress_label.configure(text=f"{next_value}%")
        self.add_log(f"진행률: {next_value}%")

        self.root.after(150, self._run_progress_step)


def main() -> None:
    root = tk.Tk()
    app = WhisperToolkitGUI(root)
    _ = app
    root.mainloop()


if __name__ == "__main__":
    main()
