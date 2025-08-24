# HF Translations Management

Easy management for translations of Hugging Face project documentation.

## Acknowledgments

This project is heavily based on and adapted from [fastapi-translations-management](https://github.com/ceb10n/fastapi-translations-management) by [@ceb10n](https://github.com/ceb10n). The core architecture, CLI structure, and workflow were inspired by their excellent translation management system. We've modified and extended it specifically for Hugging Face repositories and documentation structure.

**Original inspiration**: [fastapi-translations-management](https://github.com/ceb10n/fastapi-translations-management) - Special thanks to @ceb10n for the foundational approach.

## Who's this library for?

This is a utility package for contributors working on Hugging Face documentation translations. It helps you:

- Track translation progress across HF repositories
- Identify missing translations
- Find outdated translations that need updating
- Generate reports in table and CSV format

## Installation

Install using pip:

```bash
pip install -e .
```

## Usage

After installation, you'll have access to the `hf-translations` command.

### Basic Usage

Check translation status for Korean in Transformers repo:
```bash
hf-translations report -l ko
```

Check a different repository:
```bash
hf-translations report -l ko -r https://github.com/huggingface/diffusers.git
```

Save detailed results to CSV:
```bash
hf-translations report -l ko -c
```

### Available Commands

- `hf-translations report` - Generate translation status report
- `hf-translations languages` - List supported languages  
- `hf-translations list-repos` - Show common HF repositories

### Command Options

- `-l, --language` - Target language code (required)
- `-r, --repo` - HuggingFace repository URL (default: transformers)
- `-c, --csv` - Save results to CSV file
- `--limit` - Number of files to show in each category (default: 10)

## Supported Languages

The tool supports common languages found in HF documentation:

- `ko` - Korean
- `ja` - Japanese  
- `zh` - Chinese (Simplified)
- `fr` - French
- `es` - Spanish
- `de` - German
- And many more...

Use `hf-translations languages` to see the full list.

## Output

The tool provides:

1. **Summary Table** - Overview of translation progress
2. **Missing Files** - Files that need translation
3. **Outdated Files** - Translations that need updating  
4. **CSV Export** - Detailed data for further analysis

## Development

```bash
# Clone the repository
git clone <your-repo-url>
cd hf_translations_management

# Install in development mode
pip install -e .

# Run the tool
hf-translations --help
```

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

MIT License

## Credits

- Original concept and architecture from [fastapi-translations-management](https://github.com/ceb10n/fastapi-translations-management) by [@ceb10n](https://github.com/ceb10n)
- Adapted and extended for Hugging Face ecosystem by [@jungnerd](https://github.com/jungnerd)