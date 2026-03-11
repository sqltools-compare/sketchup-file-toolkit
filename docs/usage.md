# Usage Guide

## Basic Usage

```bash
python main.py --input /path/to/files
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `--input`, `-i` | Input directory path |
| `--output`, `-o` | Output directory (default: ./output) |
| `--verbose`, `-v` | Enable verbose output |
| `--help` | Show help message |

## Examples

### Scan Directory

```bash
python main.py --input ~/Documents/sketchup
```

### Process with Custom Output

```bash
python main.py -i ./projects -o ./results -v
```

## Interactive Mode

Run without arguments for interactive mode:

```bash
python main.py
```

Follow the prompts to scan and process files.
