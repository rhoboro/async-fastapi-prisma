import pytest
from httpx import AsyncClient

from app.tests.utils import ID_STRING


async def setup_data() -> None:
    from app.models import Note, Notebook

    notebook1 = await Notebook.create(title="Notebook 1", notes=[])
    notebook2 = await Notebook.create(title="Notebook 2", notes=[])

    note1 = Note.create(title="Note 1", content="Content 1", notebook_id=notebook1.id)
    note2 = Note.create(title="Note 2", content="Content 2", notebook_id=notebook1.id)
    note3 = Note.create(title="Note 3", content="Content 3", notebook_id=notebook2.id)


@pytest.mark.anyio
async def test_notebooks_read_all(ac: AsyncClient) -> None:
    """Read all notebooks"""
    # setup
    await setup_data()

    # execute
    response = await ac.get(
        "/api/notebooks",
    )

    print(response.content)
    assert 200 == response.status_code
    expected = {
        "notebooks": [
            {
                "id": ID_STRING,
                "title": "Notebook 1",
                "notes": [
                    {
                        "id": ID_STRING,
                        "title": "Note 1",
                        "content": "Content 1",
                        "notebook_id": ID_STRING,
                        "notebook_title": "Notebook 1",
                    },
                    {
                        "id": ID_STRING,
                        "title": "Note 2",
                        "content": "Content 2",
                        "notebook_id": ID_STRING,
                        "notebook_title": "Notebook 1",
                    },
                ],
            },
            {
                "id": ID_STRING,
                "title": "Notebook 2",
                "notes": [
                    {
                        "id": ID_STRING,
                        "title": "Note 3",
                        "content": "Content 3",
                        "notebook_id": ID_STRING,
                        "notebook_title": "Notebook 2",
                    }
                ],
            },
        ]
    }
    assert expected == response.json()


@pytest.mark.anyio
async def test_notebooks_read(ac: AsyncClient) -> None:
    """Read a notebook"""
    from app.models import Notebook

    # setup
    await setup_data()
    notebook = [nb for nb in await Notebook.read_all(include_notes=True)][0]

    # execute
    response = await ac.get(
        f"/api/notebooks/{notebook.id}",
    )

    print(response.content)
    assert 200 == response.status_code
    expected = {
        "id": notebook.id,
        "title": "Notebook 1",
        "notes": [
            {
                "id": ID_STRING,
                "title": "Note 1",
                "content": "Content 1",
                "notebook_id": ID_STRING,
                "notebook_title": "Notebook 1",
            },
            {
                "id": ID_STRING,
                "title": "Note 2",
                "content": "Content 2",
                "notebook_id": ID_STRING,
                "notebook_title": "Notebook 1",
            },
        ],
    }
    assert expected == response.json()


@pytest.mark.anyio
async def test_notebooks_create(ac: AsyncClient) -> None:
    """Create a notebook"""
    # execute
    response = await ac.post("/api/notebooks", json={"title": "Test Notebook", "notes": []})

    print(response.content)
    assert 200 == response.status_code
    expected = {"id": ID_STRING, "title": "Test Notebook", "notes": []}
    assert expected == response.json()


@pytest.mark.anyio
async def test_notebooks_update(ac: AsyncClient) -> None:
    """Update a notebook"""
    from app.models import Notebook

    # setup
    await setup_data()
    notebook = [nb for nb in await Notebook.read_all(include_notes=True)][0]
    assert "Notebook 1" == notebook.title
    assert 2 == len(notebook.notes)
    note = notebook.notes[0]

    # execute
    response = await ac.put(
        f"/api/notebooks/{notebook.id}", json={"title": "Test Notebook", "notes": [note.id]}
    )

    print(response.content)
    assert 200 == response.status_code
    expected = {
        "id": notebook.id,
        "title": "Test Notebook",
        "notes": [
            {
                "id": ID_STRING,
                "title": "Note 1",
                "content": "Content 1",
                "notebook_id": ID_STRING,
                "notebook_title": "Test Notebook",
            }
        ],
    }
    assert expected == response.json()

    assert "Test Notebook" == notebook.title
    assert 1 == len(notebook.notes)


@pytest.mark.anyio
async def test_notebooks_delete(ac: AsyncClient) -> None:
    """Delete a notebook"""
    from app.models import Note, Notebook

    # setup
    await setup_data()
    notebooks = [nb for nb in await Notebook.read_all(include_notes=True)]
    assert 2 == len(notebooks)
    notes = [n for n in await Note.read_all()]
    assert 3 == len(notes)

    # execute
    response = await ac.delete(
        f"/api/notebooks/{notebooks[0].id}",
    )

    print(response.content)
    assert 204 == response.status_code

    notebooks = [nb for nb in await Notebook.read_all(include_notes=True)]
    assert 1 == len(notebooks)

    # delete-orphan
    notes = [n for n in await Note.read_all()]
    assert 1 == len(notes)
