# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\cli\init.py
import os
import shutil

import typer
from ovo.cli.common import OVOCliError, console, download_files, init_nextflow
from ovo.core.configuration import (
    DEFAULT_OVO_HOME,
    ConfigProps,
    get_shell_config_path,
    get_source_command,
    save_default_config,
)
from rich.prompt import Confirm, Prompt

app = typer.Typer(pretty_exceptions_enable=False, help="OVO initialization commands")

RFDIFFUSION_MODEL_FILES = [
    # URL, local path, hash (SHA256: calculate with "shasum -a 256 my_file" or "sha256sum my_file")
    (
        "https://files.ipd.uw.edu/pub/RFdiffusion/6f5902ac237024bdd0c176cb93063dc4/Base_ckpt.pt",
        "rfdiffusion_models/Base_ckpt.pt",
        "0fcf7d7c32b4848030aca3a051e6768de194616f96ba6c38186351a33bfc6eca",
    ),
    (
        "https://files.ipd.uw.edu/pub/RFdiffusion/e29311f6f1bf1af907f9ef9f44b8328b/Complex_base_ckpt.pt",
        "rfdiffusion_models/Complex_base_ckpt.pt",
        "76e4e260aefee3b582bd76b77ab95d2592e64f00c51bf344968ab9239f3250bc",
    ),
    (
        "https://files.ipd.uw.edu/pub/RFdiffusion/f572d396fae9206628714fb2ce00f72e/Complex_beta_ckpt.pt",
        "rfdiffusion_models/Complex_beta_ckpt.pt",
        "5a0b1cafc23c60b1aabcec1e49391986ac4fd02cc1b6b4cc41714ca9fe882e9e",
    ),
    (
        "https://files.ipd.uw.edu/pub/RFdiffusion/5532d2e1f3a4738decd58b19d633b3c3/ActiveSite_ckpt.pt",
        "rfdiffusion_models/ActiveSite_ckpt.pt",
        "beca1f672049161df0bc6a2d2523828f19fd9c8a2b449988e246dde42e7ea986",
    ),
    (
        "https://files.ipd.uw.edu/pub/RFdiffusion/74f51cfb8b440f50d70878e05361d8f0/InpaintSeq_ckpt.pt",
        "rfdiffusion_models/InpaintSeq_ckpt.pt",
        "3b71b2b954e87d46b75a88ba64e0420fbf27f592604b10b6c3561b8c8ab70ab6",
    ),
]

ALPHAFOLD_MODEL_FILES = [
    (
        "https://storage.googleapis.com/alphafold/alphafold_params_2022-12-06.tar",
        "alphafold_models",
        "36d4b0220f3c735f3296d301152b738c9776d16981d054845a68a1370b26cfe3",
    )
]

ESM1V_MODEL_FILES = [
    (
        "https://dl.fbaipublicfiles.com/fair-esm/models/esm1v_t33_650M_UR90S_1.pt",
        "esm_models/esm1v_t33_650M_UR90S_1.pt",
        "9519ee60f1cddad3c101afb1f42612499e188534969c3f682e94850870f70433",
    ),
    (
        "https://dl.fbaipublicfiles.com/fair-esm/models/esm1v_t33_650M_UR90S_2.pt",
        "esm_models/esm1v_t33_650M_UR90S_2.pt",
        "5b7b095e8eafc53ccfe5994b954fb756bfe7a081f22b4caa1ed59b77b90bcf81",
    ),
    (
        "https://dl.fbaipublicfiles.com/fair-esm/models/esm1v_t33_650M_UR90S_3.pt",
        "esm_models/esm1v_t33_650M_UR90S_3.pt",
        "bc5cb2f2a1b35def284e2b2833ae58c803ca9c61b16b72c1dd54c54e76df0b67",
    ),
    (
        "https://dl.fbaipublicfiles.com/fair-esm/models/esm1v_t33_650M_UR90S_4.pt",
        "esm_models/esm1v_t33_650M_UR90S_4.pt",
        "44750a28c09f7ba9e7ccb7aeaba812cbbe90eb2a8a2c658dc5fa165f7090a15a",
    ),
    (
        "https://dl.fbaipublicfiles.com/fair-esm/models/esm1v_t33_650M_UR90S_5.pt",
        "esm_models/esm1v_t33_650M_UR90S_5.pt",
        "69ffd06be29aaaf105eda919f23e5ac4a6872e7907fbf1f087fd942abdb3adf7",
    ),
]

