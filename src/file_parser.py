"""
FileParserManager - Core functionality for SketchUp file-parser.
"""
import os
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime


class FileParserManager:
    """
    Python library for working with SketchUp files
    
    Attributes:
        verbose: Enable verbose output
        config: Configuration dictionary
    """
    
    def __init__(self, verbose: bool = False, config_path: Optional[str] = None):
        """
        Initialize the FileParserManager.
        
        Args:
            verbose: Enable verbose logging
            config_path: Path to configuration file
        """
        self.verbose = verbose
        self.config = self._load_config(config_path)
        self._cache: Dict[str, Any] = {}
        
        if self.verbose:
            print(f"[FileParserManager] Initialized")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        default_config = {
            "version": "1.0.0",
            "software": "SketchUp",
            "extensions": ['.blend', '.max', '.c4d', '.obj', '.fbx', '.stl'],
            "output_format": "json",
            "max_items": 1000,
        }
        
        if config_path and Path(config_path).exists():
            with open(config_path, "r") as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        return default_config
    
    def _log(self, message: str):
        """Log message if verbose mode is enabled."""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {message}")
    
    def scan(self, path: str) -> List[Dict[str, Any]]:
        """
        Scan directory for SketchUp files.
        
        Args:
            path: Directory path to scan
            
        Returns:
            List of found items with metadata
        """
        results = []
        scan_path = Path(path)
        
        if not scan_path.exists():
            raise FileNotFoundError(f"Path not found: {path}")
        
        self._log(f"Scanning: {path}")
        
        extensions = self.config.get("extensions", [])
        
        for ext in extensions:
            for file_path in scan_path.rglob(f"*{ext}"):
                item = {
                    "path": str(file_path),
                    "name": file_path.stem,
                    "extension": file_path.suffix,
                    "size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(
                        file_path.stat().st_mtime
                    ).isoformat(),
                }
                results.append(item)
                self._log(f"Found: {file_path.name}")
        
        self._log(f"Total items found: {len(results)}")
        return results
    
    def process(self, input_path: str, output_path: str = "./output") -> Dict[str, Any]:
        """
        Process files from input path.
        
        Args:
            input_path: Source directory
            output_path: Destination directory
            
        Returns:
            Processing results summary
        """
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        self._log(f"Processing: {input_path} -> {output_path}")
        
        items = self.scan(input_path)
        
        results = {
            "processed": 0,
            "skipped": 0,
            "errors": 0,
            "items": [],
        }
        
        for item in items:
            try:
                processed_item = self._process_item(item)
                results["items"].append(processed_item)
                results["processed"] += 1
            except Exception as e:
                self._log(f"Error processing {item['name']}: {e}")
                results["errors"] += 1
        
        report_path = output_dir / "report.json"
        with open(report_path, "w") as f:
            json.dump(results, f, indent=2)
        
        self._log(f"Report saved: {report_path}")
        print(f"\nProcessed: {results['processed']} items")
        print(f"Errors: {results['errors']}")
        
        return results
    
    def _process_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single item."""
        return {
            **item,
            "processed": True,
            "processed_at": datetime.now().isoformat(),
        }
    
    def interactive(self):
        """Run in interactive mode."""
        print(f"\n=== FileParserManager Interactive Mode ===")
        print(f"Software: SketchUp")
        print(f"Extensions: {', '.join(self.config.get('extensions', []))}")
        print()
        
        while True:
            try:
                path = input("Enter path to scan (or 'quit'): ").strip()
                
                if path.lower() in ("quit", "exit", "q"):
                    print("Goodbye!")
                    break
                
                if not path:
                    continue
                
                items = self.scan(path)
                print(f"\nFound {len(items)} items:")
                
                for i, item in enumerate(items[:10], 1):
                    print(f"  {i}. {item['name']} ({item['size']} bytes)")
                
                if len(items) > 10:
                    print(f"  ... and {len(items) - 10} more")
                
                print()
                
            except FileNotFoundError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Error: {e}")
    
    def export(self, items: List[Dict], output_path: str, format: str = "json"):
        """
        Export items to file.
        
        Args:
            items: List of items to export
            output_path: Output file path
            format: Export format (json, csv)
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        if format == "json":
            with open(output_file, "w") as f:
                json.dump(items, f, indent=2)
        elif format == "csv":
            import csv
            if items:
                with open(output_file, "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=items[0].keys())
                    writer.writeheader()
                    writer.writerows(items)
        
        self._log(f"Exported {len(items)} items to {output_path}")
