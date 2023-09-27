import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import os
import datetime


def create_text_frame(master):
    text_frame = tk.Frame(master, width=500, height=100)
    text_field = ScrolledText(text_frame, font=("Meiryo UI", 12), height=7, width=55)
    text_field.pack()
    return text_frame, text_field


def create_counter(master):
    counter = tk.Label(master, text=0, width="10", font=("Meiryo UI", 14))
    return counter


def create_send_button(master, command):
    send_button = tk.Button(
        master,
        text="送信",
        width="35",
        pady=5,
        fg="#ffffff",
        bg="#1E88E5",
        relief=tk.FLAT,
        font=("Meiryo UI", 14),
        anchor="center",
        command=command,
    )
    return send_button


def save_and_clear_text(
    target_path: str, text_widget: ScrolledText, timestamp_format: str
):
    template = "**{:" + timestamp_format + "}**\n{}"

    with open(target_path, mode="a", encoding="UTF-8") as f:
        timestamp = datetime.datetime.now()
        body = text_widget.get(0.0, tk.END)
        f.write(template.format(timestamp, body))

    text_widget.delete(0.0, tk.END)


def create_main_window(master, file_path, timestamp_format):
    main_window = tk.Frame(master)

    text_frame, text_field = create_text_frame(main_window)
    text_frame.pack()

    counter_button_frame = tk.Frame(main_window, width=500, height=30)
    counter_button_frame.pack(padx=20, pady=10)
    counter = create_counter(counter_button_frame)
    counter.grid(row=0, column=0)

    def send_button_click():
        # 変数のスコープを犯す(引数でもらっていない変数を処理に使う)という「変な」ことをするので、
        # それ以外の変わったことを極力同じところでしないことで認知負荷を下げる
        return save_and_clear_text(file_path, text_field, timestamp_format)

    send_button = create_send_button(counter_button_frame, send_button_click)
    send_button.grid(row=0, column=1)

    def launch_auto_sync(root, *, period_ms=1000):  # 普通はクラスで実現する
        def one_step():
            text = text_field.get(0.0, tk.END)
            counter["text"] = len(text) - 1
            root.after(period_ms, one_step)

        one_step()

    return main_window, launch_auto_sync


def launch_app(save_file_path: str, timestamp_format: str, *, sync_period_ms=1000):
    root = tk.Tk()
    root.title("フリーメモ")
    root.geometry("600x220")

    main_window, launch_auto_sync = create_main_window(
        root, save_file_path, timestamp_format
    )
    main_window.pack()

    launch_auto_sync(root, period_ms=sync_period_ms)
    root.mainloop()


def main():
    # 平時にいじる部分は一か所にまとめる
    save_dir = f"{os.environ['GoogleDrive']}\\Knowledge\\Zettelkasten\\400_デイリーノート\\410_デイリー"
    file_name = f"{datetime.date.today():%Y-%m-%d}.md"
    file_path = os.path.join(save_dir, file_name)
    timestamp_format = "%H:%M"

    launch_app(file_path, timestamp_format, sync_period_ms=10)


if __name__ == "__main__":
    main()