ESM_IF_MODEL_FILES = [
    (
        "https://dl.fbaipublicfiles.com/fair-esm/models/esm_if1_gvp4_t16_142M_UR50.pt",
        "esm_models/esm_if1_gvp4_t16_142M_UR50.pt",
        "be4ba36edec22a9bfaa4946ff6b2815f1f19d8a3d7e0eada8b796d5a0eae9fd4",
    )
]

BOLTZ_MODEL_FILES = {
    (
        "https://huggingface.co/boltz-community/boltz-1/resolve/main/boltz1_conf.ckpt",
        "boltz_models/boltz1_conf.ckpt",
        "fea245d912c570ec117b2277c2719f312a6fc109c07b6f6ef741690ee775c2f5",
    ),
    (
        "https://huggingface.co/boltz-community/boltz-1/resolve/main/ccd.pkl",
        "boltz_models/ccd.pkl",
        "2d3b2f03a3c5665944adba51e33263511e51b21c9cd05d902f9c4b7c1e58d2f4",
    ),
}


@app.command()
def home(
    home_dir: str | None = typer.Argument(None, help="OVO home directory"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Confirm all without prompting"),
    no_env: bool = typer.Option(False, "--no-env", help="Do not set OVO_HOME in shell .bashrc/.zshrc file"),
    default_profile: str = typer.Option(None, "--profile", help="Default nextflow profile to use in default scheduler"),
):
    """Initialize the OVO home directory"""

    console.print("[bold]OVO initialization[/bold]")

    if home_dir is None:
        console.print("""
[bold]Create OVO home directory[/bold]

This directory will contain all OVO files:

- [bold]config.yml[/bold][gray]______[/gray]configuration file
- [bold]ovo.db[/bold][gray]__________[/gray]SQLite database (stored as a single file)
- [bold]workdir[/bold][gray]_________[/gray]Working directory for Nextflow workflows
- [bold]storage[/bold][gray]_________[/gray]PDB design files and other permanent results
- [bold]reference_files[/bold][gray]_[/gray]Downloaded model weights and other reference files

All paths can be customized later in the [bold]config.yml[/bold] file.
""")
        home_dir = yes or Prompt.ask(
            prompt="Enter path, or press [bold]Enter[/bold] to select the default",
            default=os.getenv("OVO_HOME", DEFAULT_OVO_HOME),  # Use OVO_HOME env var if set already
        )

    home_dir = os.path.abspath(os.path.expanduser(home_dir))

    while os.path.exists(home_dir):
        if yes:
            raise FileExistsError(f"Home directory already exists: {home_dir}")
        # show error f"Home directory already exists: {home_dir}"
        console.print(f"[red]Error:[/red] Home directory already exists: [bold]{home_dir}[/bold]")
        home_dir = Prompt.ask("Please choose a different path for the new OVO Home directory")
        home_dir = os.path.abspath(os.path.expanduser(home_dir))

    if not yes and home_dir != DEFAULT_OVO_HOME:
        if not Confirm.ask(f"Confirm directory: [bold]{home_dir}[/bold]"):
            console.print("Aborted")
            raise typer.Exit()

    if not default_profile:
        default_profile = "conda"
        if not yes:
            console.print("""
    OVO uses Nextflow to run workflows and manage software environments.
    How do you want the default OVO scheduler to manage dependencies?""")
            default_profile = Prompt.ask(
                "\nSelect profile, or press [bold]Enter[/bold] to select the default",
                choices=["conda", "singularity", "apptainer", "docker", "podman"],
                default=default_profile,
            )

    # ask about using conda when docker is not on PATH
    if not shutil.which(default_profile):
        console.print(
            f"[yellow]WARNING:[/yellow] {default_profile} not found on PATH, please make sure to install or activate {default_profile} or change the default scheduler profile (docker, singularity, apptainer, ...)"
        )

    config_props = ConfigProps()
    config_props.pyrosetta_license = yes or Confirm.ask(
        "\nEnable fastrelax? In case of commercial use, this requires a PyRosetta license"
    )

    admin_users = []
    if os.environ.get("USER"):
        # we don't want to flood the user with too many questions, enable by default
        admin_users.append(os.environ["USER"])

    os.makedirs(home_dir, exist_ok=True)

    config_path = save_default_config(
        home_dir=home_dir,
        config_props=config_props,
        default_profile=default_profile,
        admin_users=admin_users,
    )

    console.print(f"\n[green]✔[/green] Initialized OVO config: [bold]{config_path}[/bold]")

    if home_dir != DEFAULT_OVO_HOME and not no_env:
        console.print("\nYou will need to set the OVO_HOME environment variable to use this home directory.")
        export_command = f'export OVO_HOME="{home_dir}"'

        if (shell_config_path := get_shell_config_path()) and (
            yes or Confirm.ask(f"\nAdd the OVO_HOME dir to {shell_config_path}?")
        ):
            with open(shell_config_path, "a") as f:
                f.write(f"\n{export_command}")
            console.print(f"\n✔ Added to {shell_config_path}. Restart your terminal or run:")
            console.print(get_source_command())
        else:
            console.print("\nPlease set this environment variable manually:")
            console.print(f"[bold green]{export_command}[/bold green]")

    console.print("\nNext step: Initialize the preview workflow using [bold]ovo init preview[/bold]")


@app.command()
def preview():
    """Initialize nextflow, reference files and environment for the RFdiffusion preview workflow"""
    from ovo import config, local_scheduler

    # Initialize nextflow
    console.print("[bold]Initializing nextflow...[/bold]")
    init_nextflow()
    console.print("[bold][green]✔[/green] Nextflow initialized successfully[/bold]")

    # Download RFdiffusion base model weights
    download_files(destination_dir=config.reference_files_dir, file_list=RFDIFFUSION_MODEL_FILES)

    # Submit RFdiffusion preview (which also initializes the RFdiffusion conda environment)
    ovo_resources_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources"))
    process, job_id = local_scheduler.submit(
        "rfdiffusion-backbone",
        params={
            "contig": "A82-87/10/A92-97",
            "input_pdb": os.path.join(ovo_resources_path, "examples/inputs/5ELI_A.pdb"),
            "num_designs": 1,
            "run_parameters": "diffuser.T=2",
        },
        submission_args=dict(sync=True),
    )
    process.wait()
    if process.returncode == 0:
        console.print("[bold][green]✔[/green] RFdiffusion preview completed successfully[/bold]")
        console.print("Example unconditional design output saved to:")
        console.print(local_scheduler.get_output_dir(job_id))
    else:
        console.print("RFdiffusion workflow [red]FAILED[/red], please see errors above")
        exit(process.returncode)

    console.print("\nNext step: Set up end-to-end RFdiffusion workflow using [bold]ovo init rfdiffusion[/bold]")
    console.print("           Or already explore OVO web app using [bold]ovo app[/bold]")


@app.command()
def rfdiffusion(scheduler: str = None):
    """Initialize nextflow, reference files and environment for the RFdiffusion end-to-end workflow"""
    from ovo import config, get_scheduler

    # Initialize nextflow
    init_nextflow()

    # Download RFdiffusion base model weights
    download_files(destination_dir=config.reference_files_dir, file_list=RFDIFFUSION_MODEL_FILES)

    # Download AlphaFold weights
    download_files(destination_dir=config.reference_files_dir, file_list=ALPHAFOLD_MODEL_FILES)

    scheduler = get_scheduler(scheduler_key=scheduler or config.default_scheduler)

    # Submit RFdiffusion scaffold end-to-end workflows
    ovo_resources_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources"))
    process, job_id = scheduler.submit(
        "rfdiffusion-end-to-end",
        params={
            "rfdiffusion_contig": "A82-87/10/A92-97",
            "rfdiffusion_input_pdb": os.path.join(ovo_resources_path, "examples/inputs/5ELI_A.pdb"),
            "rfdiffusion_num_designs": 1,
            "rfdiffusion_run_parameters": "diffuser.T=2",
            "mpnn_num_sequences": 2,
            "design_type": "scaffold",
            "refolding_tests": "af2_model_1_ptm_ft_1rec",
        },
        submission_args=dict(sync=True),
    )
    process.wait()
    if process.returncode == 0:
        console.print("[bold][green]✔[/green] RFdiffusion scaffold preview completed successfully[/bold]")
        console.print("Example scaffold design output saved to:")
        console.print(scheduler.get_output_dir(job_id))
    else:
        console.print("RFdiffusion workflow [red]FAILED[/red], please see errors above")
        exit(process.returncode)

    # Submit RFdiffusion binder end-to-end workflow with LigandMPNN
    process, job_id = scheduler.submit(
        "rfdiffusion-end-to-end",
        params={
            "rfdiffusion_contig": "A20-130/0 10",
            "rfdiffusion_input_pdb": os.path.join(ovo_resources_path, "examples/inputs/5ELI_A.pdb"),
            "rfdiffusion_num_designs": 1,
            "rfdiffusion_run_parameters": "diffuser.T=15",
            "mpnn_num_sequences": 2,
            "mpnn_fastrelax_cycles": 0,
            "disable_pyrosetta_scoring": not config.props.pyrosetta_license,
            "design_type": "binder",
            "refolding_tests": "af2_model_1_multimer_tt_3rec",
        },
        submission_args=dict(sync=True),
    )
    process.wait()
    if process.returncode == 0:
        console.print("[bold][green]✔[/green] RFdiffusion binder preview completed successfully[/bold]")
        console.print("Example binder design output saved to:")
        console.print(scheduler.get_output_dir(job_id))
    else:
        console.print("RFdiffusion workflow [red]FAILED[/red], please see errors above")
        exit(process.returncode)

    if config.props.pyrosetta_license:
        # Submit RFdiffusion binder end-to-end workflow with FastRelax
        process, job_id = scheduler.submit(
            "rfdiffusion-end-to-end",
            params={
                "rfdiffusion_contig": "A20-130/0 10",
                "rfdiffusion_input_pdb": os.path.join(ovo_resources_path, "examples/inputs/5ELI_A.pdb"),
                "rfdiffusion_num_designs": 1,
                "rfdiffusion_run_parameters": "diffuser.T=15",
                "mpnn_fastrelax_cycles": 1,
                "design_type": "binder",
                "refolding_tests": "af2_model_1_multimer_tt_3rec",
            },
            submission_args=dict(sync=True),
        )
        process.wait()
        if process.returncode == 0:
            console.print("[bold][green]✔[/green] RFdiffusion binder preview completed successfully[/bold]")
            console.print("Example binder design output saved to:")
            console.print(scheduler.get_output_dir(job_id))
        else:
            console.print("RFdiffusion workflow [red]FAILED[/red], please see errors above")
            exit(process.returncode)

    console.print("\nNext step: Run OVO web app using [bold]ovo app[/bold]")


@app.command()
def proteinqc(
    tool_keys: str = typer.Option(
        "all",
        "--tools",
        help="Comma-separated list of ProteinQC tools to use, or 'all' to use all available tools (supported by the scheduler)",
    ),
    scheduler: str = None,
):
    """Initialize nextflow, reference files and environment for the ProteinQC workflow"""
    from ovo import config, get_scheduler
    from ovo.core.database.models_proteinqc import ESM_1V, ESM_IF, PROTEINQC_TOOLS
    from ovo.core.logic.proteinqc_logic import get_available_tools

    # Initialize nextflow
    init_nextflow()

    scheduler = get_scheduler(scheduler_key=scheduler or config.default_scheduler)

    if tool_keys != "all":
        tool_keys = tool_keys.split(",")
        all_tools_by_key = {tool.tool_key: tool for tool in PROTEINQC_TOOLS}
        tools = []
        for key in tool_keys:
            if key not in all_tools_by_key:
                raise OVOCliError(
                    f"Invalid ProteinQC tool '{key}', available tools: {','.join(all_tools_by_key.keys())}"
                )
            tools.append(all_tools_by_key[key])
    else:
        tools = get_available_tools(PROTEINQC_TOOLS, scheduler)
        tool_keys = [tool.tool_key for tool in tools]

    # Download ESM1v weights
    if ESM_1V in tools:
        download_files(destination_dir=config.reference_files_dir, file_list=ESM1V_MODEL_FILES)

    # Download ESM-IF weights
    if ESM_IF in tools:
        download_files(destination_dir=config.reference_files_dir, file_list=ESM_IF_MODEL_FILES)

    # Submit ProteinQC workflow
    ovo_resources_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources"))
    input_path = os.path.join(ovo_resources_path, "examples/inputs/5ELI_A.pdb")

    chains = ["A"]
    process, job_id = scheduler.submit(
        "proteinqc",
        params={
            "input_pdb": input_path,
            "tools": ",".join(tool_keys),
            "chains": ",".join(chains),
        },
        submission_args=dict(sync=True),
    )
    process.wait()
    if process.returncode == 0:
        console.print("[bold][green]✔[/green] ProteinQC completed successfully[/bold]")
        console.print("Example ProteinQC output saved to:")
        console.print(scheduler.get_output_dir(job_id))
    else:
        console.print("ProteinQC workflow [red]FAILED[/red], please see errors above")
        exit(process.returncode)


if __name__ == "__main__":
    app()
