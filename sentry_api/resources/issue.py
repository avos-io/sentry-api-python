from urllib.parse import quote_plus, urljoin

from sentry_api.path.projects_path import project_issues_path
from sentry_api.path.organizations_path import org_issues_events_path, org_issues_tags_path, org_issues_tags_values_path
from sentry_api.resources.pagination import SentryApiPage
from .base import BaseResource

class IssuesResource(BaseResource):
    """
    Sentry API: https://docs.sentry.io/api/events/
    """

    def list(self, project_slug: str):
        """
        Sentry API: https://docs.sentry.io/api/events/list-a-projects-issues/
        """
        return SentryApiPage(self.http_client, "get", project_issues_path(self.organization_slug, project_slug))

    def get_events(self, issue_id: str, full = False):
        """
        Sentry API: https://docs.sentry.io/api/events/list-an-issues-events/
        """
        if full:
            query_params = "?full=true"
        return SentryApiPage(self.http_client, "get", urljoin(org_issues_events_path(self.organization_slug, issue_id), query_params))

    def get_events_query(self, issue_id: str, query: str):
        return SentryApiPage(self.http_client, "get", urljoin(org_issues_events_path(self.organization_slug, issue_id),f'?query={quote_plus(query)}'))

    def get_tag_details(self, issue_id: str, key: str):
        """
        Sentry API: https://docs.sentry.io/api/events/retrieve-tag-details/
        """
        return SentryApiPage(self.http_client, "get", org_issues_tags_path(self.organization_slug, issue_id, key))

    def get_tag_values(self, issue_id: str, key: str):
        """
        Sentry API: https://docs.sentry.io/api/events/list-a-tags-values-related-to-an-issue/
        """
        return SentryApiPage(self.http_client, "get", org_issues_tags_values_path(self.organization_slug, issue_id, key))

