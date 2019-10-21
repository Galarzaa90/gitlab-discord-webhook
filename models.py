class BaseRequest:
    def __init__(self, **kwargs):
        self.object_kind = kwargs.get("object_kind")
        self.event_type = kwargs.get("event_type")


class IssueRequest(BaseRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.issue = Issue(**kwargs.get("object_attributes", {}))
        self.repository = Repository(**kwargs.get("repository", {}))
        self.user = User(**kwargs.get("user", {}))
        self.assignees = [User(**kwarg) for kwarg in kwargs.get("assignees", [])]
        self.labels = kwargs.get("labels")
        self.changes = Changes(**kwargs.get("changes", {}))
        self.project = Project(**kwargs.get("project", {}))


class Issue:
    def __init__(self, **kwargs):
        self.author_id = kwargs.get("author_id")
        self.closed_at = kwargs.get("closed_at")
        self.confidential = kwargs.get("confidential")
        self.created_at = kwargs.get("created_at")
        self.description = kwargs.get("description")
        self.due_date = kwargs.get("due_date")
        self.id = kwargs.get("id")
        self.iid = kwargs.get("iid")
        self.last_edited_at = kwargs.get("last_edited_at")
        self.last_edited_by = kwargs.get("last_edited_by")
        self.milestone_id = kwargs.get("milestone_id")
        self.moved_to_id = kwargs.get("moved_to_id")
        self.duplicated_to_id = kwargs.get("duplicated_to_id")
        self.project_id = kwargs.get("project_id")
        self.relative_position = kwargs.get("relative_position")
        self.state_id = kwargs.get("state_id")
        self.time_estimate = kwargs.get("time_estimate")
        self.title = kwargs.get("title")
        self.updated_at = kwargs.get("updated_at")
        self.updated_by_id = kwargs.get("updated_by_id")
        self.weight = kwargs.get("weight")
        self.url = kwargs.get("url")
        self.total_time_spent = kwargs.get("total_time_spent")
        self.human_total_time_spent = kwargs.get("human_total_time_spent")
        self.human_time_estimate = kwargs.get("state_id")
        self.assignee_ids = kwargs.get("assignee_ids", [])
        self.assignee_id = kwargs.get("assignee_id")
        self.state = kwargs.get("sate")
        self.action = kwargs.get("action")

class Changes:
    def __init__(self, **kwargs):
        self.labels = LabelChanges(**kwargs.get("labels", {}))
        self.assignees = AssigneeChanges(**kwargs.get("assignees", {}))
        self.total_time_spent = SimpleChange(**kwargs.get("total_time_spent", {}))


class AssigneeChanges:
    def __init__(self, **kwargs):
        self.previous = [User(**kwarg) for kwarg in kwargs.get("previous", [])]
        self.current = [User(**kwarg) for kwarg in kwargs.get("current", [])]


class LabelChanges:
    def __init__(self, **kwargs):
        self.previous = [Label(**kwarg) for kwarg in kwargs.get("previous", [])]
        self.current = [Label(**kwarg) for kwarg in kwargs.get("current", [])]


class SimpleChange:
    def __init__(self, **kwargs):
        self.previous = kwargs.get("previous")
        self.current = kwargs.get("current")


class PushRequest(BaseRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.before = kwargs.get("before")
        self.after = kwargs.get("after")
        self.ref = kwargs.get("ref")
        self.checkout_sha = kwargs.get("checkout_sha")
        self.message = kwargs.get("message")
        self.user_id = kwargs.get("user_id")
        self.user_name = kwargs.get("user_name")
        self.user_email = kwargs.get("user_email")
        self.user_avatar = kwargs.get("user_avatar")
        self.project_id = kwargs.get("project_id")
        self.project = Project(**kwargs.get("project", {}))
        self.commits = [Commit(**kwarg) for kwarg in kwargs.get("commits", [])]
        self.repository = Repository(**kwargs.get("repository", {}))
        self.total_commits_count = kwargs.get("total_commits_count")

    @property
    def branch(self):

        return self.ref.replace("refs/heads/", "")


class Project:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.web_url = kwargs.get("web_url")
        self.avatar_url = kwargs.get("avatar_url")
        self.git_ssh_url = kwargs.get("git_ssh_url")
        self.git_http_url = kwargs.get("git_http_url")
        self.namespace = kwargs.get("namespace")
        self.visibility_level = kwargs.get("visibility_level")
        self.path_with_namespace = kwargs.get("path_with_namespace")
        self.default_branch = kwargs.get("default_branch")
        self.ci_config_path = kwargs.get("ci_config_path")
        self.homepage = kwargs.get("homepage")
        self.url = kwargs.get("url")
        self.ssh_url = kwargs.get("ssh_url")
        self.http_url = kwargs.get("http_url")

    def __repr__(self):
        return "<Project name=%r namespace=%r>" % (self.name, self.namespace)


class Commit:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.message = kwargs.get("message")
        self.timestamp = kwargs.get("timestamp")
        self.url = kwargs.get("url")
        self.author = Author(**kwargs.get("author", {}))
        self.added = kwargs.get("added")
        self.changed = kwargs.get("changed")
        self.removed = kwargs.get("removed")

    def __repr__(self):
        return "<Commit id=%r message=%r>" % (self.id, self.message)


class Author:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.email = kwargs.get("email")

    def __repr__(self):
        return "<Author name=%r email=%r>" % (self.name, self.email)


class Repository:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.url = kwargs.get("url")
        self.description = kwargs.get("description")
        self.homepage = kwargs.get("homepage")
        self.git_http_url = kwargs.get("git_http_url")
        self.git_ssh_url = kwargs.get("git_ssh_url")
        self.visibility_level = kwargs.get("visibility_level")

    def __repr__(self):
        return "<Repository name=%r>" % self.name


class User:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.username = kwargs.get("username")
        self.avatar_url = kwargs.get("avatar_url")

    def __repr__(self):
        return "<User username=%r>" % self.username

class Label:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.title = kwargs.get("title")
        self.color = kwargs.get("color")
        self.project_id = kwargs.get("project_id")
        self.created_at = kwargs.get("created_at")
        self.updated_at = kwargs.get("updated_at")
        self.template = kwargs.get("template")
        self.description = kwargs.get("description")
        self.type = kwargs.get("type")
        self.group_id = kwargs.get("group_id")

    def __repr__(self):
        return "<Label title=%r>" % self.title
