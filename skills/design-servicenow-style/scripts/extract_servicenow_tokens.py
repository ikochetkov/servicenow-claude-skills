#!/usr/bin/env python3
"""
ServiceNow Figma Design Token Extractor
========================================
Extracts design tokens, styles, components, and variables from ServiceNow's
official Figma libraries using the Figma REST API.

Usage:
    python extract_servicenow_tokens.py --token YOUR_FIGMA_PAT [--file-key KEY] [--all]

Outputs structured JSON and Markdown reference files for the design-servicenow-style skill.
"""

import argparse
import json
import os
import sys
import time
from collections import defaultdict
from pathlib import Path

import requests

API_BASE = "https://api.figma.com/v1"

# All 18 known ServiceNow Figma Community files
# Community file IDs - these are the COMMUNITY IDs, user needs to duplicate to get editable file keys
SERVICENOW_COMMUNITY_FILES = {
    # Workspace libraries
    "workspace-components": {
        "community_url": "https://www.figma.com/community/file/1557487797746155558",
        "name": "Workspace → Components and Variables",
        "category": "workspace",
        "description": "UIB components for Workspaces & WEP portals"
    },
    "workspace-ai": {
        "community_url": "https://www.figma.com/community/file/1496251077635557615",
        "name": "Workspace → AI Components (Now Assist)",
        "category": "workspace",
        "description": "AI/Now Assist experience components"
    },
    "workspace-icons": {
        "community_url": "https://www.figma.com/community/file/UNKNOWN_ICONS",
        "name": "Workspace → Icons and Illustrations",
        "category": "workspace",
        "description": "Icon and illustration assets"
    },
    "workspace-conversational": {
        "community_url": "https://www.figma.com/community/file/1426245135283868391",
        "name": "Workspace → Conversational Interfaces",
        "category": "workspace",
        "description": "Agent Chat & Virtual Agent patterns"
    },
    "workspace-dataviz": {
        "community_url": "https://www.figma.com/community/file/UNKNOWN_DATAVIZ",
        "name": "Workspace → Data Visualizations",
        "category": "workspace",
        "description": "Charts, graphs, and data visualization components"
    },
    "workspace-templates": {
        "community_url": "https://www.figma.com/community/file/UNKNOWN_WS_TEMPLATES",
        "name": "Workspace → Templates",
        "category": "workspace",
        "description": "Ready-made workspace page templates"
    },
    "workspace-risk": {
        "community_url": "https://www.figma.com/community/file/UNKNOWN_RISK",
        "name": "Workspace → Risk Management Templates",
        "category": "workspace",
        "description": "IRM/Risk Management specific templates"
    },
    "workspace-dashboards": {
        "community_url": "https://www.figma.com/community/file/UNKNOWN_DASHBOARDS",
        "name": "Workspace → Dashboard Templates",
        "category": "workspace",
        "description": "Dashboard layout templates"
    },
    # Native Mobile
    "mobile-components": {
        "community_url": "https://www.figma.com/community/file/1557467833531440055",
        "name": "Native Mobile → Components & Variables",
        "category": "mobile",
        "description": "iOS/Android native components"
    },
    "mobile-icons": {
        "community_url": "https://www.figma.com/community/file/UNKNOWN_MOBILE_ICONS",
        "name": "Native Mobile → Icons",
        "category": "mobile",
        "description": "Mobile icon assets"
    },
    # Employee Center
    "ec-components": {
        "community_url": "https://www.figma.com/community/file/1557465743354626993",
        "name": "Employee Center → Components and Variables",
        "category": "employee-center",
        "description": "Employee portal building blocks"
    },
    "ec-templates": {
        "community_url": "https://www.figma.com/community/file/1238626671513323851",
        "name": "Employee Center → Templates",
        "category": "employee-center",
        "description": "Ready-made EC page templates"
    },
    # Customer Portal
    "cp-components": {
        "community_url": "https://www.figma.com/community/file/1496241945222838495",
        "name": "Customer Portal → Components and Variables",
        "category": "customer-portal",
        "description": "Customer-facing portal components"
    },
    # Core UI
    "core-components": {
        "community_url": "https://www.figma.com/community/file/1426239265412275920",
        "name": "Core UI → Components and Variables",
        "category": "core-ui",
        "description": "Foundation components shared across frameworks"
    },
    "core-icons": {
        "community_url": "https://www.figma.com/community/file/UNKNOWN_CORE_ICONS",
        "name": "Core UI → Icons & Illustrations",
        "category": "core-ui",
        "description": "Shared icon and illustration library"
    },
    "core-templates": {
        "community_url": "https://www.figma.com/community/file/UNKNOWN_CORE_TEMPLATES",
        "name": "Core UI → Templates",
        "category": "core-ui",
        "description": "Core UI templates"
    },
    # Accessibility
    "accessibility": {
        "community_url": "https://www.figma.com/community/file/1238625834550173002",
        "name": "Accessibility Specifications",
        "category": "accessibility",
        "description": "Accessibility specs and guidelines"
    },
    # Now Assist (Yokohama)
    "now-assist": {
        "community_url": "https://www.figma.com/community/file/1496251077635557615",
        "name": "Workspace → Now Assist Components",
        "category": "workspace",
        "description": "Now Assist AI experience patterns"
    },
}


