def setup_phoenix(
    enabled: bool,
    project_name: str = "default",
    description: str | None = None,
) -> None:
    """Launch a local Phoenix app and trace LlamaIndex + OpenAI spans.

    Instrumenting the OpenAI SDK captures chat-completion token usage
    (prompt/completion), which Phoenix surfaces as token counts and cost.
    Traces are grouped under `project_name`; the project id is assigned by
    Phoenix and logged for reference.
    """
    if not enabled:
        return

    import phoenix as px
    from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
    from openinference.instrumentation.openai import OpenAIInstrumentor
    from phoenix.client import Client
    from phoenix.otel import register

    px.launch_app()

    client = Client()
    try:
        project = client.projects.get(project_name=project_name)
    except Exception:
        project = client.projects.create(
            name=project_name, description=description
        )
    print(f"Phoenix project '{project_name}' (id={project.get('id')})", flush=True)

    tracer_provider = register(project_name=project_name)
    LlamaIndexInstrumentor().instrument(tracer_provider=tracer_provider)
    OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
