import importlib
import asyncio


def _reload_module():
    mod = importlib.import_module("self_evolution_core")
    importlib.reload(mod)
    return mod


def test_evolution_engine_basic_status_and_flow():
    mod = _reload_module()
    engine = mod.EvolutionEngine(safety_threshold=0.0)  # allow all for basic path

    # Initial status
    status = engine.get_evolution_status()
    assert status["current_generation"] == 0
    assert status["safety_threshold"] == 0.0

    # Minimal evolve cycle with empty metrics
    perf_metrics = {"accuracy": 0.5}
    user_profiles = {}
    result = asyncio.run(engine.evolve_system(perf_metrics, user_profiles))
    assert isinstance(result, dict)
    assert "generation" in result


def test_evolution_utils_helpers():
    mod = _reload_module()

    # Mutation impact
    impact = mod.EvolutionUtils.calculate_mutation_impact(
        {"type": "parameter_adjustment", "delta": 3.0}, {},
    )
    assert 0.0 <= impact <= 1.0

    # Safety validation passes when constraints satisfied
    proposed = {"lr": 0.05}
    constraints = {"lr": {"max": 0.1}}
    assert mod.EvolutionUtils.validate_evolution_safety(proposed, constraints) is True

    # Safety validation fails when constraint violated
    proposed2 = {"lr": 0.2}
    assert mod.EvolutionUtils.validate_evolution_safety(proposed2, constraints) is False
