<div align="center">

#  LagrangianLM

### A Production-Grade Small Language Model Built From First Principles

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-red?style=for-the-badge&logo=pytorch)
![Status](https://img.shields.io/badge/Status-In%20Development-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</p>

---

#  Development Progress

### Overall Project Progress

```text
█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 3%
```

>  **Currently Building:** Project Foundation & Development Environment

---

*"A journey to understand every component from first principles."*

</div>

---

# 📖 Introduction

**LagrangianLM** is a production-grade Small Language Model (SLM) inspired by the **LLaMA** family of models.

Instead of relying on existing implementations, this project aims to build every major component of a modern Large Language Model from scratch while maintaining production-level software engineering practices.

The objective is not simply to reproduce an architecture—but to understand the mathematics, engineering decisions, and systems behind modern language models.

The project will eventually include:

-  Custom tokenizer
-  LLaMA-inspired architecture
-  Rotary Positional Embeddings (RoPE)
-  RMSNorm
-  SwiGLU
-  Pretraining from scratch
-  Instruction Fine-tuning
-  Inference Optimization
-  Docker Deployment
-  FastAPI Serving
-  Experiment Tracking
-  Benchmarks & Evaluation

---

#  Motivation

Modern language models are often treated as black boxes.

LagrangianLM exists to change that.

This project focuses on understanding every stage of building a language model:

- How raw text becomes training data.
- Why tokenization works.
- How attention learns context.
- Why modern architectures evolved beyond GPT-2.
- How models are pretrained.
- How inference is optimized.
- How production systems serve millions of requests efficiently.

Every component will be implemented from first principles before using optimized libraries.

---

# 🏗️ Architecture

```text
                 Raw Text
                     │
                     ▼
            Dataset Engineering
                     │
                     ▼
             SentencePiece/BPE Tokenizer
                     │
                     ▼
                 Token IDs
                     │
                     ▼
             Token Embeddings
                     │
                     ▼
         Rotary Positional Embeddings
                     │
                     ▼
        Transformer Decoder Blocks × N
                     │
      ┌──────────────┴──────────────┐
      │                             │
      ▼                             ▼
 Multi-Head Attention          SwiGLU MLP
      │                             │
      └──────────────┬──────────────┘
                     ▼
                 RMSNorm
                     │
                     ▼
              Language Model Head
                     │
                     ▼
           Next Token Prediction
```

---

# 📂 Project Structure

```text
LagrangianLM/
│
├── configs/
├── datasets/
├── tokenizer/
├── model/
│   ├── embeddings.py
│   ├── rope.py
│   ├── rmsnorm.py
│   ├── swiglu.py
│   ├── attention.py
│   ├── decoder.py
│   └── lagrangianlm.py
│
├── training/
├── inference/
├── evaluation/
├── scripts/
├── checkpoints/
├── logs/
├── docs/
├── tests/
├── utils/
├── notebooks/
│
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/LagrangianLM.git
```

Move into the project

```bash
cd LagrangianLM
```

Sync dependencies using **uv**

```bash
uv sync
```

Run Python

```bash
uv run python
```

---

#  Project Goals

- Build a **150M parameter Small Language Model**
- Train from scratch
- Understand every mathematical component
- Build production-grade infrastructure
- Optimize inference
- Deploy publicly
- Document every stage of development


---

#  License

This project will be released under the **MIT License**.

---

# Acknowledgements

This project is inspired by the research and engineering efforts behind modern language models, including:

- Meta AI (LLaMA)
- OpenAI (GPT)
- Hugging Face
- PyTorch
- Stanford CS336
- Andrej Karpathy
- Sebastian Raschka

---

<div align="center">

### ⭐ If you find this project interesting, consider giving it a star!

**Building modern AI systems from first principles.**

</div>