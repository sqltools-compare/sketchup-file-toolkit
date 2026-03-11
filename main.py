"""
sketchup-file-toolkit - Python library for working with SketchUp files

A toolkit for SketchUp users.
"""
import argparse
import sys
from pathlib import Path

from src.file_parser import FileParserManager


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Python library for working with SketchUp files"
    )
    parser.add_argument(
        "--input", "-i",
        type=str,
        help="Input path"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="./output",
        help="Output directory"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    try:
        manager = FileParserManager(verbose=args.verbose)
        
        if args.input:
            manager.process(args.input, args.output)
        else:
            manager.interactive()
            
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
