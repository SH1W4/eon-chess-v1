#!/usr/bin/env python3
import argparse
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Paths to artifacts this runner can generate
CI_WORKFLOW = ROOT / ".github/workflows/ci.yml"
AUDIO_MANAGER = ROOT / "src/audio/audio_manager.py"
AUDIO_INIT = ROOT / "src/audio/__init__.py"
QUANTUM_README = ROOT / "src/quantum/optimizations/README.md"
QUANTUM_PROFILE = ROOT / "scripts/quantum_profile.py"
SUPPORT_MD = ROOT / "docs/SUPPORT.md"
ISSUE_TEMPLATE = ROOT / ".github/ISSUE_TEMPLATE/bug_report.yml"


def ensure_dir(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    ensure_dir(path)
    path.write_text(content, encoding="utf-8")
    return True


# ----- Generators -----

def generate_ci() -> list[str]:
    created = []
    ci_content = textwrap.dedent(
        """
        name: CI
        on:
          push:
            branches: [ main ]
          pull_request:
            branches: [ main ]
        jobs:
          build-and-test:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v4
              - name: Set up Python
                uses: actions/setup-python@v5
                with:
                  python-version: '3.11'
              - name: Install dependencies
                run: |
                  python -m pip install --upgrade pip
                  if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
              - name: Run tests
                run: |
                  if [ -d tests ]; then pytest -q; else echo "No tests/ directory"; fi
        """
    ).strip() + "\n"
    if write_if_missing(CI_WORKFLOW, ci_content):
        created.append(str(CI_WORKFLOW.relative_to(ROOT)))
    return created


def generate_audio() -> list[str]:
    created = []
    audio_manager_content = textwrap.dedent(
        '''
        # Audio system for CHESS with cultural integration.
        # Minimal stub to be extended by frontend/backend layers.
        from __future__ import annotations
        from dataclasses import dataclass
        from typing import Optional

        @dataclass
        class TrackSpec:
            culture: str
            phase: str  # opening|midgame|endgame
            path: str

        class AudioManager:
            def __init__(self):
                self.current_culture: Optional[str] = None
                self.current_phase: str = "opening"
                self.muted: bool = False

            def set_culture(self, culture: str) -> None:
                self.current_culture = culture

            def set_phase(self, phase: str) -> None:
                assert phase in {"opening", "midgame", "endgame"}
                self.current_phase = phase

            def mute(self, value: bool = True) -> None:
                self.muted = value

            def next_track(self) -> TrackSpec:
                culture = self.current_culture or "default"
                base = f"assets/audio/{culture}"
                return TrackSpec(culture=culture, phase=self.current_phase, path=f"{base}/{self.current_phase}.mp3")

            def sfx_for_event(self, event: str) -> str:
                culture = self.current_culture or "default"
                return f"assets/audio/{culture}/sfx/{event}.mp3"
        '''
    ).strip() + "\n"
    init_content = "# Audio package\n"
    if write_if_missing(AUDIO_MANAGER, audio_manager_content):
        created.append(str(AUDIO_MANAGER.relative_to(ROOT)))
    if write_if_missing(AUDIO_INIT, init_content):
        created.append(str(AUDIO_INIT.relative_to(ROOT)))
    return created


def generate_quantum() -> list[str]:
    created = []
    readme = textwrap.dedent(
        """
        # Quantum Optimizations

        Targets:
        - Analyze performance hotspots in superposition/entanglement phases
        - Introduce state caching for repeated branches
        - Validate parity with classical engine on gold test sets

        Use `scripts/quantum_profile.py` to sample representative scenarios.
        """
    ).strip() + "\n"
    profiler = textwrap.dedent(
        '''
        #!/usr/bin/env python3
        """Lightweight profiling harness for quantum engine."""
        import time
        from pathlib import Path

        def run_scenarios():
            # Placeholder: integrate with actual quantum engine when available
            scenarios = [
                {"name": "opening_superposition", "depth": 4},
                {"name": "midgame_branches", "depth": 6},
                {"name": "endgame_collapse", "depth": 5},
            ]
            results = []
            for sc in scenarios:
                start = time.time()
                time.sleep(0.05)  # simulate work
                results.append({"scenario": sc["name"], "elapsed_ms": int((time.time() - start)*1000)})
            return results

        if __name__ == "__main__":
            for r in run_scenarios():
                print(f"{r['scenario']}: {r['elapsed_ms']} ms")
        '''
    ).strip() + "\n"
    if write_if_missing(QUANTUM_README, readme):
        created.append(str(QUANTUM_README.relative_to(ROOT)))
    if write_if_missing(QUANTUM_PROFILE, profiler):
        created.append(str(QUANTUM_PROFILE.relative_to(ROOT)))
        QUANTUM_PROFILE.chmod(0o755)
    return created


def generate_support() -> list[str]:
    created = []
    support_md = textwrap.dedent(
        """
        # Support & Tickets

        - Report bugs via GitHub Issues (Bug Report template provided)
        - Read the FAQ in docs/FAQ.md
        - Feature requests are welcome via issues labeled `enhancement`
        """
    ).strip() + "\n"
    issue_template = textwrap.dedent(
        """
        name: Bug report
        description: File a bug report
        title: "[Bug]: "
        labels: [bug]
        body:
          - type: textarea
            id: what-happened
            attributes:
              label: What happened?
              description: Also tell us what you expected to happen
              placeholder: Tell us what you see!
              value: |
                A bug happened!
            validations:
              required: true
          - type: input
            id: version
            attributes:
              label: Version
              description: CHESS version or commit hash
              placeholder: v0.2.0
          - type: textarea
            id: logs
            attributes:
              label: Relevant log output
              render: shell
        """
    ).strip() + "\n"
    if write_if_missing(SUPPORT_MD, support_md):
        created.append(str(SUPPORT_MD.relative_to(ROOT)))
    if write_if_missing(ISSUE_TEMPLATE, issue_template):
        created.append(str(ISSUE_TEMPLATE.relative_to(ROOT)))
    return created


def plan(target: str) -> list[str]:
    mapping = {
        "ci": [CI_WORKFLOW],
        "audio": [AUDIO_MANAGER, AUDIO_INIT],
        "quantum": [QUANTUM_README, QUANTUM_PROFILE],
        "support": [SUPPORT_MD, ISSUE_TEMPLATE],
    }
    if target == "all":
        targets = sum(mapping.values(), [])
    else:
        targets = mapping.get(target, [])
    return [str(p.relative_to(ROOT)) for p in targets]


def apply(target: str) -> list[str]:
    if target in ("ci", "all"):
        created_ci = generate_ci()
    else:
        created_ci = []
    if target in ("audio", "all"):
        created_audio = generate_audio()
    else:
        created_audio = []
    if target in ("quantum", "all"):
        created_quantum = generate_quantum()
    else:
        created_quantum = []
    if target in ("support", "all"):
        created_support = generate_support()
    else:
        created_support = []
    return created_ci + created_audio + created_quantum + created_support


def main():
    parser = argparse.ArgumentParser(description="ARKITECT Task Runner")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_plan = sub.add_parser("plan", help="Show what would be generated")
    p_plan.add_argument("target", choices=["ci", "audio", "quantum", "support", "all"], help="Target area")

    p_apply = sub.add_parser("apply", help="Generate missing artifacts for a target")
    p_apply.add_argument("target", choices=["ci", "audio", "quantum", "support", "all"], help="Target area")

    args = parser.parse_args()

    if args.cmd == "plan":
        for p in plan(args.target):
            print(p)
        return 0
    if args.cmd == "apply":
        created = apply(args.target)
        if created:
            print("Created:")
            for p in created:
                print(f" - {p}")
        else:
            print("Nothing to create. All artifacts already exist.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())

