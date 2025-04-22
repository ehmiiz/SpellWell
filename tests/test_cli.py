"""Test module for CLI functionality."""
import os
import tempfile
from click.testing import CliRunner
from spellwell.cli import main


def test_version():
    """Test that the --version flag works."""
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output.lower()


def test_help():
    """Test that the --help flag works."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    
    # Test help for subcommands
    for cmd in ["add", "list", "practice", "stats", "clear"]:
        result = runner.invoke(main, [cmd, "--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output


def test_add_word():
    """Test adding a word to the wordlist."""
    runner = CliRunner()
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        try:
            result = runner.invoke(main, ["add", "hello", "-f", tmp.name])
            assert result.exit_code == 0
            assert "Added" in result.output
            
            # Check the file contents
            with open(tmp.name, 'r') as f:
                content = f.read()
                assert "hello" in content
        finally:
            os.unlink(tmp.name)


def test_list_words():
    """Test listing words from the wordlist."""
    runner = CliRunner()
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        try:
            # Add some words
            with open(tmp.name, 'w') as f:
                f.write("hello\nworld\n")
            
            result = runner.invoke(main, ["list", "-f", tmp.name])
            assert result.exit_code == 0
            assert "hello" in result.output
            assert "world" in result.output
        finally:
            os.unlink(tmp.name)


def test_clear_wordlist():
    """Test clearing the wordlist."""
    runner = CliRunner()
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        try:
            # Add some words
            with open(tmp.name, 'w') as f:
                f.write("hello\nworld\n")
            
            # Simulate user confirmation
            result = runner.invoke(main, ["clear", "-f", tmp.name], input="y\n")
            assert result.exit_code == 0
            
            # Check file is empty
            with open(tmp.name, 'r') as f:
                content = f.read()
                assert content == ""
        finally:
            os.unlink(tmp.name)