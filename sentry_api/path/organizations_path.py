# Organisations
def __org_slug_path(organization_slug: str):
    return f"organizations/{organization_slug}/"

# Organisations Issues
def org_issues_path(organization_slug: str):
    return f"{__org_slug_path(organization_slug)}/issues/"

def org_issues_issue_path(organization_slug: str, issue_id: str):
    return f"{__org_slug_path(organization_slug)}/issues/{issue_id}/"

def org_issues_events_path(organization_slug: str, issue_id: str):
    return f"{org_issues_issue_path(organization_slug, issue_id)}/events/"

def org_issues_tags_path(organization_slug: str, issue_id: str, key: str):
    return f"{org_issues_issue_path(organization_slug, issue_id)}/tags/{key}/"

def org_issues_tags_values_path(organization_slug: str, issue_id: str, key: str):
    return f"{org_issues_tags_path(organization_slug, issue_id, key)}values/"

