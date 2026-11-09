# AGENTS.md — Data Structures in Python: Learning Project

## Purpose

This repo is a **learning project**, not a production library. The goal is to build
real intuition for common data structures: how they work, what they make cheap or
expensive, and how to recognize when a problem calls for one.

To get there, each structure is implemented from scratch in idiomatic, modern Python,
paired with a tutorial-style write-up, tests, practice problems, and Anki flashcards.

**Success means:** the human can explain each structure's trade-offs, invariants, and
use cases from memory. They should also be able to pick the right structure for an
unfamiliar problem. Working code alone doesn't count as success.

---

## How the agent should behave (tutor mode)

The human is learning, so default to **teaching, not doing**.

- **Don't write an implementation unless asked.** When the human is building a structure,
  give hints, ask guiding questions, or point to the specific failing case first.
  Escalate to code only if they ask for it or are clearly stuck.
- **Predict, then check.** Before running code or visualizing an operation, ask the
  human to predict the outcome, e.g. "Where does 7 end up after these inserts?"
- **Always ask "what's cheap, what's expensive?"** Tie explanations back to trade-offs.
- **Show the naive version first** when explaining something, then the improvement.
  The bug or inefficiency is where the lesson is.
- **Review rather than rewrite.** When reviewing the human's code, point out issues and
  explain why. Don't silently replace their implementation.
- **Suggest flashcards.** After the human struggles with a concept or problem, suggest
  1–3 Anki cards that capture the insight (see the Anki section).
- **Scaffolding, tests, docs, tooling, and boilerplate are fair game.** Do these freely
  when asked.

---

## The 11 structures (in order)

Each one builds on the previous ones.

| # | Structure | Key lesson | Typical uses | Python stdlib analog |
|---|-----------|-----------|--------------|----------------------|
| 1 | Dynamic array | Amortized O(1) append, contiguous memory, cache locality | Almost everything | `list` |
| 2 | Hash map / hash set | O(1) average lookup; hashing, collisions, load factor | Counting, dedup, "seen before?", grouping, caching | `dict`, `set` |
| 3 | Linked list (singly + doubly) | Pointer thinking; O(1) splice when you hold the node | Building block for other structures | — |
| 4 | Stack | LIFO; models nesting and recursion | Parens matching, undo, DFS, monotonic stack | `list` |
| 5 | Queue / deque | FIFO; double-ended | BFS, scheduling, sliding window | `collections.deque` |
| 6 | Binary heap / priority queue | Cheap min/max; heap invariant | Top-K, merge K sorted, Dijkstra, running median | `heapq` |
| 7 | BST → balanced BST (AVL or red-black) | Ordered ops in O(log n); why balance matters | Ordered maps, range queries, floor/ceiling | — (none built in) |
| 8 | Trie | Prefix-keyed lookup | Autocomplete, spell check, word games | — |
| 9 | Graph (adjacency list) + BFS/DFS | Many problems are graphs in disguise | Paths, dependencies/topo sort, grids, networks | — |
| 10 | Union-find (disjoint set) | Near-O(1) connectivity with path compression + union by rank | Components, cycle detection, Kruskal | — |
| 11 | LRU cache (hash map + doubly linked list) | Combining structures so each covers the other's weakness | Caching | `functools.lru_cache` |

**Bonus (later):** segment/Fenwick tree, skip list, Bloom filter.

