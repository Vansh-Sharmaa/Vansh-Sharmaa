# 🔬 LLM Fine-Tuning: LoRA, QLoRA & Parameter-Efficient Adaptation

A technical blueprint for memory-efficient LLM adaptation using Low-Rank Adaptation (LoRA) and 4-bit Quantized LoRA (QLoRA).

---

## 📐 Mathematical Formulation: LoRA

Given pre-trained weight matrix $W_0 \in \mathbb{R}^{d \times k}$, LoRA decomposes weight updates into two low-rank matrices:

$$W = W_0 + \Delta W = W_0 + \frac{\alpha}{r} (B \cdot A)$$

Where:
- $B \in \mathbb{R}^{d \times r}$ initialized to 0
- $A \in \mathbb{R}^{r \times k}$ initialized with Gaussian random values $\mathcal{N}(0, \sigma^2)$
- $r \ll \min(d, k)$ is the rank dimension (typically 8, 16, 32, or 64)
- $\alpha$ is a scaling constant (often set to $2 \times r$)

---

## ⚙️ QLoRA Innovations

1. **NF4 (NormalFloat4)**: Quantization data type theoretically optimal for zero-mean, unit-variance normally distributed neural network weights.
2. **Double Quantization (DQ)**: Quantizing the quantization constants themselves, saving ~0.37 bits per parameter.
3. **Paged Optimizers**: Managing GPU memory spikes during checkpointing and long context processing via CUDA Unified Memory paging.

---

## 🛠️ Minimal Hugging Face PEFT Configuration

```python
from peft import LoraConfig, get_peft_model, TaskType
from transformers import BitsAndBytesConfig
import torch

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True
)

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)
```
