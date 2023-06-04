# Overview
The Foundation is a core library for Bridge Commander modding, intended to serve a range of mods and themes, and hold a common ground of compatibility between them for integration at will.  While it cannot guarantee bug-free use of its functions, it should make correct usage as easy as possible, intuitive, and idiomatic.

As shared infrastructure, it is expected that Foundation will be forked, distributed as such, and merged.  In the Foundation's case, this is encouraged, so long as core functionality remains compatible.  The loading mechanism for Foundation is meant to make loading specific versions simple, and pruning outdated or irrelevant versions simple.

What is not widely shared infrastructure, experimental, less than 100% stable should be kept in a branch and distributed as a separate extension.  There should be no overwrites or OverrideDefs of Foundation routines themselves, and additions through injection are now highly discouraged.  Changes to the Foundation should be on put on a feature branch, and merge through pull request and review.

Foundation's contribution standards do not necessarily convey to what others base on it.  Projects based on Foundation will necessarily be open because of the LGPL license, and protected by the license as well.  This does not mean they have the same needs or policy regarding contribution or distribution or inclusion in core Foundation; they are expected to have their own update cycle.  Please consult their authors for permission, even though compliant mods will have the full source.

## Branching and merging practice
* Foundation's main branch will represent core, essential functionality.  What rises to the level of stability and common use should merge with it from other forks and branches.
* Extensions and adaptations will be kept as other branches; modpacks are expected to merge branches for their specific needs.
* If the feature is optional, or meant for implementation-agnostic code, or in any way might be replaced, please keep it in a branch.
* For any merging of feature branches, especially if they require conflict resolution, please name the merged branches consistent with merge_branchA_branchB.  We will have a distribution mechanism so that well-made merges are distributed and shared, the better to help people customize their mods.

## Code quality guidelines
* Foundation now standardizes on Black auto-formatting with a line length of 160; `black -l160 _filename.py_` is the expected invocation.  Black may be found at https://black.readthedocs.io/.
* Per above, Foundation files will use long-established indentation standards: 4 spaces per level of indentation.  No tabs anywhere, please.  If the use of black on a Foundation file makes it difficult to compare to BC stock, consider making a temporary black-formatted copy of the stock file.  You'll find the comparison easier than usual.
* For functional review, a "linting" tool is recommended to detect common errors in Python code.  While flake8 (https://flake8.pycqa.org/en/latest/) will be overzealous about "missing" imports that are built-in to Bridge Commander, it is still recommended for detecting common mistakes.
* Free-standing print statements may be allowed in Bridge Commander's Python 1.5.2, but they interfere with important modern development tools for Python.  Use debug() calls instead.
* Python 1.5.2 `raise` statements for exceptions are not in the same format as expected by modern tools; you'll need to take extra measures to get formatting complete.  This is worth the trouble.
* The try/except functionality has been too often used to allow errors to slip by to cause failures in more obscure parts of runtime.  Please be highly specific with `except` statements.  All bare `except:` statements without a type of Error are risky.

