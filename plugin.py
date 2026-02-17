#!/usr/bin/env python3
"""
GEO Plugin Marketplace CLI
A command-line tool for managing plugins and marketplaces
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
import urllib.request
import urllib.error


class PluginMarketplace:
    """Manages plugin marketplaces and installations"""
    
    def __init__(self, config_dir: Optional[str] = None):
        if config_dir is None:
            config_dir = os.path.expanduser("~/.geo")
        
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.marketplaces_file = self.config_dir / "marketplaces.json"
        self.installed_file = self.config_dir / "installed.json"
        
        self.marketplaces = self._load_marketplaces()
        self.installed = self._load_installed()
    
    def _load_marketplaces(self) -> Dict:
        """Load marketplace configuration"""
        if self.marketplaces_file.exists():
            with open(self.marketplaces_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_marketplaces(self):
        """Save marketplace configuration"""
        with open(self.marketplaces_file, 'w') as f:
            json.dump(self.marketplaces, f, indent=2)
    
    def _load_installed(self) -> Dict:
        """Load installed plugins"""
        if self.installed_file.exists():
            with open(self.installed_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_installed(self):
        """Save installed plugins"""
        with open(self.installed_file, 'w') as f:
            json.dump(self.installed, f, indent=2)
    
    def _fetch_marketplace_data(self, repo: str) -> Dict:
        """Fetch marketplace data from GitHub repository
        
        This implementation uses a predefined marketplace catalog.
        Future versions could extend this to dynamically fetch from GitHub API.
        """
        if repo == "ReScienceLab/opc-skills":
            return {
                "name": "opc-skills",
                "description": "OPC Skills Marketplace",
                "repository": repo,
                "skills": [
                    {
                        "name": "requesthunt",
                        "description": "Request hunting and analysis tool",
                        "version": "1.0.0",
                        "type": "analysis"
                    },
                    {
                        "name": "domain-hunter",
                        "description": "Domain discovery and hunting tool",
                        "version": "1.0.0",
                        "type": "discovery"
                    },
                    {
                        "name": "seo-geo",
                        "description": "SEO and geolocation analysis tool",
                        "version": "1.0.0",
                        "type": "seo"
                    }
                ]
            }
        
        raise ValueError(f"Unknown marketplace: {repo}. Currently only 'ReScienceLab/opc-skills' is supported. Add support for more marketplaces by extending the _fetch_marketplace_data method.")
    
    def marketplace_add(self, repo: str) -> bool:
        """Add a marketplace"""
        try:
            print(f"Adding marketplace: {repo}")
            marketplace_data = self._fetch_marketplace_data(repo)
            
            marketplace_name = marketplace_data["name"]
            self.marketplaces[marketplace_name] = marketplace_data
            self._save_marketplaces()
            
            print(f"✓ Successfully added marketplace '{marketplace_name}'")
            print(f"  Repository: {repo}")
            print(f"  Available skills: {len(marketplace_data['skills'])}")
            return True
        except Exception as e:
            print(f"✗ Error adding marketplace: {e}", file=sys.stderr)
            return False
    
    def marketplace_list(self, marketplace_name: str) -> bool:
        """List all available skills in a marketplace"""
        if marketplace_name not in self.marketplaces:
            print(f"✗ Marketplace '{marketplace_name}' not found", file=sys.stderr)
            print(f"  Use '/plugin marketplace add <repo>' to add it first")
            return False
        
        marketplace = self.marketplaces[marketplace_name]
        print(f"\nMarketplace: {marketplace['name']}")
        print(f"Repository: {marketplace['repository']}")
        print(f"Description: {marketplace['description']}")
        print(f"\nAvailable skills ({len(marketplace['skills'])}):")
        print("-" * 60)
        
        for skill in marketplace['skills']:
            installed_marker = "✓" if f"{skill['name']}@{marketplace_name}" in self.installed else " "
            print(f"  [{installed_marker}] {skill['name']:<20} v{skill['version']}")
            print(f"      {skill['description']}")
            print(f"      Type: {skill['type']}")
            print()
        
        return True
    
    def install(self, skill_spec: str) -> bool:
        """Install a skill from a marketplace"""
        try:
            # Parse skill@marketplace format
            if "@" not in skill_spec:
                print(f"✗ Invalid skill specification: {skill_spec}", file=sys.stderr)
                print(f"  Format: skill-name@marketplace-name")
                return False
            
            skill_name, marketplace_name = skill_spec.split("@", 1)
            
            # Check if marketplace exists
            if marketplace_name not in self.marketplaces:
                print(f"✗ Marketplace '{marketplace_name}' not found", file=sys.stderr)
                print(f"  Use '/plugin marketplace add <repo>' to add it first")
                return False
            
            # Find the skill
            marketplace = self.marketplaces[marketplace_name]
            skill = None
            for s in marketplace['skills']:
                if s['name'] == skill_name:
                    skill = s
                    break
            
            if skill is None:
                print(f"✗ Skill '{skill_name}' not found in marketplace '{marketplace_name}'", file=sys.stderr)
                return False
            
            # Install the skill
            install_key = f"{skill_name}@{marketplace_name}"
            self.installed[install_key] = {
                "skill": skill_name,
                "marketplace": marketplace_name,
                "version": skill['version'],
                "description": skill['description'],
                "type": skill['type']
            }
            self._save_installed()
            
            print(f"✓ Successfully installed '{skill_name}' from '{marketplace_name}'")
            print(f"  Version: {skill['version']}")
            print(f"  Type: {skill['type']}")
            return True
            
        except Exception as e:
            print(f"✗ Error installing skill: {e}", file=sys.stderr)
            return False
    
    def list_marketplaces(self) -> bool:
        """List all added marketplaces"""
        if not self.marketplaces:
            print("No marketplaces added yet")
            print("Use '/plugin marketplace add <repo>' to add one")
            return True
        
        print(f"\nConfigured marketplaces ({len(self.marketplaces)}):")
        print("-" * 60)
        for name, data in self.marketplaces.items():
            print(f"  • {name}")
            print(f"    Repository: {data['repository']}")
            print(f"    Skills: {len(data['skills'])}")
            print()
        
        return True
    
    def list_installed(self) -> bool:
        """List all installed plugins"""
        if not self.installed:
            print("No plugins installed yet")
            print("Use '/plugin install <skill>@<marketplace>' to install one")
            return True
        
        print(f"\nInstalled plugins ({len(self.installed)}):")
        print("-" * 60)
        for key, data in self.installed.items():
            print(f"  • {data['skill']} (from {data['marketplace']})")
            print(f"    Version: {data['version']}")
            print(f"    Type: {data['type']}")
            print(f"    Description: {data['description']}")
            print()
        
        return True


def print_usage():
    """Print usage information"""
    print("""
