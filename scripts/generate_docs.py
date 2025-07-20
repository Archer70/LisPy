#!/usr/bin/env python3
"""
LisPy Documentation Generator

Scans function and special form definitions to generate a static documentation site.

Usage:
    python scripts/generate_docs.py                    # Generate full docs
    python scripts/generate_docs.py --preview add map  # Generate specific functions
    python scripts/generate_docs.py --serve            # Generate and serve locally
"""

import argparse
import http.server
import os
import socketserver
import sys
from pathlib import Path

# Add the project root to the path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import the modular components
from doc_generator import DocumentationScanner, HTMLGenerator


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate LisPy documentation")
    parser.add_argument(
        "--preview", nargs="*", help="Generate docs for specific functions only"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate docs for all available functions and special forms",
    )
    parser.add_argument(
        "--serve", action="store_true", help="Start local server after generation"
    )
    parser.add_argument("--output", default="docs/generated", help="Output directory")

    args = parser.parse_args()

    project_root = PROJECT_ROOT
    scanner = DocumentationScanner(project_root)
    generator = HTMLGenerator(
        Path(args.output), project_root / "docs" / "templates", project_root
    )

    try:
        if args.all:
            # Generate all available documentation
            print(
                "Generating documentation for all available functions and special forms..."
            )
            docs = scanner.scan_functions()
        elif args.preview is not None:
            if args.preview:
                # Generate only specified functions
                print(f"Generating documentation for: {', '.join(args.preview)}")
                docs = scanner.scan_specific_functions(args.preview)
            else:
                # --preview with no arguments means use default preview functions
                print("Generating preview documentation for: add, map")
                docs = scanner.scan_specific_functions(["add", "map"])
        elif args.serve:
            # If --serve is used alone, generate all docs first
            print(
                "Generating documentation for all available functions and special forms..."
            )
            docs = scanner.scan_functions()
        else:
            # Default behavior - show help
            parser.print_help()
            return

        if not docs:
            print("No documentation found!")
            return

        generator.generate_site(docs)

        if args.serve:
            # Start simple HTTP server for local testing
            os.chdir(args.output)

            # Try to find an available port starting from 8000
            port = 8000
            max_attempts = 10

            for attempt in range(max_attempts):
                try:
                    with socketserver.TCPServer(
                        ("", port), http.server.SimpleHTTPRequestHandler
                    ) as httpd:
                        print(f"✅ Documentation server started successfully!")
                        print(f"🌐 View documentation at: http://localhost:{port}")
                        print(f"📁 Serving from: {os.getcwd()}")
                        print(f"🔍 Search functionality: Available")
                        print(
                            f"📊 Total functions documented: {len(docs) if 'docs' in locals() else 'Unknown'}"
                        )
                        print()
                        print("💡 Tips:")
                        print(
                            "   • The server is running in the foreground (this is normal)"
                        )
                        print(
                            "   • Open http://localhost:{} in your browser".format(port)
                        )
                        print(
                            "   • Try the search functionality with terms like 'map', '+', or 'filter'"
                        )
                        print("   • Press Ctrl+C to stop the server")
                        print()
                        try:
                            httpd.serve_forever()
                        except KeyboardInterrupt:
                            print("\n🛑 Server stopped gracefully.")
                            return
                except OSError as e:
                    if e.errno == 10048 or "Address already in use" in str(e):
                        print(f"Port {port} is already in use, trying {port + 1}...")
                        port += 1
                        continue
                    else:
                        raise e

            print(f"Could not find an available port after trying ports 8000-{port-1}")
            print(
                "Please close other applications using these ports or specify a different port."
            )

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
