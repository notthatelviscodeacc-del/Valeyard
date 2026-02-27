```python
# project structure:
# pipboy/
# ├── main.py
# ├── config.py
# ├── display/
# │   ├── __init__.py
# │   ├── screen.py
# │   └── screens/
# │       ├── __init__.py
# │       ├── stat_screen.py
# │       ├── inv_screen.py
# │       ├── data_screen.py
# │       ├── map_screen.py
# │       └── radio_screen.py
# ├── handlers/
# │   ├── __init__.py
# │   ├── telegram_handler.py
# │   └── github_handler.py
# └── utils/
#     ├── __init__.py
#     └── logger.py

# ─────────────────────────────────────────────
# config.py
# ─────────────────────────────────────────────

TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_POLL_INTERVAL = 3  # seconds

GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"
GITHUB_REPO = "YOUR_REPO"  # format: "username/repo"
GITHUB_POLL_INTERVAL = 60  # seconds

DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 240
DISPLAY_FPS = 10

PIPBOY_GREEN = (0, 255, 65)
PIPBOY_DARK_GREEN = (0, 180, 45)
PIPBOY_BLACK = (0, 0, 0)
PIPBOY_AMBER = (255, 176, 0)

TABS = ["STAT", "INV", "DATA", "MAP", "RADIO"]
DEFAULT_TAB = "DATA"

# ─────────────────────────────────────────────
# utils/logger.py
# ─────────────────────────────────────────────

import logging
import sys


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger

# ─────────────────────────────────────────────
# utils/__init__.py
# ─────────────────────────────────────────────

from .logger import get_logger

__all__ = ["get_logger"]

# ─────────────────────────────────────────────
# handlers/telegram_handler.py
# ─────────────────────────────────────────────

import threading
import time
from typing import Callable, Optional
import requests
from utils import get_logger
import config

logger = get_logger("TelegramHandler")


class TelegramHandler:
    BASE_URL = "https://api.telegram.org/bot{token}/{method}"

    def __init__(self, token: str, on_message: Optional[Callable] = None):
        self.token = token
        self.on_message = on_message
        self.offset = 0
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self.notifications: list[dict] = []

    def _api(self, method: str, payload: Optional[dict] = None) -> Optional[dict]:
        url = self.BASE_URL.format(token=self.token, method=method)
        try:
            response = requests.post(url, json=payload or {}, timeout=10)
            response.raise_for_status()
            data = response.json()
            if not data.get("ok"):
                logger.warning("Telegram API returned not-ok: %s", data)
                return None
            return data.get("result")
        except requests.RequestException as exc:
            logger.error("Telegram API request failed: %s", exc)
            return None

    def send_message(self, chat_id: int, text: str) -> bool:
        result = self._api("sendMessage", {"chat_id": chat_id, "text": text})
        if result:
            logger.info("Message sent to chat_id=%s", chat_id)
            return True
        return False

    def get_updates(self) -> list[dict]:
        payload = {"offset": self.offset, "timeout": 2, "limit": 10}
        updates = self._api("getUpdates", payload)
        if updates is None:
            return []
        return updates

    def _process_update(self, update: dict) -> None:
        update_id = update.get("update_id", 0)
        self.offset = update_id + 1

        message = update.get("message") or update.get("channel_post")
        if not message:
            return

        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "").strip()
        username = message.get("from", {}).get("username", "unknown")

        logger.info("Received message from @%s (chat=%s): %s", username, chat_id, text)

        notification = {
            "chat_id": chat_id,
            "username": username,
            "text": text,
            "timestamp": time.time(),
        }

        with self._lock:
            self.notifications.append(notification)
            if len(self.notifications) > 50:
                self.notifications.pop(0)

        command_result = self._handle_command(text, chat_id)
        if not command_result and self.on_message:
            self.on_message(notification)

    def _handle_command(self, text: str, chat_id: int) -> bool:
        commands = {
            "/status": self._cmd_status,
            "/tab": self._cmd_tab,
            "/ping": self._cmd_ping,
        }
        parts = text.split()
        if not parts:
            return False
        cmd = parts[0].lower()
        handler = commands.get(cmd)
        if handler:
            handler(parts[1:], chat_id)
            return True
        return False

    def _cmd_status(self, args: list, chat_id: int) -> None:
        self.send_message(chat_id, "PIP-BOY ONLINE — All systems nominal.")

    def _cmd_ping(self, args: list, chat_id: int) -> None:
        self.send_message(chat_id, "PONG — Pip-Boy responding.")

    def _cmd_tab(self, args: list, chat_id: int) -> None:
        if args and args[0].upper() in config.TABS:
            tab = args[0].upper()
            self.send_message(chat_id, f"Switching to {tab} screen.")
            with self._lock:
                self.notifications.append({
                    "chat_id": chat_id,
                    "username": "system",
                    "text": f"__switch_tab__{tab}",
                    "timestamp": time.time(),
                })
        else:
            self.send_message(
                chat_id,
                f"Available tabs: {', '.join(config.TABS)}"
            )

    def _poll_loop(self) -> None:
        logger.info("Telegram polling started.")
        while self._running:
            updates = self.get_updates()
            for update in updates:
                self._process_update(update)
            time.sleep(config.TELEGRAM_POLL_INTERVAL)
        logger.info("Telegram polling stopped.")

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=10)

    def get_latest_notifications