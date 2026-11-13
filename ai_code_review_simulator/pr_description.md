Pull Request: Add Static Diff Rule Scanner & Review Scoring

Summary

Implements automated static rule checks and a weighted review score calculator (analyze_diff_lines) for unified pull request diffs in ai_code_review_simulator. Flags common security and maintainability issues (eval/exec, hardcoded credentials, bare except:, and leftover TODO/FIXME comments) on newly added lines before human review.

Changes

Added analyze_diff_lines() and SEVERITY_WEIGHTS in review_rules.py to inspect added diff lines (+), compute a 0–100 review score, and determine auto-approval eligibility.

Added rule definitions for SEC001 (dynamic execution), SEC002 (hardcoded secrets), QUAL001 (bare except:), and MAINT001 (TODO/FIXME markers).

Added 4 unit tests in TestAnalyzeDiffLines verifying clean diff scoring, high-severity approval blocking, medium/low penalty calculation, and ignoring removed/context lines.

Context

Scope: ~125 LOC (feature implementation + unit tests) for holbertonschool-ai4devs/ai_code_review_simulator.

Related Issue: #14 — Automate baseline static checks prior to AI/peer code review.

Motivation: Catching high-severity security anti-patterns and bare exception handlers immediately on diff ingestion reduces reviewer noise and enforces consistent quality gates.

Verification: Executed python3 -m unittest review_rules.py — all 4 unit tests pass.
