import time
import uuid

import requests

from backend.config import settings


class GigaChatClient:
    def __init__(self):
        self._token: str | None = None
        self._token_expire_ts = 0.0

    def _fetch_token(self) -> str:
        headers = {
            "Authorization": f"Basic {settings.gigachat_credentials}",
            "RqUID": str(uuid.uuid4()),
            "Content-Type": "application/x-www-form-urlencoded",
        }
        payload = {"scope": settings.gigachat_scope}
        response = requests.post(settings.gigachat_auth_url, headers=headers, data=payload, timeout=30, verify=False)
        response.raise_for_status()
        data = response.json()
        self._token = data["access_token"]
        self._token_expire_ts = time.time() + int(data.get("expires_at", 1800)) - 60
        return self._token

    def _token_or_refresh(self) -> str:
        if not self._token or time.time() >= self._token_expire_ts:
            return self._fetch_token()
        return self._token

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        if not settings.gigachat_credentials:
            return (
                "Не удалось обратиться к GigaChat: отсутствуют credentials. "
                "Заполните GIGACHAT_CREDENTIALS в .env."
            )
        token = self._token_or_refresh()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        payload = {
            "model": settings.gigachat_model,
            "temperature": 0.1,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        response = requests.post(f"{settings.gigachat_api_url}/chat/completions", headers=headers, json=payload, timeout=60, verify=False)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()


gigachat_client = GigaChatClient()
