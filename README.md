# geo

GEO Plugin Marketplace - A command-line tool for managing plugins and skill marketplaces.

## Installation

Clone the repository and add the plugin script to your PATH:

```bash
git clone https://github.com/fr1zxx/geo.git
cd geo
chmod +x plugin
export PATH="$PATH:$(pwd)"
```

Alternatively, you can run the plugin script directly:

```bash
./plugin <command>
```

## Usage

### Add a Marketplace

Add a marketplace to discover and install skills:

```bash
./plugin marketplace add ReScienceLab/opc-skills
```

### List Available Skills

List all available skills in a marketplace:

```bash
./plugin marketplace list opc-skills
```

### Install Skills

Install specific skills from a marketplace:

```bash
./plugin install requesthunt@opc-skills
./plugin install domain-hunter@opc-skills
./plugin install seo-geo@opc-skills
```

### List Installed Plugins

View all installed plugins:

```bash
./plugin list
```

### List Marketplaces

View all configured marketplaces:

```bash
./plugin marketplace
```

## Commands

| Command | Description |
|---------|-------------|
| `./plugin marketplace add <repository>` | Add a marketplace |
| `./plugin marketplace list <marketplace>` | List skills in a marketplace |
| `./plugin marketplace` | List all marketplaces |
| `./plugin install <skill>@<marketplace>` | Install a skill |
| `./plugin list` | List installed plugins |
| `./plugin help` | Show help |

## Example Workflow

```bash
# Add the OPC Skills marketplace
./plugin marketplace add ReScienceLab/opc-skills

# Install specific skills
./plugin install requesthunt@opc-skills
./plugin install domain-hunter@opc-skills
./plugin install seo-geo@opc-skills

# List all available skills
./plugin marketplace list opc-skills

# View installed plugins
./plugin list
```

## Configuration

Plugin marketplace data is stored in `~/.geo/`:
- `marketplaces.json` - Configured marketplaces
- `installed.json` - Installed plugins

## Requirements

- Python 3.6+
- No external dependencies required