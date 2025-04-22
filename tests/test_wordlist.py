"""Test module for wordlist functionality."""
import os
import tempfile
import json
from spellwell.wordlist import (
    ensure_wordlist_exists, 
    add_word, 
    get_words, 
    store_results, 
    get_results
)


def test_ensure_wordlist_exists():
    """Test creating the wordlist file if it doesn't exist."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        os.unlink(tmp.name)  # Delete the file so we can test creation
        try:
            ensure_wordlist_exists(tmp.name)
            assert os.path.exists(tmp.name)
        finally:
            if os.path.exists(tmp.name):
                os.unlink(tmp.name)


def test_add_word():
    """Test adding a word to the wordlist."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        try:
            add_word("hello", tmp.name)
            add_word("world", tmp.name)
            
            # Check the words were added
            with open(tmp.name, 'r') as f:
                content = f.read()
                assert "hello" in content
                assert "world" in content
            
            # Test adding a duplicate (shouldn't add)
            add_word("hello", tmp.name)
            words = get_words(tmp.name)
            assert len(words) == 2
            assert "hello" in words
            assert "world" in words
        finally:
            os.unlink(tmp.name)


def test_get_words():
    """Test retrieving words from the wordlist."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        try:
            # Add some words directly to the file
            with open(tmp.name, 'w') as f:
                f.write("apple\nbanana\ncherry\n")
            
            words = get_words(tmp.name)
            assert len(words) == 3
            assert "apple" in words
            assert "banana" in words
            assert "cherry" in words
        finally:
            os.unlink(tmp.name)


def test_store_and_get_results():
    """Test storing and retrieving practice results."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        try:
            # Store some results
            results = [
                ("apple", "apple", True),
                ("banana", "banana", True),
                ("cherry", "chery", False)
            ]
            store_results(results, tmp.name)
            
            # Check the results file was created with the right format
            with open(tmp.name, 'r') as f:
                data = json.load(f)
                assert len(data) == 1  # One session
                assert "timestamp" in data[0]
                assert len(data[0]["results"]) == 3  # Three results
            
            # Test retrieving results
            retrieved = get_results(tmp.name)
            assert len(retrieved) == 3
            
            # Check the values
            words = [word for word, _, _ in retrieved]
            assert "apple" in words
            assert "banana" in words
            assert "cherry" in words
            
            # Check correctness
            correct_count = sum(1 for _, _, correct in retrieved if correct)
            assert correct_count == 2
        finally:
            os.unlink(tmp.name)