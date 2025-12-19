# n8n Integration Instructions

This repository includes a simple n8n workflow example (`config/n8n_workflow.json`) that accepts Agent webhooks and logs them.

Steps to import and use:

1. Start n8n (e.g., `n8n start`).
2. In the n8n UI, go to the Workflows screen and choose "Import from File". Select `config/n8n_workflow.json`.
3. Activate the workflow.
4. In the workflow the webhook node path is `/agent-webhook`. n8n exposes webhook URLs of the form:

   https://<your-n8n-host>/webhook/agent-webhook

5. Run the agent and register the n8n webhook URL using the `--n8n` option:

```bash
python src/agent.py --config config/models.yaml --n8n "https://<your-n8n-host>/webhook/agent-webhook"
```

6. The agent will POST JSON payloads to the provided webhook on completion and for events.

Notes:
- Ensure your n8n instance is reachable from where you run the agent (public URL or tunneled). Use `ngrok` for local testing:

```bash
ngrok http 5678
```

- If you want to forward agent events to another system from n8n (Slack, email, database), add nodes after the Webhook node in the workflow.
