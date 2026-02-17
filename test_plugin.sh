#!/bin/bash
# Integration test for the plugin marketplace system

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_CMD="$SCRIPT_DIR/plugin"

# Use a temporary config directory for testing
TEST_HOME="/tmp/plugin-test-$$"
export HOME="$TEST_HOME"
mkdir -p "$HOME"

echo "=== Testing Plugin Marketplace System ==="
echo

# Test 1: Add marketplace
echo "Test 1: Adding marketplace..."
$PLUGIN_CMD marketplace add ReScienceLab/opc-skills
echo "✓ Test 1 passed"
echo

# Test 2: List marketplace
echo "Test 2: Listing marketplace..."
$PLUGIN_CMD marketplace
echo "✓ Test 2 passed"
echo

# Test 3: Install first skill
echo "Test 3: Installing requesthunt..."
$PLUGIN_CMD install requesthunt@opc-skills
echo "✓ Test 3 passed"
echo

# Test 4: Install second skill
echo "Test 4: Installing domain-hunter..."
$PLUGIN_CMD install domain-hunter@opc-skills
echo "✓ Test 4 passed"
echo

# Test 5: Install third skill
echo "Test 5: Installing seo-geo..."
$PLUGIN_CMD install seo-geo@opc-skills
echo "✓ Test 5 passed"
echo

# Test 6: List all available skills in marketplace
echo "Test 6: Listing all skills in marketplace..."
$PLUGIN_CMD marketplace list opc-skills
echo "✓ Test 6 passed"
echo

# Test 7: List installed plugins
echo "Test 7: Listing installed plugins..."
$PLUGIN_CMD list
echo "✓ Test 7 passed"
echo

# Test 8: Show help
echo "Test 8: Showing help..."
$PLUGIN_CMD help
echo "✓ Test 8 passed"
echo

# Clean up - safety check to ensure we only delete the test directory
if [[ "$HOME" == "$TEST_HOME" ]] && [[ "$TEST_HOME" == /tmp/plugin-test-* ]]; then
    rm -rf "$HOME"
else
    echo "Warning: Skipping cleanup due to unexpected HOME value: $HOME"
fi

echo "=== All tests passed! ==="
