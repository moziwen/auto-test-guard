import argparse
import os
import shutil
import sys
from pathlib import Path

SKILL_NAME = "auto-test-guard"
INSTALL_FILES = (
    "SKILL.md",
    "prompt-guard.txt",
)
INSTALL_DIRS = (
    "agents",
    "references",
)


def default_target_root() -> Path:
    codex_home = Path.home() / ".codex"
    return Path(os.environ.get("CODEX_HOME", codex_home)) / "skills"


def repo_root() -> Path:
    return Path(__file__).resolve().parent


def ensure_safe_target(source: Path, target: Path) -> None:
    source = source.resolve()
    target = target.resolve()

    if target == source:
        raise ValueError("Refusing to install over the repository root.")
    if source in target.parents:
        raise ValueError("Refusing to install inside the repository tree.")
    if target in source.parents:
        raise ValueError("Refusing to install to a parent of the repository tree.")


def copy_tree(source_root: Path, target_root: Path) -> None:
    for name in INSTALL_FILES:
        src = source_root / name
        if not src.exists():
            raise FileNotFoundError(f"Missing install file: {src}")
        shutil.copy2(src, target_root / name)

    for name in INSTALL_DIRS:
        src = source_root / name
        if not src.exists():
            raise FileNotFoundError(f"Missing install directory: {src}")
        shutil.copytree(src, target_root / name)


def install(target_root: Path, force: bool) -> Path:
    source_root = repo_root()
    target_root = target_root.expanduser().resolve()
    target_dir = target_root / SKILL_NAME

    ensure_safe_target(source_root, target_dir)
    target_root.mkdir(parents=True, exist_ok=True)

    if target_dir.exists():
        if not force:
            raise FileExistsError(
                f"Target already exists: {target_dir}. Re-run with --force to overwrite."
            )
        shutil.rmtree(target_dir)

    target_dir.mkdir(parents=True, exist_ok=False)
    copy_tree(source_root, target_dir)
    return target_dir


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install the auto-test-guard skill into a Codex skills directory."
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=default_target_root(),
        help="Path to the skills directory. Defaults to CODEX_HOME/skills or ~/.codex/skills.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing installation of this skill.",
    )
    args = parser.parse_args()

    try:
        installed_path = install(args.target, args.force)
    except Exception as exc:
        print(f"Install failed: {exc}", file=sys.stderr)
        return 1

    print(f"Installed {SKILL_NAME} to {installed_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
