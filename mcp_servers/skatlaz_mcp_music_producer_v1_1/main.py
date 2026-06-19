from skatlaz_music_producer.pipeline import MusicProducerPipeline

if __name__ == "__main__":
    pipeline = MusicProducerPipeline(
        input_dir="input_album",
        output_dir="output_album",
        album_title="My Damn Blues Book",
        artist="Busk Blues",
        label="Buskplay AI-DSP Press",
        run_demucs=True,
        export_mp3=True,
        export_wav=True,
        create_zip=True,
    )
    pipeline.process_album()
