from pathlib import Path


def load_guide_text() -> str:
    # Resolve repository root as the parent of this tests directory
    test_dir = Path(__file__).resolve().parent
    repo_root = test_dir.parent
    guide_path = repo_root / "COMPLETE-BEGINNERS-GUIDE.md"
    assert guide_path.exists(), f"Guide file not found at: {guide_path}"
    text = guide_path.read_text(encoding="utf-8")
    assert text.strip(), "Guide file is empty"
    return text


def test_contains_main_title_and_sections():
    text = load_guide_text()

    required_headings = [
        "# 🎯 SYNOVA AI - COMPLETE BEGINNER'S GUIDE",
        "## 🚀 STEP-BY-STEP LAUNCH INSTRUCTIONS",
        "## 🎮 HOW TO USE YOUR AI PLATFORM",
        "## 🔧 TROUBLESHOOTING GUIDE",
        "## 🎯 TESTING YOUR PLATFORM",
        "## 💡 CUSTOMIZATION IDEAS",
        "## 🚀 WHAT'S NEXT",
        "## 📞 NEED HELP?",
        "## 🎉 CONGRATULATIONS",
    ]

    for h in required_headings:
        assert h in text, f"Missing heading: {h}"


def test_step_commands_present():
    text = load_guide_text()

    # Commands presented in code blocks
    expected_commands = [
        "python create-synova-project.py",
        "pip install -r requirements.txt",
        "start.bat",
        "chmod +x start.sh",
        "./start.sh",
    ]

    for cmd in expected_commands:
        assert cmd in text, f"Missing command in guide: {cmd}"


def test_backend_url_and_docs_present():
    text = load_guide_text()
    assert "http://localhost:8000" in text, "Backend URL not documented"
    assert "http://localhost:8000/docs" in text, "OpenAPI docs URL not documented"


def test_limits_and_usage_described():
    text = load_guide_text()
    assert "50 messages per day" in text, "Daily message limit not documented"
    assert "200 characters per message" in text, "Character limit not documented"


def test_customization_snippet_present():
    text = load_guide_text()

    expected_snippet_parts = [
        '"terrestrial": {',
        '"greeting": "Hello! I\'m Synova..."',
        '"help": "I can help with..."',
        '"joke": "Why did the AI cross the road? To get to the other site!"',
        'elif "joke" in query_lower:',
        'response = tier_responses["joke"]',
    ]

    for part in expected_snippet_parts:
        assert part in text, f"Expected example snippet content missing: {part}"


def test_troubleshooting_contains_common_items():
    text = load_guide_text()
    expected_items = [
        "Python not found",
        "pip install failed",
        "Backend not connected",
        "Website won't open",
        "AI responses are slow",
    ]
    for item in expected_items:
        assert item in text, f"Troubleshooting item missing: {item}"
