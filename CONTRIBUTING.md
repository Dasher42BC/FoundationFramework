# Overview
The Foundation is a core library for Bridge Commander modding, intended to serve a range of mods and themes, and hold a common ground of compatibility between them for integration at will.  While it cannot guarantee bug-free use of its functions, it should make correct usage as easy as possible, intuitive, and idiomatic.

As shared infrastructure, it is expected that Foundation will be forked, distributed as such, and merged.  In the Foundation's case, this is encouraged, so long as core functionality remains compatible.  The loading mechanism for Foundation is meant to make loading specific versions simple, and pruning outdated or irrelevant versions simple.

What is not widely shared infrastructure, experimental, less than 100% stable should be kept in a branch and distributed as a separate extension.  There should be no overwrites or OverrideDefs of Foundation routines themselves, and additions through injection are now highly discouraged.  Changes to the Foundation should be on put on a feature branch, and merge through pull request and review.

## Implications of Lesser GNU Public License (LGPL) and respect to third parties

The LGPL license of the Foundation is meant to protect it, and all Python code based on it, from closed-source exploitation of what others have worked on openly.  It ensures an open, level playing field for volunteers, their works in turn to be distributed under the Activision/Totally Games license.

These extra guidelines do not necessarily convey to what others base on it.  They have their own needs, policies, and update cycles apart from core Foundation.  Open source is not public domain.  Please consult the authors for permission before merging any work into a core Foundation library.

## Code quality guidelines
* Foundation now standardizes on Black auto-formatting with a line length of 160; `black -l160 _filename.py_` is the expected invocation.  Black may be found at https://black.readthedocs.io/.  This means long-established indentation standards: 4 spaces per level of indentation.  No tabs anywhere, please.  If the use of black on a Foundation file makes it difficult to compare to BC stock, consider making a temporary black-formatted copy of the stock file.  You'll find the comparison easier than usual.
* For functional review, flake8 (https://flake8.pycqa.org/en/latest/) is recommended to detect common errors in Python code.  It is overzealous about "missing" imports that are built-in to Bridge Commander, yet still recommended for detecting common mistakes.
* Free-standing print statements may be allowed in Bridge Commander's Python 1.5.2, but they interfere with important modern development tools for Python.  Use debug() calls instead.
* Python 1.5.2 `raise` statements for exceptions are not in the same format as expected by modern tools; you'll need to take extra measures to get formatting complete.  This is worth the trouble.
* The try/except functionality has been too often used to allow errors to slip by to cause failures in more obscure parts of runtime.  Please be highly specific with `except` statements.  All bare `except:` statements without a type of Error are risky.

## Branching and merging practice in git
* Foundation's main branch will represent core, essential functionality.  What's proven stable and valuable to all should merge with it from other forks and branches.
* Extensions and adaptations will be kept as separate branches; modpacks are expected to merge branches for their specific needs.  Anything that might need a different implementation should be kept as branches, merged to releases as needed.  If the feature is optional, or meant for implementation-agnostic code, or in any way might be replaced, please keep it in a branch.
* For any merging of feature branches, especially if they require conflict resolution, please name the merged branches consistent with merge_branchA_branchB.  We will have a distribution mechanism so that well-made merges are distributed and shared, the better to help people customize their mods.
