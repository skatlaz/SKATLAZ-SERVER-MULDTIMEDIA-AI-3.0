from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [('ai_core', '0001_initial')]
    operations = [
        migrations.CreateModel(
            name='MCPMultimediaConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Default Multimedia MCP', max_length=140)),
                ('image_engine', models.CharField(default='flux.1-dev', max_length=80)),
                ('video_engine', models.CharField(default='wan2.1', max_length=80)),
                ('audio_engine', models.CharField(default='bark-tts', max_length=80)),
                ('rag_engine', models.CharField(default='sentence-transformers', max_length=80)),
                ('code_engine', models.CharField(default='deepseek-code', max_length=80)),
                ('enable_image_mcp', models.BooleanField(default=True)),
                ('enable_video_mcp', models.BooleanField(default=True)),
                ('enable_audio_mcp', models.BooleanField(default=True)),
                ('enable_rag_mcp', models.BooleanField(default=True)),
                ('enable_code_mcp', models.BooleanField(default=True)),
                ('config_json', models.JSONField(blank=True, default=dict)),
                ('training_json', models.JSONField(blank=True, default=dict)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'verbose_name': 'MCP Multimedia Config', 'verbose_name_plural': 'MCP Multimedia Configs'},
        ),
    ]
