!pip install transformers datasets accelerate scikit-learn pandas torch sentencepiece

import zipfile
import pandas as pd
import torch
import numpy as np

from torch.utils.data import Dataset
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, f1_score

from transformers import (
    BertTokenizer,
    XLMRobertaTokenizer,
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)

zip_path = "Basics of BERT and XLM-RoBERTa - PyTorch - 2.zip"

with zipfile.ZipFile(zip_path, "r") as zip_ref:
    zip_ref.extractall("bert_xlm_data")

with zipfile.ZipFile("bert_xlm_data/Basics of BERT and XLM-RoBERTa - PyTorch/train.csv.zip", "r") as zip_ref:
    zip_ref.extractall("bert_xlm_data")

with zipfile.ZipFile("bert_xlm_data/Basics of BERT and XLM-RoBERTa - PyTorch/test.csv.zip", "r") as zip_ref:
    zip_ref.extractall("bert_xlm_data")

train_df = pd.read_csv("bert_xlm_data/train.csv")
test_df = pd.read_csv("bert_xlm_data/test.csv")

display(train_df.head())
display(test_df.head())

print("Train shape:", train_df.shape)
print("Test shape:", test_df.shape)
print("Train columns:", train_df.columns)

bert_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
xlm_tokenizer = XLMRobertaTokenizer.from_pretrained("xlm-roberta-base")

sentence1 = train_df.loc[0, "premise"]
sentence2 = train_df.loc[0, "hypothesis"]

bert_tokens = bert_tokenizer.encode_plus(
    sentence1,
    sentence2,
    max_length=128,
    padding="max_length",
    truncation=True,
    return_tensors="pt"
)

xlm_tokens = xlm_tokenizer.encode_plus(
    sentence1,
    sentence2,
    max_length=128,
    padding="max_length",
    truncation=True,
    return_tensors="pt"
)

print("BERT special tokens:")
print(bert_tokenizer.special_tokens_map)
print("BERT vocab size:", bert_tokenizer.vocab_size)
print("BERT decoded example:")
print(bert_tokenizer.decode(bert_tokens["input_ids"][0]))

print("XLM-RoBERTa special tokens:")
print(xlm_tokenizer.special_tokens_map)
print("XLM-RoBERTa vocab size:", xlm_tokenizer.vocab_size)
print("XLM-RoBERTa decoded example:")
print(xlm_tokenizer.decode(xlm_tokens["input_ids"][0]))

kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

folds = []

for train_index, val_index in kf.split(train_df, train_df["label"]):
    train_split = train_df.iloc[train_index].reset_index(drop=True)
    val_split = train_df.iloc[val_index].reset_index(drop=True)
    folds.append((train_split, val_split))

for i, (train_split, val_split) in enumerate(folds):
    print(f"Fold {i + 1}")
    print("Train shape:", train_split.shape)
    print("Validation shape:", val_split.shape)
    print("Validation label distribution:")
    print(val_split["label"].value_counts(normalize=True))

class NLIDataset(Dataset):
    def __init__(self, dataframe, tokenizer, max_length=128, has_labels=True):
        self.dataframe = dataframe
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.has_labels = has_labels

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, index):
        row = self.dataframe.iloc[index]

        encoding = self.tokenizer.encode_plus(
            row["premise"],
            row["hypothesis"],
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_attention_mask=True,
            return_tensors="pt"
        )

        item = {
            "input_ids": encoding["input_ids"].squeeze(),
            "attention_mask": encoding["attention_mask"].squeeze()
        }

        if self.has_labels:
            item["labels"] = torch.tensor(row["label"], dtype=torch.long)

        return item

model_name = "xlm-roberta-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=1)

    return {
        "accuracy": accuracy_score(labels, predictions),
        "f1": f1_score(labels, predictions, average="weighted")
    }

train_split, val_split = folds[0]

train_dataset = NLIDataset(train_split, tokenizer, has_labels=True)
val_dataset = NLIDataset(val_split, tokenizer, has_labels=True)

model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=3
)

training_args = TrainingArguments(
    output_dir="./xlm_roberta_results",
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=1,
    weight_decay=0.01,
    logging_dir="./logs",
    load_best_model_at_end=True,
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics
)

trainer.train()

results = trainer.evaluate()
print(results)

test_dataset = NLIDataset(test_df, tokenizer, has_labels=False)

predictions = trainer.predict(test_dataset)
predicted_labels = np.argmax(predictions.predictions, axis=1)

submission = pd.DataFrame({
    "id": test_df["id"],
    "prediction": predicted_labels
})

submission.to_csv("submission.csv", index=False)

display(submission.head())
