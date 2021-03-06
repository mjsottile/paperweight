#!/usr/bin/env python
# encoding: utf-8
"""
Utilities for reading content in git repositories.

- :func:`read_git_blob` will read unicode text from a git commit (given a
  commit reference and a file path.
"""

import git
import os


def read_git_blob(commit_ref, path, root='.'):
    """Get text from a git blob.

    Parameters
    ----------
    commit_ref : str
        Any SHA or git tag that can resolve into a commit in the
        git repository.
    path : str
        Path to the document in the git repository, relative to the root
        of the repository.
    root : str
        Path from current working directory to the root of the git repository.

    Returns
    -------
    text : unicode
        The document text.
    """
    repo = git.Repo(root)
    tree = repo.tree(commit_ref)
    dirname, fname = os.path.split(path)
    text = None
    if dirname == '':
        text = _read_blob(tree, fname)
    else:
        components = path.split(os.sep)
        text = _read_blob_in_tree(tree, components)
    return text


def _read_blob_in_tree(tree, components):
    """Recursively open trees to ultimately read a blob"""
    if len(components) == 1:
        # Tree is direct parent of blob
        return _read_blob(tree, components[0])
    else:
        # Still trees to open
        dirname = components.pop(0)
        for t in tree.trees:
            if t.name == dirname:
                return _read_blob_in_tree(t, components)


def _read_blob(tree, filename):
    for blb in tree.blobs:
        if blb.name == filename:
            txt = unicode(blb.data_stream.read(), 'utf-8')
            # txt = txt.encode('utf-8')
            return txt
    return None
