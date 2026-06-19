from pathlib import Path
from ai_core.models import FineTuneJob

def build_modelfile(job: FineTuneJob, output_root: str="models/ollama_exports") -> str:
    out_dir=Path(output_root)/job.name.replace(" ", "_"); out_dir.mkdir(parents=True, exist_ok=True)
    adapter_line=""
    if job.output_dir and job.method in {"lora", "qlora"}: adapter_line=f"ADAPTER {job.output_dir}\n"
    system="You are a specialized Skatlaz Server AI agent. Use RAG context and answer with precision."
    if job.agent and job.agent.prompt_template: system=job.agent.prompt_template.system_prompt.replace('"""','\\"\\"\\"')
    model_name=job.ollama_model_name or job.name.lower().replace(" ", "_")
    content = f'''FROM {job.base_model}
{adapter_line}PARAMETER temperature 0.2
PARAMETER top_p 0.9
SYSTEM """{system}"""
TEMPLATE """{{{{ if .System }}}}<|system|>
{{{{ .System }}}}{{{{ end }}}}
<|user|>
{{{{ .Prompt }}}}
<|assistant|>
"""
'''
    path=out_dir/"Modelfile"; path.write_text(content, encoding="utf-8")
    job.modelfile_path=str(path); job.ollama_model_name=model_name; job.save(update_fields=["modelfile_path", "ollama_model_name", "updated_at"])
    return str(path)

def ollama_create_command(job: FineTuneJob) -> str:
    if not job.modelfile_path: build_modelfile(job)
    return f"ollama create {job.ollama_model_name} -f {job.modelfile_path}"
