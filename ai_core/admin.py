from django.contrib import admin
from django.apps import apps


def get_model(name):
    try:
        return apps.get_model('ai_core', name)
    except LookupError:
        return None


def safe_register(model, admin_class=None):
    if model is None:
        return
    try:
        if admin_class:
            admin.site.register(model, admin_class)
        else:
            admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass


class SimpleSkatlazAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')


# Modelos legados do Skatlaz Server AI 3.0
AgentCategory = get_model('AgentCategory')
AiAgent = get_model('AiAgent')
ChatSession = get_model('ChatSession')
ChatMessage = get_model('ChatMessage')
DocumentSource = get_model('DocumentSource')
FineTuneJob = get_model('FineTuneJob')
LlmProvider = get_model('LlmProvider')
PromptTemplate = get_model('PromptTemplate')
RagChunk = get_model('RagChunk')
RagCollection = get_model('RagCollection')
TrainingDataset = get_model('TrainingDataset')
WebDiverTask = get_model('WebDiverTask')


if AgentCategory:
    class AgentCategoryAdmin(admin.ModelAdmin):
        list_display = tuple(f.name for f in AgentCategory._meta.fields[:4])
        search_fields = tuple(f.name for f in AgentCategory._meta.fields if f.get_internal_type() in ('CharField', 'TextField'))[:3]
    safe_register(AgentCategory, AgentCategoryAdmin)

if LlmProvider:
    class LlmProviderAdmin(admin.ModelAdmin):
        list_display = tuple(f.name for f in LlmProvider._meta.fields[:5])
        search_fields = tuple(f.name for f in LlmProvider._meta.fields if f.get_internal_type() in ('CharField', 'TextField'))[:3]
    safe_register(LlmProvider, LlmProviderAdmin)

if AiAgent:
    class AiAgentAdmin(admin.ModelAdmin):
        list_display = tuple(x for x in ('name', 'category', 'provider', 'role', 'is_active') if hasattr(AiAgent, x)) or ('id',)
        list_filter = tuple(x for x in ('category', 'provider', 'is_active') if hasattr(AiAgent, x))
        search_fields = tuple(x for x in ('name', 'role', 'system_prompt') if hasattr(AiAgent, x))
    safe_register(AiAgent, AiAgentAdmin)


class PromptTemplateAdmin(admin.ModelAdmin):
    """Admin seguro para PromptTemplate.

    Algumas bases antigas do Skatlaz Server AI 3.0 possuem a tabela legada
    ai_core_aiagent.prompt_template_id com FK NO ACTION no SQLite. Ao apagar
    um PromptTemplate pelo admin, o SQLite pode disparar:

        IntegrityError: FOREIGN KEY constraint failed

    Antes de excluir, limpamos as referências legadas para permitir a exclusão
    segura, equivalente ao comportamento esperado de SET_NULL.
    """
    list_display = tuple(f.name for f in PromptTemplate._meta.fields[:5]) if PromptTemplate else ('id',)
    search_fields = tuple(f.name for f in PromptTemplate._meta.fields if f.get_internal_type() in ('CharField', 'TextField'))[:4] if PromptTemplate else ()

    def _clear_legacy_aiagent_prompt_refs(self, ids):
        if not ids:
            return
        from django.db import connection
        ids = [int(x) for x in ids if x]
        placeholders = ','.join(['%s'] * len(ids))
        table_names = connection.introspection.table_names()
        if 'ai_core_aiagent' not in table_names:
            return
        with connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE ai_core_aiagent SET prompt_template_id = NULL WHERE prompt_template_id IN ({placeholders})",
                ids,
            )

    def delete_model(self, request, obj):
        self._clear_legacy_aiagent_prompt_refs([obj.pk])
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        self._clear_legacy_aiagent_prompt_refs(list(queryset.values_list('pk', flat=True)))
        super().delete_queryset(request, queryset)

if PromptTemplate:
    safe_register(PromptTemplate, PromptTemplateAdmin)

for model in [ChatSession, ChatMessage, DocumentSource, FineTuneJob, RagChunk, RagCollection, TrainingDataset, WebDiverTask]:
    if model:
        class DynamicAdmin(admin.ModelAdmin):
            list_display = tuple(f.name for f in model._meta.fields[:5])
            search_fields = tuple(f.name for f in model._meta.fields if f.get_internal_type() in ('CharField', 'TextField'))[:4]
        safe_register(model, DynamicAdmin)


# Novos modelos MCP / JSON
AITaskType = get_model('AITaskType')
AIMCPServer = get_model('AIMCPServer')
AIMCPAgent = get_model('AIMCPAgent')
AIJSONLibrary = get_model('AIJSONLibrary')
AIPromptTemplate = get_model('AIPromptTemplate')
AIUploadSession = get_model('AIUploadSession')
AIGeneratedArtifact = get_model('AIGeneratedArtifact')
MCPMultimediaConfig = get_model('MCPMultimediaConfig')

if AITaskType:
    class AITaskTypeAdmin(admin.ModelAdmin):
        list_display = tuple(x for x in ('name', 'slug', 'is_active') if hasattr(AITaskType, x)) or ('id',)
        search_fields = tuple(x for x in ('name', 'slug', 'description') if hasattr(AITaskType, x))
    safe_register(AITaskType, AITaskTypeAdmin)

if AIMCPServer:
    class AIMCPServerAdmin(admin.ModelAdmin):
        list_display = tuple(x for x in ('name', 'task_type', 'is_active', 'created_at') if hasattr(AIMCPServer, x)) or ('id',)
        list_filter = tuple(x for x in ('task_type', 'is_active') if hasattr(AIMCPServer, x))
        search_fields = tuple(x for x in ('name', 'description', 'endpoint_url') if hasattr(AIMCPServer, x))
    safe_register(AIMCPServer, AIMCPServerAdmin)

if AIMCPAgent:
    class AIMCPAgentAdmin(admin.ModelAdmin):
        list_display = tuple(x for x in ('name', 'task_type', 'mcp_server', 'is_active', 'created_at') if hasattr(AIMCPAgent, x)) or ('id',)
        list_filter = tuple(x for x in ('task_type', 'mcp_server', 'is_active') if hasattr(AIMCPAgent, x))
        search_fields = tuple(x for x in ('name', 'description', 'system_prompt') if hasattr(AIMCPAgent, x))
    safe_register(AIMCPAgent, AIMCPAgentAdmin)

for model in [AIJSONLibrary, AIPromptTemplate, AIUploadSession, AIGeneratedArtifact, MCPMultimediaConfig]:
    if model:
        class MCPDynamicAdmin(admin.ModelAdmin):
            list_display = tuple(f.name for f in model._meta.fields[:6])
            search_fields = tuple(f.name for f in model._meta.fields if f.get_internal_type() in ('CharField', 'TextField'))[:4]
        safe_register(model, MCPDynamicAdmin)

admin.site.site_header = 'Skatlaz Server AI 3.0'
admin.site.site_title = 'Skatlaz Admin'
admin.site.index_title = 'Site administration'
