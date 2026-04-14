from intent_decomposer import IntentDecomposer


def simulate_global_deployment_intent():
    decomposer = IntentDecomposer()

    # 1. Create a Global Intent for building a distributed multi-region platform
    intent_id = decomposer.create_intent(
        "Deploy a global, Vercel-like infrastructure caching layer across EU, US, and AP regions with automated DNS cutover."
    )

    # 2. Decompose intent into a DAG of agent fast-path tasks
    # The DAG represents dependencies using 'depends_on' pointing to 'internal_id'
    intent_tasks = [
        # Phase 1: Planning and Architecture
        {
            "internal_id": "arch_design",
            "agent": "3design",
            "payload": {"prompt": "Design multi-region active-active PostgreSQL cluster with Edge caching nodes."},
            "depends_on": []
        },
        # Phase 2: Infra Setup (parallel tasks waiting on architecture)
        {
            "internal_id": "infra_us",
            "agent": "terraform", # We'll map to a generic execution agent if terraform doesn't exist
            "payload": {"prompt": "Deploy edge cluster in us-east-1 and us-west-2 based on arch document."},
            "depends_on": ["arch_design"]
        },
        {
            "internal_id": "infra_eu",
            "agent": "terraform",
            "payload": {"prompt": "Deploy edge cluster in eu-central-1 and eu-west-1 based on arch document."},
            "depends_on": ["arch_design"]
        },
        {
            "internal_id": "infra_ap",
            "agent": "terraform",
            "payload": {"prompt": "Deploy edge cluster in ap-northeast-1 and ap-southeast-2 based on arch document."},
            "depends_on": ["arch_design"]
        },
        # Phase 3: Validation and Cutover
        {
            "internal_id": "health_check",
            "agent": "7exec",
            "payload": {"prompt": "Perform global latency and health checks across all new edge nodes."},
            "depends_on": ["infra_us", "infra_eu", "infra_ap"]
        },
        {
            "internal_id": "dns_cutover",
            "agent": "9git", # Represents config rollout/gitops
            "payload": {"prompt": "Merge Route53 / Cloudflare DNS cutover PR pointing traffic to new Edge global accelerator."},
            "depends_on": ["health_check"]
        },
        {
            "internal_id": "observability",
            "agent": "logging",
            "payload": {"prompt": "Configure global Grafana dashboards for cache hit-rates and node telemetry."},
            "depends_on": ["arch_design"] # Can happen concurrently with Infra setup
        }
    ]

    # Map agents that might not have fast-paths to default 0master or terminal for demo purposes
    for t in intent_tasks:
        if t["agent"] not in ["3design", "7exec", "9git", "logging"]:
            t["agent"] = "7exec"

    # Queue into Postgres DAG
    decomposer.decompose_and_queue(intent_id, intent_tasks)

if __name__ == "__main__":
    simulate_global_deployment_intent()
