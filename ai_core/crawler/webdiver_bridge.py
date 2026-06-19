from ai_core.models import WebDiverTask, DocumentSource

def run_webdiver_task(task: WebDiverTask) -> WebDiverTask:
    task.status="running"; task.save(update_fields=["status", "updated_at"])
    try:
        try:
            from webdiver.web_diver import www_diver_add_task, www_diver_start
            www_diver_add_task(task.url)
            www_diver_start(task.database_path, task.diver_type)
            result=f"WebDiver finished: {task.url} with type {task.diver_type}. Database: {task.database_path}"
        except Exception as exc:
            result=f"WebDiver fallback: URL registered but crawler package failed/unavailable. Error: {exc}"
        task.result_text=result; task.status="done"; task.error=""; task.save()
        if task.collection:
            DocumentSource.objects.create(collection=task.collection, source_type="web", title=task.url, url=task.url, raw_text=result, metadata={"webdiver_task_id": task.id, "diver_type": task.diver_type})
    except Exception as exc:
        task.status="error"; task.error=str(exc); task.save()
    return task
