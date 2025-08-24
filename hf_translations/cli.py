from typing import Annotated

import typer
from rich.console import Console

from hf_translations import printer
from hf_translations.translations import HFLanguages, Summary

console = Console()

app = typer.Typer(
    rich_markup_mode="rich",
    help="🤗 Hugging Face Documentation Translation Status Checker"
)


@app.command("report")
def report(
    lang: Annotated[
        HFLanguages,
        typer.Option(
            ...,
            "--language",
            "-l",
            help="The language to check for translation status",
        ),
    ],
    repo_url: Annotated[
        str,
        typer.Option(
            "--repo",
            "-r", 
            help="HuggingFace repository URL to analyze"
        ),
    ] = "https://github.com/huggingface/transformers.git",
    save_csv: Annotated[
        bool,
        typer.Option(
            "--csv",
            "-c",
            help="Save detailed report to CSV file",
        ),
    ] = False,
    limit: Annotated[
        int,
        typer.Option(
            "--limit",
            help="Number of files to show in each category"
        )
    ] = 10,
) -> None:
    """Generate a translation status report for HF documentation."""
    console.clear()
    console.print(f"🔍 Analyzing translations for [bold cyan]{lang.value}[/bold cyan]")
    console.print(f"📂 Repository: [blue]{repo_url}[/blue]")
    console.print()
    
    summary = Summary(lang=lang.value, repo_url=repo_url)
    
    try:
        summary.generate()
        printer.print_table(summary, console, limit)
        
        if save_csv:
            printer.print_to_csv(summary)
            
    except Exception as e:
        console.print(f"❌ Error: {str(e)}", style="red")
        raise typer.Exit(1)


@app.command("list-repos") 
def list_repos() -> None:
    """List common HuggingFace repositories that support translations."""
    repos = [
        "https://github.com/huggingface/transformers.git",
        "https://github.com/huggingface/diffusers.git", 
        "https://github.com/huggingface/datasets.git",
        "https://github.com/huggingface/accelerate.git",
        "https://github.com/huggingface/peft.git",
    ]
    
    console.print("🤗 [bold]Common HuggingFace repositories:[/bold]")
    for repo in repos:
        console.print(f"  • {repo}")


@app.command("languages")
def list_languages() -> None:
    """List supported languages for translation checking."""
    console.print("🌍 [bold]Supported languages:[/bold]")
    for lang in HFLanguages:
        console.print(f"  • {lang.value} ({lang.name})")


def main() -> None:
    app()