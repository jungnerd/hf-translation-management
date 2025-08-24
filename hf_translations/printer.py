import csv
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.table import Table

from .translations.document import Document
from .translations.summary import Summary


def print_table(summary: Summary, console: Console, limit: int = 10) -> None:
    """Print translation summary table to console."""
    
    # Main summary table
    table = Table(title=f"🌍 HF Translation Summary - {summary.lang.upper()}")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Count", style="magenta")
    table.add_column("Percentage", style="green")
    
    table.add_row("Files analyzed", str(summary.files_analyzed), "100%")
    table.add_row(
        "Files translated",
        str(summary.files_translated), 
        f"{summary.percentage_translated:.1f}%"
    )
    table.add_row(
        "Missing translation", 
        str(summary.files_missing_translation),
        f"{summary.percentage_missing_translation:.1f}%"
    )
    table.add_row(
        "Outdated translation",
        str(summary.files_outdated),
        f"{summary.percentage_outdated_translation:.1f}%"
    )
    
    console.print(table)
    console.print()

    # Missing translations table  
    missing_files = summary.first_missing_translation_files(limit)
    if missing_files:
        missing_table = Table(title=f"🔴 Top {len(missing_files)} Missing Translations")
        missing_table.add_column("File", style="red")
        missing_table.add_column("Status", style="yellow")
        
        for doc in missing_files:
            file_path = Path(doc.original_file).name
            missing_table.add_row(file_path, doc.status)
            
        console.print(missing_table)
        console.print()

    # Outdated translations table
    outdated_files = summary.first_outdated_files(limit)
    if outdated_files:
        outdated_table = Table(title=f"🟡 Top {len(outdated_files)} Outdated Translations")
        outdated_table.add_column("File", style="yellow")
        outdated_table.add_column("Original Date", style="blue")
        outdated_table.add_column("Translation Date", style="blue")
        outdated_table.add_column("Status", style="red")
        
        for doc in outdated_files:
            file_path = Path(doc.original_file).name
            orig_date = doc.original_commit.strftime("%Y-%m-%d") if doc.original_commit else "Unknown"
            trans_date = doc.translation_commit.strftime("%Y-%m-%d") if doc.translation_commit else "Unknown"
            outdated_table.add_row(file_path, orig_date, trans_date, doc.status)
            
        console.print(outdated_table)


def print_to_csv(summary: Summary) -> None:
    """Save translation summary to CSV file."""
    filename = f"hf-translations-{summary.lang}-{datetime.now().strftime('%Y%m%d')}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Header
        writer.writerow([
            "Original File",
            "Translation File", 
            "Translation Exists",
            "Original Commit Date",
            "Translation Commit Date",
            "Status",
            "Is Outdated"
        ])
        
        # Data rows
        for doc in summary.files:
            writer.writerow([
                doc.original_file,
                doc.translation_file or "",
                doc.translation_exists,
                doc.original_commit.isoformat() if doc.original_commit else "",
                doc.translation_commit.isoformat() if doc.translation_commit else "",
                doc.status,
                doc.translation_is_outdated
            ])
    
    print(f"📊 CSV report saved as: {filename}")