class FigmaExtractor:
    """Extracts design tokens and component data from Figma files."""

    def __init__(self, token: str, output_dir: str = "output"):
        self.token = token
        self.headers = {"X-Figma-Token": token}
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._request_count = 0
        self._last_request_time = 0

    def _rate_limit(self):
        """Respect Figma's rate limits (10 req/min for Starter Full seat)."""
        self._request_count += 1
        now = time.time()
        elapsed = now - self._last_request_time
        if elapsed < 6.5:  # ~9 req/min to stay safe
            time.sleep(6.5 - elapsed)
        self._last_request_time = time.time()

    def _get(self, url: str, params: dict = None) -> dict:
        """Make a rate-limited GET request to the Figma API."""
        self._rate_limit()
        full_url = f"{API_BASE}{url}"
        print(f"  → GET {full_url}")
        resp = requests.get(full_url, headers=self.headers, params=params)
        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 60))
            print(f"  ⚠ Rate limited. Waiting {retry_after}s...")
            time.sleep(retry_after)
            return self._get(url, params)
        resp.raise_for_status()
        return resp.json()

    def get_file(self, file_key: str, depth: int = 2) -> dict:
        """Get file structure with limited depth to avoid huge responses."""
        return self._get(f"/files/{file_key}", params={"depth": depth})

    def get_file_styles(self, file_key: str) -> dict:
        """Get all published styles in a file."""
        return self._get(f"/files/{file_key}/styles")

    def get_file_components(self, file_key: str) -> dict:
        """Get all components in a file."""
        return self._get(f"/files/{file_key}/components")

    def get_file_component_sets(self, file_key: str) -> dict:
        """Get all component sets (variant groups) in a file."""
        return self._get(f"/files/{file_key}/component_sets")

    def get_nodes(self, file_key: str, node_ids: list) -> dict:
        """Get specific nodes by ID."""
        ids = ",".join(node_ids)
        return self._get(f"/files/{file_key}/nodes", params={"ids": ids})

    def get_file_deep(self, file_key: str) -> dict:
        """Get full file content (WARNING: can be very large)."""
        return self._get(f"/files/{file_key}")

    # ── Token Extraction ──────────────────────────────────────────────

    def extract_colors_from_styles(self, styles_data: dict) -> list:
        """Extract color tokens from style metadata."""
        colors = []
        for style in styles_data.get("meta", {}).get("styles", []):
            if style.get("style_type") == "FILL":
                colors.append({
                    "name": style.get("name", ""),
                    "description": style.get("description", ""),
                    "key": style.get("key", ""),
                    "node_id": style.get("node_id", ""),
                })
        return colors

    def extract_text_styles(self, styles_data: dict) -> list:
        """Extract typography tokens from style metadata."""
        text_styles = []
        for style in styles_data.get("meta", {}).get("styles", []):
            if style.get("style_type") == "TEXT":
                text_styles.append({
                    "name": style.get("name", ""),
                    "description": style.get("description", ""),
                    "key": style.get("key", ""),
                    "node_id": style.get("node_id", ""),
                })
        return text_styles

    def extract_effect_styles(self, styles_data: dict) -> list:
        """Extract shadow/effect tokens from style metadata."""
        effects = []
        for style in styles_data.get("meta", {}).get("styles", []):
            if style.get("style_type") == "EFFECT":
                effects.append({
                    "name": style.get("name", ""),
                    "description": style.get("description", ""),
                    "key": style.get("key", ""),
                    "node_id": style.get("node_id", ""),
                })
        return effects

    def extract_components(self, components_data: dict) -> list:
        """Extract component metadata."""
        components = []
        for comp in components_data.get("meta", {}).get("components", []):
            components.append({
                "name": comp.get("name", ""),
                "description": comp.get("description", ""),
                "key": comp.get("key", ""),
                "node_id": comp.get("node_id", ""),
                "containing_frame": comp.get("containing_frame", {}).get("name", ""),
            })
        return components

    def extract_component_sets(self, sets_data: dict) -> list:
        """Extract component set (variant group) metadata."""
        sets = []
        for cs in sets_data.get("meta", {}).get("component_sets", []):
            sets.append({
                "name": cs.get("name", ""),
                "description": cs.get("description", ""),
                "key": cs.get("key", ""),
                "node_id": cs.get("node_id", ""),
            })
        return sets

    def extract_color_values_from_nodes(self, file_data: dict) -> list:
        """Walk the file tree to extract actual color values from fill styles."""
        colors = []
        self._walk_tree(file_data.get("document", {}), colors)
        return colors

    def _walk_tree(self, node: dict, colors: list, depth: int = 0):
        """Recursively walk the Figma node tree extracting style info."""
        # Extract fills with color values
        if "fills" in node:
            for fill in node["fills"]:
                if fill.get("type") == "SOLID" and "color" in fill:
                    c = fill["color"]
                    r, g, b = int(c["r"] * 255), int(c["g"] * 255), int(c["b"] * 255)
                    a = c.get("a", 1)
                    hex_val = f"#{r:02x}{g:02x}{b:02x}"
                    rgb_val = f"{r},{g},{b}"
                    colors.append({
                        "node_name": node.get("name", ""),
                        "node_type": node.get("type", ""),
                        "hex": hex_val,
                        "rgb": rgb_val,
                        "opacity": a,
                    })

        # Extract text style info
        if node.get("type") == "TEXT" and "style" in node:
            style = node["style"]
            colors.append({
                "node_name": node.get("name", ""),
                "node_type": "TEXT_STYLE",
                "font_family": style.get("fontFamily", ""),
                "font_size": style.get("fontSize", ""),
                "font_weight": style.get("fontWeight", ""),
                "line_height": style.get("lineHeightPx", ""),
                "letter_spacing": style.get("letterSpacing", ""),
            })

        # Recurse into children
        for child in node.get("children", []):
            if depth < 10:  # Prevent infinite recursion
                self._walk_tree(child, colors, depth + 1)

    # ── Full Extraction Pipeline ──────────────────────────────────────

    def extract_library(self, file_key: str, library_id: str, library_info: dict) -> dict:
        """Extract all tokens from a single Figma library file."""
        print(f"\n{'='*60}")
        print(f"Extracting: {library_info['name']}")
        print(f"File key: {file_key}")
        print(f"{'='*60}")

        result = {
            "library_id": library_id,
            "name": library_info["name"],
            "category": library_info["category"],
            "description": library_info["description"],
            "community_url": library_info["community_url"],
            "file_key": file_key,
            "extracted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

        # 1. Get styles
        try:
            print("\n[1/4] Fetching styles...")
            styles = self.get_file_styles(file_key)
            result["color_styles"] = self.extract_colors_from_styles(styles)
            result["text_styles"] = self.extract_text_styles(styles)
            result["effect_styles"] = self.extract_effect_styles(styles)
            print(f"  Found: {len(result['color_styles'])} colors, "
                  f"{len(result['text_styles'])} text styles, "
                  f"{len(result['effect_styles'])} effects")
        except Exception as e:
            print(f"  ✗ Styles failed: {e}")
            result["color_styles"] = []
            result["text_styles"] = []
            result["effect_styles"] = []

        # 2. Get components
        try:
            print("\n[2/4] Fetching components...")
            components = self.get_file_components(file_key)
            result["components"] = self.extract_components(components)
            print(f"  Found: {len(result['components'])} components")
        except Exception as e:
            print(f"  ✗ Components failed: {e}")
            result["components"] = []

        # 3. Get component sets
        try:
            print("\n[3/4] Fetching component sets...")
            sets = self.get_file_component_sets(file_key)
            result["component_sets"] = self.extract_component_sets(sets)
            print(f"  Found: {len(result['component_sets'])} component sets")
        except Exception as e:
            print(f"  ✗ Component sets failed: {e}")
            result["component_sets"] = []

        # 4. Get file structure (limited depth for overview)
        try:
            print("\n[4/4] Fetching file structure (depth=2)...")
            file_data = self.get_file(file_key, depth=2)
            result["file_name"] = file_data.get("name", "")
            result["last_modified"] = file_data.get("lastModified", "")
            result["version"] = file_data.get("version", "")

            # Extract page names as table of contents
            pages = []
            doc = file_data.get("document", {})
            for page in doc.get("children", []):
                page_info = {
                    "name": page.get("name", ""),
                    "id": page.get("id", ""),
                    "child_count": len(page.get("children", [])),
                }
                pages.append(page_info)
            result["pages"] = pages
            print(f"  Found: {len(pages)} pages")
        except Exception as e:
            print(f"  ✗ File structure failed: {e}")
            result["pages"] = []

        return result

    def extract_deep_tokens(self, file_key: str, page_node_ids: list) -> dict:
        """Extract deep color/typography values from specific pages."""
        print(f"\n  Extracting deep tokens from {len(page_node_ids)} pages...")
        all_tokens = []
        for node_id in page_node_ids[:5]:  # Limit to 5 pages to manage API calls
            try:
                nodes = self.get_nodes(file_key, [node_id])
                for nid, node_data in nodes.get("nodes", {}).items():
                    doc = node_data.get("document", {})
                    tokens = []
                    self._walk_tree(doc, tokens)
                    all_tokens.extend(tokens)
            except Exception as e:
                print(f"  ✗ Node {node_id} failed: {e}")
        return all_tokens

    # ── Output Generation ─────────────────────────────────────────────

    def save_json(self, data: dict, filename: str):
        """Save extracted data as JSON."""
        path = self.output_dir / filename
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"  Saved: {path}")

    def save_markdown_reference(self, data: dict, filename: str):
        """Generate a Markdown reference file from extracted data."""
        path = self.output_dir / filename
        lib = data

        lines = [
            f"# {lib['name']}",
            f"",
            f"**Category:** {lib['category']}",
            f"**Description:** {lib['description']}",
            f"**Community URL:** {lib['community_url']}",
            f"**Last Modified:** {lib.get('last_modified', 'N/A')}",
            f"**Version:** {lib.get('version', 'N/A')}",
            f"",
        ]

        # Pages / Table of Contents
        if lib.get("pages"):
            lines.append("## Pages")
            lines.append("")
            for p in lib["pages"]:
                lines.append(f"- **{p['name']}** (ID: {p['id']}, {p['child_count']} children)")
            lines.append("")

        # Color Styles
        if lib.get("color_styles"):
            lines.append(f"## Color Styles ({len(lib['color_styles'])} total)")
            lines.append("")
            lines.append("| Name | Description |")
            lines.append("|------|-------------|")
            for s in sorted(lib["color_styles"], key=lambda x: x["name"]):
                desc = s["description"].replace("\n", " ").replace("|", "\\|") if s["description"] else ""
                lines.append(f"| `{s['name']}` | {desc} |")
            lines.append("")

        # Text Styles
        if lib.get("text_styles"):
            lines.append(f"## Text Styles ({len(lib['text_styles'])} total)")
            lines.append("")
            lines.append("| Name | Description |")
            lines.append("|------|-------------|")
            for s in sorted(lib["text_styles"], key=lambda x: x["name"]):
                desc = s["description"].replace("\n", " ").replace("|", "\\|") if s["description"] else ""
                lines.append(f"| `{s['name']}` | {desc} |")
            lines.append("")

        # Effect Styles
        if lib.get("effect_styles"):
            lines.append(f"## Effect Styles ({len(lib['effect_styles'])} total)")
            lines.append("")
            lines.append("| Name | Description |")
            lines.append("|------|-------------|")
            for s in sorted(lib["effect_styles"], key=lambda x: x["name"]):
                desc = s["description"].replace("\n", " ").replace("|", "\\|") if s["description"] else ""
                lines.append(f"| `{s['name']}` | {desc} |")
            lines.append("")

        # Component Sets (variant groups)
        if lib.get("component_sets"):
            lines.append(f"## Component Sets ({len(lib['component_sets'])} total)")
            lines.append("")
            lines.append("| Name | Description |")
            lines.append("|------|-------------|")
            for cs in sorted(lib["component_sets"], key=lambda x: x["name"]):
                desc = cs["description"].replace("\n", " ").replace("|", "\\|") if cs["description"] else ""
                lines.append(f"| `{cs['name']}` | {desc} |")
            lines.append("")

        # Components
        if lib.get("components"):
            lines.append(f"## Components ({len(lib['components'])} total)")
            lines.append("")
            # Group by containing frame
            by_frame = defaultdict(list)
            for c in lib["components"]:
                frame = c.get("containing_frame", "Ungrouped") or "Ungrouped"
                by_frame[frame].append(c)

            for frame_name in sorted(by_frame.keys()):
                comps = by_frame[frame_name]
                lines.append(f"### {frame_name} ({len(comps)} components)")
                lines.append("")
                for c in sorted(comps, key=lambda x: x["name"]):
                    desc = f" — {c['description']}" if c.get("description") else ""
                    lines.append(f"- `{c['name']}`{desc}")
                lines.append("")

        with open(path, "w") as f:
            f.write("\n".join(lines))
        print(f"  Saved: {path}")


