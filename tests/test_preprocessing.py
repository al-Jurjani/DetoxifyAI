import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import preprocess_aggressive


def test_preprocess_aggressive_lowercase():
    """Test that preprocessing converts to lowercase."""
    result = preprocess_aggressive("HELLO WORLD")
    assert result == "hello world"


def test_preprocess_aggressive_urls():
    """Test that preprocessing removes URLs."""
    result = preprocess_aggressive("Check this https://example.com and www.test.com")
    assert "https" not in result
    assert "www" not in result
    assert "example.com" not in result


def test_preprocess_aggressive_mentions_hashtags():
    """Test that preprocessing removes @ mentions and # hashtags."""
    result = preprocess_aggressive("Hey @user check #trending")
    assert "@user" not in result
    assert "#trending" not in result


def test_preprocess_aggressive_numbers():
    """Test that preprocessing removes numbers."""
    result = preprocess_aggressive("I have 123 apples and 456 oranges")
    assert "123" not in result
    assert "456" not in result
    assert "apples" in result
    assert "oranges" in result


def test_preprocess_aggressive_punctuation():
    """Test that preprocessing removes punctuation."""
    result = preprocess_aggressive("Hello! How are you? I'm fine.")
    assert "!" not in result
    assert "?" not in result
    assert "." not in result
    # Should keep the words
    assert "hello" in result
    assert "fine" in result


def test_preprocess_aggressive_whitespace():
    """Test that preprocessing normalizes whitespace."""
    result = preprocess_aggressive("Hello    world   test")
    assert "  " not in result  # No double spaces
    assert result.count(" ") == 2  # Only single spaces between words


def test_preprocess_aggressive_complex():
    """Test preprocessing with complex input."""
    text = "Hey @john123! Check out https://example.com #cool 999 times!!!"
    result = preprocess_aggressive(text)
    # Should be cleaned: lowercase, no URLs, no @, no #, no numbers, no punctuation
    # @john123 becomes empty (@ removed, then 123 removed, then john removed because it's part of @john123)
    # #cool becomes empty (# removed, then cool removed because it's part of #cool)
    assert result == "hey check out times"
