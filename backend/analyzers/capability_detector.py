"""
Capability Detector — multi-layer evidence collection.

Detection priority:
  1. Dependency files (package.json, requirements.txt)
  2. Import statements
  3. File names
  4. Folder names
  5. Code patterns

A capability is PRESENT when ANY indicator matches.
"""

import json
import re
from collections.abc import Callable
from dataclasses import dataclass, field

from analyzers.capabilities import CapabilitySpec, get_capabilities, normalize_project_type
from services.github_service import fetch_file_content

_CONTENT_SCAN_LIMIT = 80
_CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".ipynb", ".java", ".kt",
    ".dart", ".swift", ".go", ".rb", ".rs", ".cs", ".m", ".h",
}


@dataclass
class RepoContext:
    file_paths: list[str]
    js_deps: set[str]
    py_deps_text: str
    technologies: set[str]
    normalized_paths: list[str]
    get_content: Callable[[str], str | None]
    _scanned_content: dict[str, str] = field(default_factory=dict)


def _build_context(
    file_paths: list[str],
    owner: str,
    repo: str,
    technologies: list[str] | None = None,
) -> RepoContext:
    cache: dict[str, str | None] = {}

    def get_content(path: str) -> str | None:
        if path not in cache:
            cache[path] = fetch_file_content(owner, repo, path)
        return cache[path]

    js_deps: set[str] = set()
    if "package.json" in file_paths:
        raw = get_content("package.json")
        if raw:
            try:
                pkg = json.loads(raw)
                js_deps.update(pkg.get("dependencies", {}).keys())
                js_deps.update(pkg.get("devDependencies", {}).keys())
            except (json.JSONDecodeError, Exception):
                pass

    py_fragments = []
    for path in file_paths:
        lower = path.lower()
        if lower.endswith("requirements.txt") or lower.endswith("requirements-dev.txt"):
            content = get_content(path)
            if content:
                py_fragments.append(content.lower())
        elif lower in ("pyproject.toml", "pipfile", "setup.py", "environment.yml"):
            content = get_content(path)
            if content:
                py_fragments.append(content.lower())

    normalized_paths = [p.lower().replace("\\", "/") for p in file_paths]

    return RepoContext(
        file_paths=file_paths,
        js_deps=js_deps,
        py_deps_text="\n".join(py_fragments),
        technologies=set(technologies or []),
        normalized_paths=normalized_paths,
        get_content=get_content,
    )


def _add_evidence(evidence: list[dict], seen: set, etype: str, value: str) -> None:
    key = (etype, value)
    if key not in seen:
        seen.add(key)
        evidence.append({"type": etype, "value": value})


def _path_segments(path: str) -> list[str]:
    return [seg for seg in path.split("/") if seg]


def _scan_code_files(ctx: RepoContext, spec: CapabilitySpec) -> dict[str, str]:
    """Cache file contents for import/pattern scanning (priority: src, app, notebooks)."""
    if ctx._scanned_content:
        return ctx._scanned_content

    priority_prefixes = ("src/", "app/", "backend/", "frontend/", "notebooks/", "tests/", "test/", "api/")
    candidates = []

    for path in ctx.normalized_paths:
        if not any(path.endswith(ext) for ext in spec.scan_extensions):
            continue
        if not any(path.endswith(ext) for ext in _CODE_EXTENSIONS):
            continue
        priority = 0
        for i, prefix in enumerate(priority_prefixes):
            if path.startswith(prefix) or f"/{prefix}" in path:
                priority = len(priority_prefixes) - i
                break
        candidates.append((priority, path))

    candidates.sort(key=lambda x: (-x[0], x[1]))
    scanned = 0
    for _, path in candidates:
        if scanned >= _CONTENT_SCAN_LIMIT:
            break
        content = ctx.get_content(path)
        if content:
            ctx._scanned_content[path] = content
            scanned += 1

    return ctx._scanned_content


def _match_dependencies(spec: CapabilitySpec, ctx: RepoContext, evidence: list, seen: set) -> None:
    for pkg in spec.js_packages:
        if pkg in ctx.js_deps:
            _add_evidence(evidence, seen, "dependency", pkg)
    for pkg in spec.py_packages:
        if pkg in ctx.py_deps_text:
            _add_evidence(evidence, seen, "dependency", pkg)
    for name in spec.tech_names:
        if name in ctx.technologies:
            _add_evidence(evidence, seen, "dependency", name)


