import pandas as pd
from sentence_transformers import SentenceTransformer, InputExample, losses, models
from torch.utils.data import DataLoader
import torch
import os

# Load your dataset (if not already loaded)
# df = pd.read_csv("your_dataset.csv")  # Make sure it has 'question_text' and 'sub_topic' columns

# Filter or preprocess if needed
df = df.dropna(subset=["question_text", "sub_topic"])
df["question_text"] = df["question_text"].astype(str)
df["sub_topic"] = df["sub_topic"].astype(str)

# Create training pairs as InputExample objects
train_examples = []
for i, row in df.iterrows():
    train_examples.append(
        InputExample(texts=[row["question_text"], row["sub_topic"]], label=1.0)
    )

# Create a DataLoader
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)

base_model_name = "all-MiniLM-L6-v2"  # SBERT lightweight model
model = SentenceTransformer(base_model_name)


train_loss = losses.CosineSimilarityLoss(model=model)

# Fine-tune
model_save_path = f"fine-tuned-sbert-model"
num_epochs = 6

model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=num_epochs,
    warmup_steps=100,
    output_path=model_save_path,
    show_progress_bar=True
)

print(f"✅ Model fine-tuned and saved at: {model_save_path}")
