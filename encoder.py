"""Load multilingual E5 and reproduce masked mean pooling."""
import numpy as np


class E5Encoder:
    def __init__(self, checkpoint):
        import torch
        from transformers import AutoModel, AutoTokenizer

        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        self.model = AutoModel.from_pretrained(checkpoint).eval()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def encode(self, texts, normalize_embeddings=True):
        batches = []
        for start in range(0, len(texts), 16):
            inputs = self.tokenizer(texts[start:start+16], padding=True, truncation=True,
                                    max_length=512, return_tensors="pt").to(self.device)
            with self.torch.inference_mode():
                hidden = self.model(**inputs).last_hidden_state
                mask = inputs.attention_mask.unsqueeze(-1)
                vectors = (hidden * mask).sum(dim=1) / mask.sum(dim=1)
                if normalize_embeddings:
                    vectors = self.torch.nn.functional.normalize(vectors, dim=1)
                batches.append(vectors.cpu().numpy())
        return np.concatenate(batches)
