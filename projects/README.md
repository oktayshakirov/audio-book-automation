# Projects

One module per book. A project says *where the manuscript is*, *which
narrator*, and *what the target runtime is* - it does not contain the book.

Each project keeps its manuscript, plan and source audit in `book/`, which is
**git-ignored**. The text of a book that is going to be sold does not belong
in a public repo's history, but it does belong next to the recipe that builds
it, so it lives here and is simply not committed.

Rendered audio goes outside the repo entirely: it is large, and it is
regenerable from the manuscript in minutes.
