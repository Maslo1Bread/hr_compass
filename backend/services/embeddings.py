import hashlib
from typing import Iterable

import numpy as np


EMBEDDING_DIM = 384


def _hash_token(token: str) -> int:
    digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def embed_texts(texts: Iterable[str]) -> np.ndarray:
    texts = list(texts)
    vectors = np.zeros((len(texts), EMBEDDING_DIM), dtype="float32")
    for i, text in enumerate(texts):
        for token in text.lower().split():
            vectors[i, _hash_token(token) % EMBEDDING_DIM] += 1.0
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return vectors / norms


def embed_text(text: str) -> np.ndarray:
    return embed_texts([text])[0]
