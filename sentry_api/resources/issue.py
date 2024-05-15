from .base import BaseResource

class IssueResource(BaseResource):
    """
    Sentry API: https://docs.sentry.io/api/events/
    """

    def events(self, issue_id: str):
        """
        Sentry API: https://docs.sentry.io/api/events/list-an-issues-events/
        """
        return self.http_client.make_a_call("get", f"organizations/{self.organization_slug}/issues/{issue_id}/events/")
