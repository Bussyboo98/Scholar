import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from transformers import DebertaV2Tokenizer, DebertaV2ForSequenceClassification
from torch.nn.functional import mse_loss
from tqdm import tqdm

# Dataset class
class EssayDataset(Dataset):
    def __init__(self, texts, scores, tokenizer, max_length):
        self.texts = texts
        self.scores = scores
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, index):
        text = self.texts[index]
        score = self.scores[index]
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            truncation=True,
            padding="max_length",
            return_tensors="pt"
        )
        return {
            "input_ids": encoding["input_ids"].squeeze(),
            "attention_mask": encoding["attention_mask"].squeeze(),
            "score": torch.tensor(score, dtype=torch.float),
        }

# Load data
train_data = pd.read_csv("train_data.csv", delimiter=";")
val_data = pd.read_csv("val_data.csv", delimiter=";")


train_texts = train_data["essay_text"].tolist()
train_scores = train_data["score"].tolist()
val_texts = val_data["essay_text"].tolist()
val_scores = val_data["score"].tolist()

# Set tokenizer and model
max_length = 512
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = DebertaV2Tokenizer.from_pretrained("microsoft/deberta-v3-large")
model = DebertaV2ForSequenceClassification.from_pretrained(
    "microsoft/deberta-v3-large",
    num_labels=1
).to(device)

# Create datasets and loaders
train_dataset = EssayDataset(train_texts, train_scores, tokenizer, max_length)
val_dataset = EssayDataset(val_texts, val_scores, tokenizer, max_length)

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=16)

# Training setup
optimizer = AdamW(model.parameters(), lr=2e-5)
num_epochs = 3

# Training loop
for epoch in range(num_epochs):
    model.train()
    total_loss = 0
    for batch in tqdm(train_loader, desc=f"Epoch {epoch + 1}"):
        optimizer.zero_grad()
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        scores = batch["score"].to(device)

        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        predictions = outputs.logits.squeeze()
        loss = mse_loss(predictions, scores)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch + 1} Loss: {total_loss / len(train_loader)}")

    # Validation loop
    model.eval()
    total_val_loss = 0
    with torch.no_grad():
        for batch in val_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            scores = batch["score"].to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            predictions = outputs.logits.squeeze()
            loss = mse_loss(predictions, scores)
            total_val_loss += loss.item()
    print(f"Epoch {epoch + 1} Validation Loss: {total_val_loss / len(val_loader)}")

# Save the model and tokenizer
model.save_pretrained("saved_model")
tokenizer.save_pretrained("saved_model")

print("Training complete. Model saved to 'saved_model'.")
