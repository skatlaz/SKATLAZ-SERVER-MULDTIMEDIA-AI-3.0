@echo off
python -c "from skatlaz_music_producer.deps import check_dependencies, print_dependency_report; print_dependency_report(check_dependencies())"
pause
