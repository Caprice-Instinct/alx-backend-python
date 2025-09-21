#!/usr/bin/env python3
"""Test client module
"""
import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


def parameterized_expand(test_cases):
    """Simple parameterized decorator replacement"""
    def decorator(func):
        def wrapper(self):
            for i, case in enumerate(test_cases):
                with self.subTest(i=i):
                    func(self, *case)
        return wrapper
    return decorator


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient
    """

    @patch('client.get_json')
    def test_org(self, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        test_cases = [("google",), ("abc",)]
        for org_name, in test_cases:
            with self.subTest(org=org_name):
                test_client = GithubOrgClient(org_name)
                test_client.org()
                expected_url = f"https://api.github.com/orgs/{org_name}"
                mock_get_json.assert_called_with(expected_url)
                mock_get_json.reset_mock()

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url"""
        expected_url = "https://api.github.com/orgs/google/repos"
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": expected_url}
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, expected_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos"""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = test_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/google/repos"
            client = GithubOrgClient("google")
            repos = client.public_repos()

            self.assertEqual(repos, ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once()

    def test_has_license(self):
        """Test GithubOrgClient.has_license"""
        test_cases = [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
        for repo, license_key, expected in test_cases:
            with self.subTest(repo=repo, license_key=license_key):
                result = GithubOrgClient.has_license(repo, license_key)
                self.assertEqual(result, expected)