def main():
    parser = argparse.ArgumentParser(description="Extract ServiceNow Figma design tokens")
    parser.add_argument("--token", required=False, default="", help="Figma Personal Access Token")
    parser.add_argument("--file-key", help="Extract a single file by key")
    parser.add_argument("--library-id", help="Library ID from the catalog (e.g., 'workspace-components')")
    parser.add_argument("--output-dir", default="output", help="Output directory")
    parser.add_argument("--list-libraries", action="store_true", help="List all known ServiceNow libraries")
    parser.add_argument("--deep", action="store_true", help="Extract deep token values (more API calls)")
    parser.add_argument("--file-keys-json", help="Path to JSON file mapping library_id -> file_key")

    args = parser.parse_args()

    if args.list_libraries:
        print("\nServiceNow Figma Libraries:")
        print("=" * 60)
        for lid, info in SERVICENOW_COMMUNITY_FILES.items():
            print(f"\n  {lid}:")
            print(f"    Name: {info['name']}")
            print(f"    Category: {info['category']}")
            print(f"    URL: {info['community_url']}")
        return

    extractor = FigmaExtractor(args.token, args.output_dir)

    # Single file extraction
    if args.file_key:
        lib_id = args.library_id or "custom"
        lib_info = SERVICENOW_COMMUNITY_FILES.get(lib_id, {
            "name": "Custom File",
            "category": "custom",
            "description": "User-specified file",
            "community_url": "",
        })

        result = extractor.extract_library(args.file_key, lib_id, lib_info)

        # Optionally extract deep token values
        if args.deep and result.get("pages"):
            page_ids = [p["id"] for p in result["pages"]]
            deep_tokens = extractor.extract_deep_tokens(args.file_key, page_ids)
            result["deep_tokens"] = deep_tokens

        extractor.save_json(result, f"{lib_id}.json")
        extractor.save_markdown_reference(result, f"{lib_id}.md")

        print(f"\n✓ Extraction complete for {lib_info['name']}")
        return

    # Batch extraction from JSON mapping file
    if args.file_keys_json:
        with open(args.file_keys_json) as f:
            file_keys = json.load(f)

        all_results = {}
        for lib_id, file_key in file_keys.items():
            if lib_id in SERVICENOW_COMMUNITY_FILES:
                lib_info = SERVICENOW_COMMUNITY_FILES[lib_id]
            else:
                lib_info = {
                    "name": lib_id,
                    "category": "unknown",
                    "description": "",
                    "community_url": "",
                }

            result = extractor.extract_library(file_key, lib_id, lib_info)
            all_results[lib_id] = result

            extractor.save_json(result, f"{lib_id}.json")
            extractor.save_markdown_reference(result, f"{lib_id}.md")

        # Generate combined catalog
        generate_catalog(all_results, extractor.output_dir)
        print(f"\n✓ Batch extraction complete. {len(all_results)} libraries processed.")
        return

    print("Please specify --file-key, --file-keys-json, or --list-libraries")
    print("Run with --help for usage information.")