**Highest leverage:** hash maps (#2), heaps (#6), graphs (#9). Spend extra time on these.

---

## Repo layout

```
dsa-python/
├── AGENTS.md
├── pyproject.toml
├── src/dsa/
│   ├── linear/      # dynamic_array.py, linked_list.py, stack.py, queue.py, deque.py
│   ├── hashing/     # hash_map.py, hash_set.py
│   ├── trees/       # bst.py, avl.py, heap.py, trie.py
│   ├── graphs/      # graph.py, union_find.py
│   └── advanced/    # lru_cache.py, (bonus: skip_list.py, bloom_filter.py, segment_tree.py)
├── tests/           # mirrors src/dsa/
├── docs/            # one Markdown chapter per structure (NN-name.md)
├── problems/        # solved practice problems, grouped by structure
├── projects/        # small apply-it projects (one per structure)
├── cards/           # Anki cards: one CSV per structure
└── benchmarks/      # comparisons against stdlib
```

---

## Code conventions

- **Python 3.12+**. Use PEP 695 generics: `class LinkedList[T]: ...`
- **Use type hints where they add clarity.** Keep parameter and generic storage
  annotations, but allow inferred return types for obvious methods such as
  `__init__` and `__len__`. Don't flag missing annotations on these methods in reviews.
- **Idiomatic Python:** implement the relevant dunder methods, such as `__len__`,
  `__iter__`, `__contains__`, `__getitem__`, `__setitem__`, `__delitem__`, `__repr__`,
  and `__eq__`.
- **Inherit from `collections.abc`** where it fits (`MutableSequence`, `MutableMapping`,
  `MutableSet`). Implement the abstract methods and get the mixins for free.
- **Match the built-ins' error behavior:** raise `IndexError`, `KeyError`, `ValueError`
  the way `list`, `dict`, and `set` do.
- **Use `__slots__` on node classes.** Add a comment explaining that it saves memory.
- **Make `__repr__` useful.** For trees, consider an ASCII rendering for debugging.
- **Trees and heaps get a `_check_invariants()` method** that asserts the structure's
  invariant (BST ordering, AVL balance factors, heap property, etc.). Tests call it
  after every mutation.
- **Each module has a top docstring** with a summary, a complexity table, and a pointer
  to its `docs/` chapter.
- **Don't import the structure being implemented.** For example, `HashMap` must not use
  `dict` internally. Using a `list` as raw backing storage is fine.

### Tooling
- `pytest` for tests
- `hypothesis` for property-based tests
- `ruff` for lint and format
- `mypy --strict` (or `pyright`) for types
- Optional: `pytest-benchmark`

---

## Testing strategy

1. **Unit tests (pytest).** Cover normal cases and edge cases: empty, single element,
   duplicates, removing a missing key, out-of-range index.
2. **Property-based tests (Hypothesis). These are the most important.** Use stateful or
   model-based testing: apply a random sequence of operations to both our structure and
   a stdlib reference model, and assert they always agree. For example:
   - `HashMap` vs `dict`
   - `DynamicArray` vs `list`
   - `Heap` vs `sorted(list)`
   - `BST` vs `sorted` + `bisect`
   - `UnionFind` vs a naive set-merging model
   - `LRUCache` vs a simple `OrderedDict`-based model
   Use `hypothesis.stateful.RuleBasedStateMachine` where it fits.
3. **Invariant checks.** Call `_check_invariants()` after every operation in tests.

---

## Chapter template (`docs/NN-name.md`)

Every chapter follows this structure:

1. **Why it exists.** The problem it solves and where it shows up in real software.
2. **Mental model.** An ASCII or Mermaid diagram.
3. **Naive version.** Show the simple approach and where it breaks or is slow.
4. **The real implementation.** Walk through it piece by piece, linking to `src/`.
5. **Invariant.** The one rule that makes it work.
6. **Complexity table.** Each operation with best, average, and worst case, plus *why*.
7. **Cheap vs expensive.** A one-paragraph summary of the trade-offs.
8. **Stdlib comparison.** What Python offers instead and when to use it.
9. **When to reach for it.** Problem signals (e.g., "top K" → heap).
10. **Exercises.**
11. **Cheat card.** A 5-line summary: cheap ops, expensive ops, invariant, reach-for-it
    signals, stdlib analog.

---

## The weekly learning loop (one structure per week, roughly)

1. **See it.** Watch one explanation, then play with the structure on VisuAlgo or the
   USFCA visualizations. Try to break it (e.g., insert sorted data into a plain BST).
2. **Draw it.** Do insert, delete, and search by hand on paper with 5–6 elements.
3. **Predict, then check.** Predict outcomes, then verify with Python Tutor or a visualizer.
4. **Build it.** Implement from memory in `src/dsa/`, then write tests with Hypothesis.
5. **Write the chapter** in `docs/` using the template.
6. **Apply it.** Solve 5–8 problems from the matching NeetCode roadmap category and
   save them in `problems/<structure>/`.
7. **Mini-project.** Build one small thing in `projects/` (ideas below).
8. **Make cards.** Write 5–10 Anki cards in `cards/<structure>.csv`.
9. **Benchmark (optional).** Compare against the stdlib analog and note why it's
   faster or slower.

### Mini-project ideas
| Structure | Project |
|-----------|---------|
| Dynamic array | Text buffer with undo history |
| Hash map | Word-frequency counter / anagram grouper |
| Linked list | Music playlist with next/prev/remove |
| Stack | Expression evaluator / bracket validator |
| Queue/deque | Print-job or task scheduler simulation |
| Heap | Event scheduler / top-K trending words from a stream |
| Balanced BST | Ordered leaderboard with rank and range queries |
| Trie | Autocomplete CLI |
| Graph + BFS/DFS | Maze solver; course-prerequisite topo sort |
| Union-find | "Friends of friends" grouping / percolation simulation |
| LRU cache | Caching decorator for a slow function |

---

## Anki flashcards

Use Anki for **intuition and pattern recognition, not memorizing code.**

### Card types
1. **Trade-off:** "Linked list vs dynamic array for random access: which is better, and why?"
2. **Problem recognition (most valuable):** "Find the K largest items in a huge stream:
   which structure?" → "Min-heap of size K, O(n log k)."
3. **Invariant:** "What property must a min-heap maintain?" → "Each parent ≤ its children;
   siblings are unordered."
4. **Why:** "Why does sorted input hurt a plain BST?" → "It degenerates into a linked
   list, so operations become O(n)."
5. **Small code cloze:** "Heap parent of index i is {{c1::(i - 1) // 2}}"
6. **Diagram:** Before/after tree rotations, using Anki's Image Occlusion.

### Rules
- Make cards **right after struggling** with something. Mistakes make the best cards.
- **One idea per card.** If the answer needs bullet points, split the card.
- **Never put a whole solution on a card.** Capture the key insight only.
- **Write your own cards.** Avoid shared decks.
- 5–10 cards per structure; 10–15 minutes of review daily.

### File format
Store cards in `cards/<structure>.csv` for Anki import (fields separated by tabs or
semicolons, with Anki's notetype/deck header lines if useful). Columns:
`Front`, `Back`, `Tags`. Tag with the structure and card type, e.g.
`dsa::heap card::recognition`. Cloze cards go in a separate `*-cloze.csv`.

When asked to generate cards, follow the rules above and keep them atomic.

---

## Resources

**Visualize**
- Python Tutor — https://pythontutor.com/ (step through your own code; see pointers)
- VisuAlgo — https://visualgo.net/
- USFCA visualizations — https://www.cs.usfca.edu/~galles/visualization/Algorithms.html

**Learn**
- *Problem Solving with Algorithms and Data Structures using Python* (Miller & Ranum),
  free on Runestone Academy. Tutorial style.
- *Open Data Structures* (Pat Morin): free, rigorous, has a Python edition.
- *Data Structures and Algorithms in Python* (Goodrich, Tamassia, Goldwasser): the
  reference textbook.
- *A Common-Sense Guide to Data Structures and Algorithms* (Jay Wengrow): best for the "why."
- MIT 6.006 *Introduction to Algorithms* (MIT OpenCourseWare and YouTube).
- Abdul Bari (YouTube): trees, rotations, heaps.

**Apply**
- NeetCode roadmap — https://neetcode.io/roadmap (problems grouped by pattern)
- *The Algorithm Design Manual* (Steven Skiena): war stories and a problem catalog.
- TheAlgorithms/Python on GitHub: for comparison only, not a tutorial.

---

## Progress tracker

Update as each structure is completed.

| # | Structure | Viz | Drawn | Impl | Tests | Chapter | Problems | Project | Cards |
|---|-----------|-----|-------|------|-------|---------|----------|---------|-------|
| 1 | Dynamic array | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | Hash map / set | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | Linked list | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | Stack | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | Queue / deque | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | Heap | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | BST → AVL/RB | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 8 | Trie | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 9 | Graph + BFS/DFS | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 10 | Union-find | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 11 | LRU cache | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
