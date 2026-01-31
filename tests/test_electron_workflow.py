from pathlib import Path


def test_electron_workflow_name():
    repo_root = Path(__file__).resolve().parents[1]
    workflow_path = repo_root / ".github" / "workflows" / "electron-build.yml"

    assert workflow_path.exists(), f"Missing workflow file: {workflow_path}"

    content = workflow_path.read_text(encoding="utf-8")
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("name:"):
            name_val = stripped.split(":", 1)[1].strip()
            if (
                len(name_val) >= 2
                and name_val[0] in {'"', "'"}
                and name_val[-1] == name_val[0]
            ):
                name_val = name_val[1:-1]
            assert name_val == "Electron Build (Template)"
            break
    else:
        raise AssertionError("name field not found in workflow file")