def generate_catalog(all_results: dict, output_dir: Path):
    """Generate a combined catalog of all extracted libraries."""
    lines = [
        "# ServiceNow Figma Library Catalog",
        "",
        "Complete inventory of ServiceNow's official Figma design libraries.",
        "Extracted from Figma community files using the REST API.",
        "",
        f"**Total Libraries:** {len(all_results)}",
        f"**Extracted:** {time.strftime('%Y-%m-%d')}",
        "",
        "## Libraries by Category",
        "",
    ]

    by_category = defaultdict(list)
    for lid, data in all_results.items():
        by_category[data["category"]].append(data)

    total_components = 0
    total_styles = 0

    for cat in sorted(by_category.keys()):
        libs = by_category[cat]
        lines.append(f"### {cat.replace('-', ' ').title()}")
        lines.append("")

        for lib in libs:
            n_comp = len(lib.get("components", []))
            n_sets = len(lib.get("component_sets", []))
            n_colors = len(lib.get("color_styles", []))
            n_text = len(lib.get("text_styles", []))
            n_fx = len(lib.get("effect_styles", []))

            total_components += n_comp
            total_styles += n_colors + n_text + n_fx

            lines.append(f"**{lib['name']}**")
            lines.append(f"- Components: {n_comp} ({n_sets} variant groups)")
            lines.append(f"- Styles: {n_colors} color, {n_text} text, {n_fx} effect")
            lines.append(f"- Community: {lib['community_url']}")
            lines.append(f"- Reference: [{lib['library_id']}.md](./{lib['library_id']}.md)")
            lines.append("")

    lines.insert(7, f"**Total Components:** {total_components}")
    lines.insert(8, f"**Total Styles:** {total_styles}")
    lines.insert(9, "")

    path = output_dir / "catalog.md"
    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"  Saved catalog: {path}")

    # Also save as JSON
    path_json = output_dir / "catalog.json"
    with open(path_json, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"  Saved catalog JSON: {path_json}")


if __name__ == "__main__":
    main()
