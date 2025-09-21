#!/usr/bin/env python3
"""Test client module
"""
import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient

try:
    from fixtures import org_payload, repos_payload, expected_repos, apache2_repos
except ImportError:
    import fixtures
    org_payload = fixtures.org_payload
    repos_payload = fixtures.repos_payload
    expected_repos = fixtures.expected_repos
    apache2_repos = fixtures.apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient
    """

    @patch('client.get_json')
    def test_org_google(self, mock_get_json):
        """Test that GithubOrgClient.org returns correct value for google"""
        test_client = GithubOrgClient("google")
        test_client.org()
        expected_url = "https://api.github.com/orgs/google"
        mock_get_json.assert_called_once_with(expected_url)

    @patch('client.get_json')
    def test_org_abc(self, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value for abc"""
        test_client = GithubOrgClient("abc")
        test_client.org()
        expected_url = "https://api.github.com/orgs/abc"
        mock_get_json.assert_called_once_with(expected_url)

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

    def test_has_license_true(self):
        """Test GithubOrgClient.has_license returns True"""
        repo = {"license": {"key": "my_license"}}
        result = GithubOrgClient.has_license(repo, "my_license")
        self.assertTrue(result)

    def test_has_license_false(self):
        """Test GithubOrgClient.has_license returns False"""
        repo = {"license": {"key": "other_license"}}
        result = GithubOrgClient.has_license(repo, "my_license")
        self.assertFalse(result)


class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient
    """

    org_payload = org_payload
    repos_payload = repos_payload
    expected_repos = expected_repos
    apache2_repos = apache2_repos

    @classmethod
    def setUpClass(cls):
        """Set up class fixtures"""
        config = {'return_value.json.side_effect': [
            cls.org_payload, cls.repos_payload,
            cls.org_payload, cls.repos_payload
        ]}
        cls.get_patcher = patch('requests.get', **config)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Tear down class fixtures"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos method with license"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
