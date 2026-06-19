from django.core.management.base import BaseCommand
from ai_core.models import DocumentSource
from ai_core.rag.retriever import index_source

class Command(BaseCommand):
    help = "Index RAG document sources into chunks."
    def add_arguments(self, parser): parser.add_argument("--source-id", type=int, default=None)
    def handle(self, *args, **opts):
        qs = DocumentSource.objects.filter(id=opts["source_id"]) if opts["source_id"] else DocumentSource.objects.filter(indexed=False)
        for source in qs:
            count=index_source(source)
            self.stdout.write(self.style.SUCCESS(f"Indexed {source}: {count} chunks"))
