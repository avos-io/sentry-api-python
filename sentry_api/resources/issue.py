from urllib.parse import quote_plus, urljoin

from sentry_api.resources.pagination import get_all_pages
from .base import BaseResource

class IssuesResource(BaseResource):
    """
    Sentry API: https://docs.sentry.io/api/events/
    """
    org_slug_path = "organizations/{organization_slug}/"
    def __project_issues_path(self, project_slug: str):
        return f"projects/{self.organization_slug}/{project_slug}/issues/"
    def __org_issues_events_path(self, issue_id: str):
        return f"organizations/{self.organization_slug}/issues/{issue_id}/events/"
    def __org_issues_tags_path(self, issue_id: str, key: str):
        return f"organizations/{self.organization_slug}/issues/{issue_id}/tags/{key}/"
    def __org_issues_tags_values_path(self, issue_id: str, key: str):
        return f"{self.__org_issues_tags_path(issue_id, key)}values/"

    def list(self, project_slug: str):
        """
        Sentry API: https://docs.sentry.io/api/events/list-a-projects-issues/
        """
        return self.http_client.make_a_call("get", self.__project_issues_path(project_slug))

    def list_all(self, project_slug: str):
        """
        Page through all issues in a project and return list of issues
        """
        return get_all_pages(self, urljoin(self.http_client.endpoint_url, self.__project_issues_path(project_slug)))

    def get_events(self, issue_id: str):
        """
        Sentry API: https://docs.sentry.io/api/events/list-an-issues-events/
        """
        return self.http_client.make_a_call("get", self._issue_events_path(issue_id))

    def get_events_query(self, issue_id: str, query: str):
        return self.http_client.make_a_call("get", urljoin(self.__org_issues_events_path(issue_id),f'?query={quote_plus(query)}'))

    def get_events_all(self, issue_id: str):
        """
        Page through all events for an issue and return list of events
        """
        return get_all_pages(self, urljoin(self.http_client.endpoint_url, self.__org_issues_events_path(issue_id)))

    def get_tag_details(self, issue_id: str, key: str):
        """
        Sentry API: https://docs.sentry.io/api/events/retrieve-tag-details/
        """
        return self.http_client.make_a_call("get", self.__org_issues_tags_path(issue_id, key))

    def get_tag_values(self, issue_id: str, key: str):
        """
        Sentry API: https://docs.sentry.io/api/events/list-a-tags-values-related-to-an-issue/
        """
        return self.http_client.make_a_call("get", self.__org_issues_tags_values_path(issue_id, key))

    def get_tag_values_all(self, issue_id: str, key: str):
        """
        Sentry API: https://docs.sentry.io/api/events/list-an-issues-events/
        """
        return get_all_pages(self, urljoin(self.http_client.endpoint_url, self.__org_issues_tags_values_path(issue_id, key)))
