## GPT-Driven Topic CLI

This project packages a LangChain-based command-line assistant that runs inside Docker. The provided `Makefile` orchestrates all project interactions, so you never have to execute project commands directly on the host.

## Prerequisites

- Docker and Docker Compose installed and running
- GNU Make available on your system

## Quick Start

1. **Create a `.env` file (required before building)**

   The `.env` file is ignored by Git and is used by Docker Compose to inject credentials at build/run time. Create it in the project root with the required GitHub Models configuration:

   ```env
   GITHUB_TOKEN=your_github_models_token               # required
   GITHUB_BASE_URL=https://models.github.ai/inference  # optional override
   GITHUB_MODEL=openai/gpt-4o-mini                     # optional override
   ```

   Replace the sample values with your actual credentials. `GITHUB_BASE_URL` and `GITHUB_MODEL` default to GitHub’s public endpoint and `openai/gpt-4o` if omitted.

2. **Build the container image**

   ```bash
   make build
   ```

   The `build` target automatically copies `.env.example` to `.env` if it does not exist yet.

3. **Run the assistant for a given topic**

   Supply a topic (required):

   ```bash
   make run TOPIC="AI in Healthcare"
   ```

   The CLI will launch inside the container, print posts in all supported languages, and then exit. The `.env` file is mounted automatically, so no extra flags are needed.

   To bring the container up using Docker Compose (e.g., for inspecting logs or running ad-hoc commands), use:

   ```bash
   make up
   ```

   This keeps the container running without executing the CLI; you can then `docker compose exec app ...` as needed. Set `WATCH_MODE=true` when invoking `make up` if you want live auto-reload via `watchfiles`.

4. **Clean up local Docker artifacts**

   ```bash
   make docker-clean
   ```

## Additional Notes

- Available targets: `make build`, `make run`, `make up`, `make docker-clean`.
- All commands execute through Docker Compose, keeping your host environment clean.
- Keep your `.env` file private—it’s already excluded from version control via `.gitignore`.
- Ensure `.env` defines `GITHUB_TOKEN`. `GITHUB_BASE_URL` and `GITHUB_MODEL` override defaults when present.
- `make run` forces `WATCH_MODE=false`, so the CLI exits after printing generated posts. Enable watch mode only when intentionally running the container (`WATCH_MODE=true make up`).
- Update environment variables or configuration inside the containerized app as needed.

