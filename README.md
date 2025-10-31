# Secret Breach Detection in Source Code with Large Language Models

This repository presents a hybrid LLM-based system for secret detection in source code, combining regex-based candidate extraction with contextual classification by fine-tuned large language models. Evaluated on data from 818 GitHub repositories, the approach significantly reduces false positives while maintaining high recall. Fine-tuned LLaMA-3.1 8B and Mistral-7B models achieved F1-scores up to 0.985, outperforming traditional regex methods. The solution enables accurate, open-source, and privacy-preserving secret detection for integration into development workflows.

## Overview

This project includes:
- A dataset generation script.
- Data split notebook for training and evaluation.
- Folder structure supporting multiple LLMs with files for various evaluation and fine-tuning settings.

## Contents

### Dataset Creation

- **`secretbench_parser.py`**  
  Parses the original SecretBench data using the metadata in `secretbench.csv` and outputs a unified CSV file with:
  - Source code snippet
  - Candidate string (regex extracted)
  - Binary label indicating whether the candidate is a secret

- **`dataset_split.ipynb`**  
  Splits the parsed CSV into standard `train`, `eval`, and `test` sets for downstream tasks.

> **Note**: The original dataset is not included here. It is available at:  
> https://github.com/setu1421/SecretBench  
> Please contact the original authors for access or usage permissions.

### Model Folders

Each top-level folder (e.g., `llama/`, `mistral/`, etc.) contains files organized for different experimental settings:

- `zero_shot/` – Inputs and expected outputs for zero-shot evaluation
- `one_shot/` – Evaluation with one annotated example
- `few_shot/` – Evaluation with few annotated examples
- `fine_tuning/` – Data files formatted for supervised fine-tuning

## Citation

If you use this work, please cite this work:
```
@misc{rahman2025secretbreachdetectionsource,
      title={Secret Breach Detection in Source Code with Large Language Models}, 
      author={Md Nafiu Rahman and Sadif Ahmed and Zahin Wahab and S M Sohan and Rifat Shahriyar},
      year={2025},
      eprint={2504.18784},
      archivePrefix={arXiv},
      primaryClass={cs.SE},
      url={https://arxiv.org/abs/2504.18784}, 
}
```


## License

Refer to the [SecretBench repository](https://github.com/setu1421/SecretBench) for accessing details of the original data.

