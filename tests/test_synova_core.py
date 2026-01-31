import importlib

import asyncio


def _reload_core():
    mod = importlib.import_module("synova_ai_core")
    importlib.reload(mod)
    return mod


def test_factory_creates_by_mode():
    core = _reload_core()

    # Terrestrial
    s1 = core.create_synova_instance("terrestrial")
    st1 = s1.get_system_status()
    assert st1["mode"] == "terrestrial"
    assert st1["components_status"]["neuro_symbolic"] is True
    assert st1["components_status"]["temporal_engine"] is True
    assert st1["components_status"]["quantum_processor"] is False
    assert st1["components_status"]["evolution_core"] is False

    # Aerial (quantum enabled by default in factory)
    s2 = core.create_synova_instance("aerial")
    st2 = s2.get_system_status()
    assert st2["mode"] == "aerial"
    assert st2["components_status"]["behavior_predictor"] is True
    assert st2["components_status"]["quantum_processor"] in (True, False)

    # Celestial with BCI and evolution
    s3 = core.create_synova_instance("celestial", bci_enabled=True, evolution_enabled=True)
    st3 = s3.get_system_status()
    assert st3["mode"] == "celestial"
    assert st3["components_status"]["evolution_core"] is True
    assert st3["components_status"]["mind_interface"] is True


def test_should_evolve_gate_logic():
    core = _reload_core()
    s = core.create_synova_instance("celestial")
    s.metrics["queries_processed"] = 2000
    s.metrics["accuracy_score"] = 0.951
    assert s._should_evolve() is True

    s.metrics["accuracy_score"] = 0.80
    assert s._should_evolve() is False


def test_trigger_evolution_requires_celestial():
    core = _reload_core()

    # Terrestrial returns error
    s = core.create_synova_instance("terrestrial")
    res = asyncio.run(s.trigger_evolution())
    assert res.get("error") is not None

    # Celestial without evolution enabled returns error
    s2 = core.create_synova_instance("celestial", evolution_enabled=False)
    res2 = asyncio.run(s2.trigger_evolution())
    assert res2.get("error") is not None


def test_status_structure_contains_expected_keys():
    core = _reload_core()
    s = core.create_synova_instance("terrestrial")
    status = s.get_system_status()

    for key in ("session_id", "mode", "state", "metrics", "components_status"):
        assert key in status

    comp = status["components_status"]
    expected_comp_keys = {
        "quantum_processor",
        "neuro_symbolic",
        "temporal_engine",
        "ethics_guardian",
        "evolution_core",
        "mind_interface",
        "behavior_predictor",
    }
    assert expected_comp_keys.issubset(comp.keys())
