import json
import os
from pathlib import Path

import faiss
import numpy as np

from backend.config import settings


class FaissStore:
    def __init__(self):
        self.store_dir = Path(settings.vector_store_dir)
        self.store_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.store_dir / "index.faiss"
        self.meta_path = self.store_dir / "meta.json"
        self.dimension = 384
        self.index = faiss.IndexFlatIP(self.dimension)
        self.meta: list[dict] = []
        self._load()

    def _load(self) -> None:
        if self.index_path.exists():
            self.index = faiss.read_index(str(self.index_path))
        if self.meta_path.exists():
            self.meta = json.loads(self.meta_path.read_text(encoding="utf-8"))

    def save(self) -> None:
        faiss.write_index(self.index, str(self.index_path))
        self.meta_path.write_text(json.dumps(self.meta, ensure_ascii=False), encoding="utf-8")

    def add(self, vectors: np.ndarray, metadata: list[dict]) -> None:
        if vectors.size == 0:
            return
        self.index.add(vectors.astype("float32"))
        self.meta.extend(metadata)
        self.save()

    def search(self, vector: np.ndarray, top_k: int = 4) -> list[dict]:
        if self.index.ntotal == 0:
            return []
        scores, idxs = self.index.search(vector.reshape(1, -1).astype("float32"), top_k)
        results = []
        for score, idx in zip(scores[0], idxs[0]):
            if idx == -1 or idx >= len(self.meta):
                continue
            item = self.meta[idx].copy()
            item["score"] = float(score)
            results.append(item)
        return results

    def rebuild(self, vectors: np.ndarray, metadata: list[dict]) -> None:
        self.index = faiss.IndexFlatIP(self.dimension)
        self.meta = []
        self.add(vectors, metadata)


faiss_store = FaissStore()
