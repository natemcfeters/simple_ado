#!/usr/bin/env python3

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

"""Tests for the package."""

# pylint: disable=line-too-long

import os
import sys
import unittest

from . import TestDetails

sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..")))
import simple_ado  # pylint: disable=wrong-import-order


class LibraryTests(unittest.TestCase):
    """Basic tests."""

    def setUp(self) -> None:
        """Set up method."""
        self.test_config = TestDetails()
        self.client = simple_ado.ADOClient(
            username=self.test_config.username,
            tenant=self.test_config.tenant,
            project_id=self.test_config.project_id,
            repository_id=self.test_config.repository_id,
            credentials=(self.test_config.username, self.test_config.token),
            status_context="simple_ado",
        )

    def test_list_repos(self):
        """Test list repos."""
        repos = self.client.git.all_repositories()
        self.assertTrue(len(repos) > 0, "Failed to find any repos")

    def test_list_refs(self):
        """Test list refs."""
        refs = self.client.git.get_refs()
        self.assertTrue(len(refs) > 0, "Failed to find any refs")

    def test_get_commit(self):
        """Test get commit."""
        refs = self.client.git.get_refs()
        ref = refs[0]
        commit_id = ref["objectId"]
        commit = self.client.git.get_commit(commit_id)
        self.assertIsNotNone(commit)

    # TODO: We can't test this until we can also create branches
    #def test_delete_branch(self):
    #    """Test delete branch."""
    #    response = self.client.git.delete_branch("refs/heads/?", "?")
    #    for value in response:
    #        self.assertTrue(value["success"])

    def test_get_pull_requests(self):
        """Test get pull requests."""
        refs = self.client.list_all_pull_requests()
        self.assertTrue(len(refs) > 0)

    def test_get_pools(self):
        """Test get pools."""
        response = self.client.pools.get_pools()
        self.assertGreater(len(response), 0)

    def test_capabilities(self):
        """Test setting capabilities."""
        pool = self.client.pools.get_pools(action_filter=simple_ado.pools.TaskAgentPoolActionFilter.manage)[0]
        agent = self.client.pools.get_agents(pool_id=pool["id"])[0]
        capabilities = agent["userCapabilities"]
        capabilities["hello"] = "world"
        self.client.pools.update_agent_capabilities(
            pool_id=pool["id"],
            agent_id=agent["id"],
            capabilities=capabilities
        )
