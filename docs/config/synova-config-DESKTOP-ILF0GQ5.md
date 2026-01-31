# Synova Backend Config Reference

Location: `config/synova-config.json` (copy from `config/synova-config.example.json`).

## Sections

- `synova`
  - `mode`: `terrestrial` | `aerial` | `celestial`
  - `quantum_enabled`: boolean
  - `bci_enabled`: boolean
  - `evolution_enabled`: boolean
  - `max_context_hours`: integer hours
  - `max_daily_queries`: integer (-1 for unlimited)
  - `ethics_level`: `basic` | `standard` | `advanced`

- `hardware`
  - `gpu_enabled`: boolean
  - `quantum_simulator`: e.g. `qiskit`
  - `neural_interface`: `none` | device name
  - `cpu_cores`: integer
  - `memory_limit_gb`: integer

- `cloud`
  - `provider`: e.g. `aws`
  - `region`: e.g. `us-east-1`
  - `quantum_access`: boolean

## Example

```json
{
  "synova": {
    "mode": "celestial",
    "quantum_enabled": true,
    "bci_enabled": false,
    "evolution_enabled": true,
    "max_context_hours": 168,
    "max_daily_queries": -1,
    "ethics_level": "advanced"
  },
  "hardware": {
    "gpu_enabled": true,
    "quantum_simulator": "qiskit",
    "neural_interface": "none",
    "cpu_cores": 8,
    "memory_limit_gb": 16
  },
  "cloud": {
    "provider": "aws",
    "region": "us-east-1",
    "quantum_access": true
  }
}
```

## Notes

- For Android emulator local dev, point mobile app to `http://10.0.2.2:8000`.

- Keep secrets (keys, API tokens) outside the repo; load via env vars.
