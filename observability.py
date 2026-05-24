def setup_phoenix(enabled: bool) -> None:
    """Launch a local Phoenix app and trace LlamaIndex spans."""
    if not enabled:
        return

    import phoenix as px
    from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
    from phoenix.otel import register

    px.launch_app()
    tracer_provider = register()
    LlamaIndexInstrumentor().instrument(tracer_provider=tracer_provider)
