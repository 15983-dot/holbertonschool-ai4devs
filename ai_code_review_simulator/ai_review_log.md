AI Review Log

Target PR: Add Static Diff Rule Scanner & Review Scoring (review_rules.py)

Review Personas: Security Auditor, Performance Engineer, Maintainability Architect

Inline Comments

(line 22) [Security] The regex r"\beval\s*\(" and r"\bexec\s*\(" can be bypassed via indirect attribute access (e.g., getattr(builtins, "eval")) or whitespace/newline formatting. Note this limitation in the rule docstring or broaden detection to compile( and __import__(.

(line 30) [Security] Secret detection only matches password, secret, and api_key with single/double quotes. Expand the pattern to cover token, auth_token, private_key, and AWS_SECRET_ACCESS_KEY to reduce false negatives.

(line 30) [Security] Test fixtures or mock values (e.g., password = "example" or api_key = "test_placeholder") will trigger false-positive SEC002 blocks. Consider adding an allowlist for obvious placeholder/dummy strings.

(line 38) [Maintainability] re.search(r"except\s*:\s*$", code.strip()) will miss inline bare except statements such as except: pass. Anchor the check without $ or parse via Python's ast module for exact syntax accuracy.

(line 46) [Maintainability] Checking "TODO" in code triggers on variable names or strings like TODO_ITEMS = []. Use word-boundary matching (r"#\s*(TODO|FIXME)\b") so only actual comments are flagged.

(line 54) [Maintainability] SEVERITY_WEIGHTS[item["severity"]] performs an unchecked dictionary lookup. Use .get(item["severity"], 0) so introducing a new severity tier (e.g., "CRITICAL") cannot raise a KeyError.

(line 61) [Performance] any(f["severity"] == "HIGH" for f in findings) iterates over findings a second time after computing penalty. Track a boolean has_high_severity flag inside the main loop to avoid redundant passes.

Global Feedback

[Performance] All four regular expressions inside analyze_diff_lines() are recompiled on every single added line in the diff. Pre-compile the regex patterns at module level (re.compile(...)) to eliminate repeated compilation overhead on large pull requests.

[Maintainability] analyze_diff_lines() currently mixes diff parsing, rule matching, and score calculation in a single function. Refactor individual checks into a declarative RULES registry (List[Rule]) so new rules can be added without modifying the core loop.

[Security] Add ReDoS (Regular Expression Denial of Service) protection by enforcing a maximum line length check (e.g., skipping or truncating lines longer than 1,000 characters such as minified JS bundles) before running regex matching.

[Maintainability] Add type annotations (TypedDict or @dataclass) for the finding objects and the return dictionary of analyze_diff_lines() so downstream consumers get static type checking and IDE autocomplete.
