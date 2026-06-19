from pathlib import Path
from ai_core.models import FineTuneJob
from ai_core.finetuning.modelfile_builder import build_modelfile

QLORA_TEMPLATE = '''# Skatlaz Server AI 2.0 - QLoRA training stub
# Optional deps: pip install torch transformers datasets peft bitsandbytes accelerate trl
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig

BASE_MODEL = {base_model!r}
DATASET_PATH = {dataset_path!r}
OUTPUT_DIR = {output_dir!r}
# TODO: implement tokenization and SFTTrainer for your dataset schema.
'''

def prepare_training_job(job: FineTuneJob, output_root: str="training_runs") -> str:
    out_dir=Path(output_root)/job.name.replace(" ", "_"); out_dir.mkdir(parents=True, exist_ok=True)
    dataset_path=job.dataset.prepared_path if job.dataset else "dataset.jsonl"
    script_path=out_dir/"train_qlora.py"
    script_path.write_text(QLORA_TEMPLATE.format(base_model=job.base_model, dataset_path=dataset_path, output_dir=str(out_dir/"adapter")), encoding="utf-8")
    job.output_dir=str(out_dir/"adapter"); job.status="queued"; job.log += f"\nGenerated training script: {script_path}"; job.save()
    build_modelfile(job)
    return str(script_path)
