from .notebooks import GetNotebookQuery, ListNotebooksQuery, NotebooksMutation
from .notes import GetNoteQuery, ListNotesQuery, NotesMutation


class Query(ListNotesQuery, GetNoteQuery, GetNotebookQuery, ListNotebooksQuery):
    pass


class Mutation(NotesMutation, NotebooksMutation):
    pass


class Subscription:
    pass
