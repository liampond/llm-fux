"""Filesystem and path discovery helpers.

Design goals:
    * Keep IO minimal (avoid repeated directory scans where possible).
    * Provide clear errors for missing required artifacts while allowing
        optional lookups (required=False) to return None gracefully.
    * Support legacy naming conventions while nudging toward the new layout.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Set, Iterable, Dict

__all__ = [
        "find_project_root",
        "load_text_file",
        "find_encoded_file",
        "find_question_file",
        "list_questions",
        "list_file_ids",
        "list_datatypes",
        "list_guides",
        "ensure_dir",
        "get_output_path",
]

_ROOT_CACHE: Optional[Path] = None
_DATATYPE_EXT: Dict[str, str] = {"mei": ".mei", "musicxml": ".musicxml", "abc": ".abc", "humdrum": ".krn"}


def _normalize_datatype(datatype: str) -> str:
        key = datatype.lower().strip()
        if key not in _DATATYPE_EXT:
                raise ValueError(f"Unknown datatype '{datatype}'. Valid: {sorted(_DATATYPE_EXT)}")
        return key


def find_project_root(start_path: Optional[Path] = None) -> Path:
    """Locate and cache the project root containing ``pyproject.toml``.

    Parameters
    ----------
    start_path: Path | None
        Starting directory (defaults to this file's parent). Accepts a file path.
    """
    global _ROOT_CACHE
    if _ROOT_CACHE and _ROOT_CACHE.exists():  # pragma: no cover (cache branch)
        return _ROOT_CACHE
    if start_path is None:
        start_path = Path(__file__).parent
    start_path = start_path if start_path.is_dir() else start_path.parent
    current = start_path.resolve()
    while True:
        if (current / "pyproject.toml").exists():
            _ROOT_CACHE = current
            return current
        if current.parent == current:
            break
        current = current.parent
    raise FileNotFoundError("Could not locate project root containing pyproject.toml")


def load_text_file(path: Path) -> str:
    """Read UTF‑8 text file returning stripped contents.

    Raises
    ------
    FileNotFoundError
        If the path is not an existing file.
    """
    if not path.is_file():
        raise FileNotFoundError(f"Expected file at {path} but none was found")
    return path.read_text(encoding="utf-8").strip()


def find_encoded_file(
    file_id: str,
    datatype: str,
    encoded_dir: Path,
    required: bool = True,
) -> Optional[Path]:
    """Locate encoded music file for ``file_id`` with given ``datatype``.

    Returns the first match (exact first, fallback glob) or None if ``required`` is False.
    Raises ValueError for unsupported datatypes & FileNotFoundError when required and missing.
    """
    key = _normalize_datatype(datatype)
    ext = _DATATYPE_EXT[key]
    candidate = encoded_dir / f"{file_id}{ext}"
    if candidate.exists():
        return candidate
    if encoded_dir.exists():
        matches = list(encoded_dir.rglob(f"*{file_id}{ext}"))
        if matches:
            return matches[0]
    if required:
        raise FileNotFoundError(f"No encoded file found for {file_id} in {encoded_dir}")
    return None


def find_question_file(
    file_id: str,
    context: bool,
    questions_dir: Path,
    required: bool = True,
) -> Optional[Path]:
    """Locate contextual / non‑contextual question prompt file (legacy datasets).

    Note: This is for legacy datasets that don't have a single prompt.md file.
    Modern datasets should use a single prompt.md file instead.
    """
    suffix = "context" if context else "nocontext"
    candidate = questions_dir / f"{file_id}.{suffix}.txt"
    if candidate.exists():
        return candidate
    if questions_dir.exists():
        pattern = f"*{file_id}*{'Context' if context else 'NoContext'}Prompt.txt"
        matches = list(questions_dir.glob(pattern))
        if matches:
            return matches[0]
    if required:
        raise FileNotFoundError(f"Question file not found for {file_id} in {questions_dir}")
    return None


def list_questions(questions_dir: Path) -> List[str]:
    """Return sorted stems of all ``.txt`` question prompt files (legacy datasets)."""
    if not questions_dir.exists():
        return []
    return sorted({f.stem for f in questions_dir.rglob("*.txt")})


def list_file_ids(encoded_dir: Path) -> List[str]:
    """Return unique filename stems under each datatype subdirectory."""
    if not encoded_dir.exists():
        return []
    ids: Set[str] = set()
    for sub in encoded_dir.iterdir():
        if not sub.is_dir():
            continue
        
        # If known datatype, filter by extension recursively
        if sub.name in _DATATYPE_EXT:
            ext = _DATATYPE_EXT[sub.name]
            for f in sub.rglob(f"*{ext}"):
                if f.is_file():
                    ids.add(f.stem)
        # Fallback: if not a known datatype, we skip it to avoid noise.
        # (The system requires datatypes to be in _DATATYPE_EXT anyway)

    return sorted(ids)


def list_datatypes(encoded_dir: Path) -> List[str]:
    """Return supported datatypes inferred from populated subdirectories."""
    if not encoded_dir.exists():
        return []
    found: Set[str] = set()
    for subdir in encoded_dir.iterdir():
        if subdir.is_dir() and subdir.name in _DATATYPE_EXT:
            try:
                next(subdir.iterdir())  # at least one entry
            except StopIteration:  # empty directory
                continue
            found.add(subdir.name)
    return sorted(found)


def list_guides(guides_dir: Path) -> List[str]:
    """Return relative paths of all guide ``.txt`` and ``.md`` files (recursive)."""
    if not guides_dir.exists():
        return []
    guides = []
    for ext in ["*.txt", "*.md"]:
        for f in guides_dir.rglob(ext):
            if f.is_file():
                guides.append(str(f.relative_to(guides_dir)))
    return sorted(guides)


def ensure_dir(path: Path) -> None:
    """Create directory (and parents) if missing (idempotent)."""
    path.mkdir(parents=True, exist_ok=True)


def _get_next_run_number(base_path: Path) -> int:
    """Find the next available run number for a given base path."""
    if not base_path.parent.exists():
        return 1
    
    # Extract the base filename pattern (everything before the extension)
    base_name = base_path.stem
    extension = base_path.suffix
    
    # Look for existing files with pattern: base_name_N.extension
    existing_numbers = []
    for existing_file in base_path.parent.iterdir():
        if existing_file.is_file() and existing_file.suffix == extension:
            # Check if it matches our pattern
            name = existing_file.stem
            if name == base_name:
                # This is the base file (no number), treat as run 1
                existing_numbers.append(1)
            elif name.startswith(base_name + "_") and name[len(base_name + "_"):].isdigit():
                # This has a number suffix
                number = int(name[len(base_name + "_"):])
                existing_numbers.append(number)
    
    if not existing_numbers:
        return 1
    
    return max(existing_numbers) + 1


def get_output_path(
    outputs_dir: Path,
    model_name: str,
    file_id: str,
    datatype: str = "mei",
    context: bool = False,
    guide: Optional[str] = None,
    dataset: Optional[str] = None,
    ext: str = ".txt",
    output_type: str = "response",  # 'response', 'prompt', or 'input'
    temperature: float = 0.0,
) -> Path:
    """Return path for model output file with deeply nested folder-based organization.

    Structure: ``outputs/<output_type>/<model>/<context-folder>/temp-<X.X>/<datatype>/<file_id>_<context>_<run><ext>``
    
    Context folder naming:
        - no-context: When context=False or no guide specified
        - context-<guide>: When context=True with specific guide (e.g., context-LLM, context-Pierre)
    
    Args:
        outputs_dir: Root outputs directory
        model_name: Name of the model (ChatGPT, Claude, Gemini)
        file_id: File identifier (e.g., Fux_CantusFirmus_C)
        datatype: Format (mei, musicxml, abc, humdrum)
        context: Whether guide/context was used
        guide: Specific guide path (required when context=True)
        dataset: Dataset name (unused in new structure)
        ext: File extension
        output_type: Type of output file ('response', 'prompt', or 'input')
        temperature: Model temperature setting (0.0-1.0)
    
    Returns:
        Path object for the output file
    """
    if not file_id:
        raise ValueError("file_id is required for output path")
    
    # Structure: outputs/<output_type>/<model>/<context-folder>/temp-<X.X>/<datatype>/
    
    # Start with output type (response/prompt/input)
    type_folder = outputs_dir / output_type
    
    # Then model
    model_folder = type_folder / model_name
    
    # Then context folder and determine context label for filename
    if context and guide:
        # Specific guide used - extract guide name from filename
        # e.g., "data/guides/Pierre-Guide.md" -> "Pierre"
        # e.g., "data/guides/LLM-Guide.md" -> "LLM"
        guide_path = Path(guide)
        guide_name = guide_path.stem  # "Pierre-Guide.md" -> "Pierre-Guide"
        # If it ends with "-Guide", take just the prefix
        if guide_name.endswith("-Guide"):
            guide_name = guide_name[:-6]  # "Pierre-Guide" -> "Pierre"
        context_folder = model_folder / f"context-{guide_name}"
        context_label = guide_name
    else:
        # No context or no guide specified
        context_folder = model_folder / "no-context"
        context_label = "no-context"
    
    # Then temperature folder
    temp_folder = context_folder / f"temp-{temperature:.1f}"
    
    # Then datatype (format)
    format_folder = temp_folder / datatype
    
    # Create the directory structure
    ensure_dir(format_folder)
    
    # Create the base filename pattern for run number detection
    # Pattern: <file_id>_<context_label>_<run>.<ext>
    base_filename = f"{file_id}_{context_label}"
    base_path = format_folder / f"{base_filename}{ext}"
    
    # Get the next run number
    run_number = _get_next_run_number(base_path)
    
    # Create the final filename with context label and run number
    final_filename = f"{file_id}_{context_label}_{run_number}{ext}"
    return format_folder / final_filename