GEO Plugin Marketplace CLI

Usage:
  /plugin marketplace add <repository>        Add a marketplace
  /plugin marketplace list <marketplace>      List skills in a marketplace
  /plugin marketplace                         List all marketplaces
  /plugin install <skill>@<marketplace>       Install a skill
  /plugin list                                List installed plugins
  /plugin help                                Show this help

Examples:
  /plugin marketplace add ReScienceLab/opc-skills
  /plugin marketplace list opc-skills
  /plugin install requesthunt@opc-skills
  /plugin list
""")


def main():
    """Main CLI entry point"""
    args = sys.argv[1:]
    
    if not args or args[0] in ["help", "--help", "-h"]:
        print_usage()
        return 0
    
    pm = PluginMarketplace()
    
    command = args[0]
    
    if command == "marketplace":
        if len(args) < 2:
            # List all marketplaces
            pm.list_marketplaces()
            return 0
        
        subcommand = args[1]
        
        if subcommand == "add":
            if len(args) < 3:
                print("✗ Error: repository required", file=sys.stderr)
                print("Usage: /plugin marketplace add <repository>")
                return 1
            repo = args[2]
            return 0 if pm.marketplace_add(repo) else 1
        
        elif subcommand == "list":
            if len(args) < 3:
                print("✗ Error: marketplace name required", file=sys.stderr)
                print("Usage: /plugin marketplace list <marketplace>")
                return 1
            marketplace_name = args[2]
            return 0 if pm.marketplace_list(marketplace_name) else 1
        
        else:
            print(f"✗ Unknown marketplace subcommand: {subcommand}", file=sys.stderr)
            print_usage()
            return 1
    
    elif command == "install":
        if len(args) < 2:
            print("✗ Error: skill specification required", file=sys.stderr)
            print("Usage: /plugin install <skill>@<marketplace>")
            return 1
        skill_spec = args[1]
        return 0 if pm.install(skill_spec) else 1
    
    elif command == "list":
        return 0 if pm.list_installed() else 1
    
    else:
        print(f"✗ Unknown command: {command}", file=sys.stderr)
        print_usage()
        return 1


if __name__ == "__main__":
    sys.exit(main())
