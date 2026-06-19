from skatlaz_openstudio.audio.tools import audio_info, apply_audio_effects
from skatlaz_openstudio.image.tools import create_cover, apply_image_filter
from skatlaz_openstudio.canvas.tools import render_template

if __name__ == "__main__":
    print("Skatlaz OpenStudio MCP v2.0")
    print("Use run_server.bat para iniciar a API MCP FastAPI.")
    print("Exemplos:")
    print("- create_cover('My Book', 'subtitle', 'outputs/cover.png')")
