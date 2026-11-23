import pytest

from scripts.deploy_config import deploy_configs


def test_deploy_copies_json_file(tmp_path):
    # Arrange
    source = tmp_path / "source"
    source.mkdir()
    (source / "service.json").write_text('{"enabled": true}', encoding="utf-8")
    destination = tmp_path / "deployment"  # does not exist yet

    # Act
    copied = deploy_configs(source, destination)

    # Assert
    assert (destination / "service.json").read_text(encoding="utf-8") == '{"enabled": true}'
    assert copied == [destination / "service.json"]


def test_deploy_excludes_other_files(tmp_path):
    # Arrange: one allowed file, one that must be excluded
    source = tmp_path / "source"
    source.mkdir()
    (source / "service.json").write_text('{"enabled": true}', encoding="utf-8")
    (source / "notes.txt").write_text("internal notes", encoding="utf-8")
    destination = tmp_path / "deployment"  # must start absent

    # Act
    copied = deploy_configs(source, destination)

    # Assert: check ALL filenames in the destination, not just service.json
    assert sorted(path.name for path in destination.iterdir()) == ["service.json"]
    assert copied == [destination / "service.json"]
def test_deploy_empty_source(tmp_path):
    # Arrange: source exists but is empty (differs from the missing-source case)
    source = tmp_path / "source"
    source.mkdir()
    destination = tmp_path / "deployment"  # must start absent

    # Act
    copied = deploy_configs(source, destination)

    # Assert: destination created, empty, and [] returned
    assert destination.is_dir()
    assert list(destination.iterdir()) == []
    assert copied == []


def test_deploy_missing_source(tmp_path):
    source = tmp_path / "missing"  # deliberately not created
    destination = tmp_path / "deployment"

    # Act and assert: the function must reject a missing source
    with pytest.raises(FileNotFoundError):
        deploy_configs(source, destination)

    # The destination must not have been created
    assert not destination.exists()