def _match_imports(spec: CapabilitySpec, ctx: RepoContext, evidence: list, seen: set) -> None:
    if not spec.import_patterns:
        return
    contents = _scan_code_files(ctx, spec)
    for path, content in contents.items():
        content_lower = content.lower()
        for pattern in spec.import_patterns:
            if pattern.lower() in content_lower:
                _add_evidence(evidence, seen, "import", pattern)
                _add_evidence(evidence, seen, "filename", path.split("/")[-1])


def _match_filenames(spec: CapabilitySpec, ctx: RepoContext, evidence: list, seen: set) -> None:
    for path in ctx.normalized_paths:
        basename = path.split("/")[-1]

        for ext in spec.file_extensions:
            if path.endswith(ext):
                _add_evidence(evidence, seen, "filename", basename if basename else path)
                break

        for keyword in spec.filename_keywords:
            if keyword in basename:
                _add_evidence(evidence, seen, "filename", basename)
                break

        for marker in spec.path_markers:
            if marker in path and marker not in (".csv", ".json"):
                if "/" in marker or marker.endswith((".json", ".yaml", ".yml")):
                    _add_evidence(evidence, seen, "filename", path)
                break


def _match_folders(spec: CapabilitySpec, ctx: RepoContext, evidence: list, seen: set) -> None:
    for path in ctx.normalized_paths:
        segments = _path_segments(path)
        for folder in spec.folder_segments:
            if folder in segments:
                _add_evidence(evidence, seen, "folder", f"{folder}/")
        for marker in spec.path_markers:
            if marker.endswith("/") and marker in path:
                _add_evidence(evidence, seen, "folder", marker)


def _match_code_patterns(spec: CapabilitySpec, ctx: RepoContext, evidence: list, seen: set) -> None:
    if not spec.content_keywords:
        return
    contents = _scan_code_files(ctx, spec)
    for path, content in contents.items():
        content_lower = content.lower()
        for pattern in spec.content_keywords:
            if pattern.lower() in content_lower:
                _add_evidence(evidence, seen, "code_pattern", pattern)


def _match_auth_paths(spec: CapabilitySpec, ctx: RepoContext, evidence: list, seen: set) -> None:
    """Extra auth detection: auth-related paths and route files."""
    if spec.key != "authentication":
        return
    auth_route_pattern = re.compile(r"(login|signup|signin|register|authenticate|auth)", re.I)
    for path in ctx.normalized_paths:
        if auth_route_pattern.search(path):
            if path.endswith((".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".java")):
                _add_evidence(evidence, seen, "filename", path.split("/")[-1])


def _evaluate_capability(spec: CapabilitySpec, ctx: RepoContext) -> dict:
    """
    Collect evidence in priority order. Capability present if any evidence found.
    """
    evidence: list[dict] = []
    seen: set = set()

    # Priority 1: Dependencies
    _match_dependencies(spec, ctx, evidence, seen)
    # Priority 2: Imports
    _match_imports(spec, ctx, evidence, seen)
    # Priority 3: File names
    _match_filenames(spec, ctx, evidence, seen)
    # Priority 4: Folder names
    _match_folders(spec, ctx, evidence, seen)
    # Priority 5: Code patterns
    _match_code_patterns(spec, ctx, evidence, seen)
    # Extra heuristics
    _match_auth_paths(spec, ctx, evidence, seen)

    matched = [e["value"] for e in evidence[:8]]

    return {
        "detected": len(evidence) > 0,
        "label": spec.label,
        "weight": spec.weight,
        "matched": matched,
        "evidence": evidence[:10],
    }


def detect_capabilities(
    file_paths: list[str],
    owner: str,
    repo: str,
    project_type: str | None = None,
    technologies: list[str] | None = None,
) -> dict[str, dict]:
    normalized = normalize_project_type(project_type)
    specs = get_capabilities(normalized)
    ctx = _build_context(file_paths, owner, repo, technologies)

    return {spec.key: _evaluate_capability(spec, ctx) for spec in specs}


def capabilities_to_bool_map(capabilities: dict[str, dict]) -> dict[str, bool]:
    return {key: bool(data.get("detected")) for key, data in capabilities.items()}
