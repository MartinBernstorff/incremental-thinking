from pathlib import Path

from inc.incthink.file_processing import process_file


def test_mvp():
    filepath = Path(__file__).parent.parent / "test_files" / "test_filehandling.md"

    file = process_file(filepath=filepath, dry_run=True)

    assert file
