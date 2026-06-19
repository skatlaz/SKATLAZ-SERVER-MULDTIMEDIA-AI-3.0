from django.core.management.base import BaseCommand
from ai_core.models import FineTuneJob
from ai_core.training.pytorch_lab import prepare_training_job
from ai_core.finetuning.modelfile_builder import ollama_create_command

class Command(BaseCommand):
    help = "Generate QLoRA training stub and Ollama Modelfile."
    def add_arguments(self, parser): parser.add_argument("job_id", type=int)
    def handle(self, *args, **opts):
        job=FineTuneJob.objects.get(id=opts["job_id"])
        script=prepare_training_job(job)
        self.stdout.write(self.style.SUCCESS(f"Training script: {script}"))
        self.stdout.write(self.style.SUCCESS(ollama_create_command(job)))
