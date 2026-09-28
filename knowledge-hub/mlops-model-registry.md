# ⚡ MLOps: Experiment Tracking & Model Registry with MLflow

Production Machine Learning systems require reproducible experiment tracking, lineage, data schemas, and validated artifacts.

---

## 📊 End-to-End Tracking Architecture

```
[Training Pipeline]
        │
        ├──► Metrics (Loss, F1, Perplexity) ───► MLflow Tracking Server
        ├──► Hyperparameters (lr, batch_size) ─► Backend Store (Postgres)
        └──► Artifacts (ONNX, PyTorch, LoRA) ──► Artifact Store (S3 / GCS / Local)
                                                        │
                                                        ▼
                                              [MLflow Model Registry]
                                              - Staging / Production
                                              - Signature Validation
```

---

## 🛠️ Python Implementation Pattern

```python
import mlflow
from mlflow.models.signature import infer_signature
import numpy as np

mlflow.set_experiment("llm-eval-suite")

with mlflow.start_run(run_name="qlora-llama3-instruct"):
    # Log hyperparameters
    mlflow.log_params({
        "model_id": "meta-llama/Llama-3.2-3B",
        "lora_r": 16,
        "lora_alpha": 32,
        "learning_rate": 2e-4,
        "epochs": 3
    })
    
    # Validation step
    eval_loss = 0.842
    eval_ppl = np.exp(eval_loss)
    mlflow.log_metrics({"val_loss": eval_loss, "val_perplexity": eval_ppl})
    
    # Input/Output signature enforcement
    dummy_input = {"prompt": "Summarize this document."}
    dummy_output = {"summary": "Brief summary..."}
    sig = infer_signature(dummy_input, dummy_output)
    
    # Register model to MLflow Model Registry
    mlflow.pyfunc.log_model(
        artifact_path="model",
        registered_model_name="DocumentSummarizer",
        signature=sig
    )
```

---

## 🛡️ Production Governance Checklist
- [x] **Enforce Model Signatures**: Guard against silent inference data-schema drift.
- [x] **Tag Model Artifacts**: Store commit SHA, dataset version, and training hardware.
- [x] **Automated Shadow Deployments**: Test new versions side-by-side with champion models.
