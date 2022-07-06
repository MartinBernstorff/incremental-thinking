from pathlib import Path

from inc.incthink.file_processing import process_file


def test_mvp():
    filepath = Path(__file__).parent.parent / "test_files" / "test_filehandling.md"

    inbox_tag = "#inbox"
    wait_interval = 4
    n_trials = 10_000

    outputs = [
        process_file(
            filepath=filepath,
            write_files=True,
            inbox_tag=inbox_tag,
            iteration2intervals={
                2: {"inbox_interval": 3, "wait_interval": wait_interval},
            },
        )
        for i in range(n_trials)
    ]

    outputs_in_inbox = [o for o in outputs if inbox_tag in o]

    assert len(outputs_in_inbox) > 2000 and len(outputs_in_inbox) < 4000
