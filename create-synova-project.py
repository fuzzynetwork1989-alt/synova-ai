#!/usr/bin/env python3
"""Creates the Synova AI starter project folders (one-time helper).
Run: python create-synova-project.py
"""
import os
from pathlib import Path

root = Path(__file__).resolve().parent / "synova-ai-platform"
folders = [
    "backend/api",
    "backend/ai_core",
    "frontend/terrestrial",
    "frontend/aerial",
    "frontend/celestial",
    "mobile",
    "docs",
    "config",
    "tests",
]

print("🚀 Creating Synova AI Project...")
print("==================================================")
for f in folders:
    p = root / f
    p.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created folder: {p.relative_to(root)}")

# create a placeholder README in the root
(root / "README.md").write_text("# Synova AI Platform\n\nProject created by create-synova-project.py\n")
print("\n🎉 Project structure created successfully!")
print(f"📁 Your project is in the '{root}' folder")
print("Next: Run the main setup to install everything!")
