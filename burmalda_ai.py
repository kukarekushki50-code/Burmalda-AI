import threading
import customtkinter as ctk
import requests

# Настройки темы
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class BurmaldaAIApp(ctk.CTk):

  def __init__(self):
    super().__init__()

    self.title("Burmalda AI — Powered by DeepSeek")
    self.geometry("700x650")

    # Переменная для API ключа
    self.api_key = ""

    # --- Верхняя панель (Ввод API Key) ---
    self.top_frame = ctk.CTkFrame(self)
    self.top_frame.pack(pady=10, padx=10, fill="x")

    self.key_label = ctk.CTkLabel(
        self.top_frame, text="DeepSeek API Key:", font=("Arial", 12, "bold")
    )
    self.key_label.pack(side="left", padx=10)

    self.key_entry = ctk.CTkEntry(
        self.top_frame,
        placeholder_text="sk-...",
        show="*",
        width=350,
    )
    self.key_entry.pack(side="left", padx=5, fill="x", expand=True)

    # --- Окно чата ---
    self.chat_history = ctk.CTkTextbox(
        self, font=("Segoe UI", 13), wrap="word"
    )
    self.chat_history.pack(pady=10, padx=10, fill="both", expand=True)
    self.chat_history.insert(
        "end",
        "😎 **Burmalda AI готова к работе!**\nВведи свой DeepSeek API Key наверх"
        " и пиши запрос ниже.\n"
        + "—" * 40
        + "\n\n",
    )
    self.chat_history.configure(state="disabled")

    # --- Нижняя панель (Ввод сообщения и кнопка) ---
    self.bottom_frame = ctk.CTkFrame(self)
    self.bottom_frame.pack(pady=10, padx=10, fill="x")

    self.user_input = ctk.CTkEntry(
        self.bottom_frame,
        placeholder_text="Напиши что-нибудь суровое...",
        font=("Arial", 13),
    )
    self.user_input.pack(
        side="left", padx=10, pady=10, fill="x", expand=True
    )
    self.user_input.bind("<Return>", lambda event: self.send_message())

    self.send_button = ctk.CTkButton(
        self.bottom_frame,
        text="Отправить",
        font=("Arial", 12, "bold"),
        command=self.send_message,
    )
    self.send_button.pack(side="right", padx=10, pady=10)

  def append_text(self, text):
    self.chat_history.configure(state="normal")
    self.chat_history.insert("end", text)
    self.chat_history.see("end")
    self.chat_history.configure(state="disabled")

  def send_message(self):
    prompt = self.user_input.get().strip()
    api_key = self.key_entry.get().strip()

    if not api_key:
      self.append_text("❌ Ошибка: Введи API Key от DeepSeek!\n\n")
      return

    if not prompt:
      return

    self.append_text(f"Я: {prompt}\n")
    self.user_input.delete(0, "end")
    self.send_button.configure(state="disabled")

    # Запуск запроса в отдельном потоке, чтобы интерфейс не зависал
    threading.Thread(
        target=self.get_ai_response, args=(api_key, prompt), daemon=True
    ).start()

  def get_ai_response(self, api_key, prompt):
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Ты — Burmalda AI, дерзкий, но крайне умный и полезный"
                    " ассистент."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "stream": False,
    }

    try:
      response = requests.post(url, json=data, headers=headers, timeout=30)
      if response.status_code == 200:
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        self.append_text(f"Burmalda AI:\n{reply}\n\n" + "—" * 40 + "\n\n")
      else:
        self.append_text(
            f"❌ Ошибка API ({response.status_code}): {response.text}\n\n"
        )
    except Exception as e:
      self.append_text(f"❌ Ошибка подключения: {str(e)}\n\n")
    finally:
      self.send_button.configure(state="normal")


if __name__ == "__main__":
  app = BurmaldaAIApp()
  app.mainloop()