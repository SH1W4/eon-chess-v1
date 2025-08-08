# FAQ - CHESS Project

Welcome to the Frequently Asked Questions. This document complements SUPPORT.md.

- What is CHESS?
  CHESS is a culturally-augmented chess system with adaptive AI (ARKITECT) and rich narratives.

- How do I report a bug?
  Use GitHub Issues with the Bug report template, or from inside the app via the Report Bug option.

- How do I request a new culture/theme?
  Open a Feature request issue and reference HOW_TO_ADD_CULTURES.md. Provide brief narrative, values, and piece metaphors.

- Where can I see all implemented cultures?
  See CULTURAL_REGISTRY.md and src/cultural/cultural_registry.py.

- How do I contribute code?
  Fork, create a feature branch, commit with conventional commits, open a PR.

- How is code quality enforced?
  CI checks run ruff (lint), black (format check), and pytest with coverage.

- Where are audio assets located?
  Under assets/audio/<culture>/{opening,midgame,endgame}.mp3 and assets/audio/<culture>/sfx/.

- Who maintains ARKITECT?
  ARKITECT is part of CHESS core; see docs/ARKITECT_AI_FINALIZATION.md and scripts/arkitect_task_runner.py.

