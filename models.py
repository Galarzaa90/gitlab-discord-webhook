
class BaseHook:
    """
    Contains the base elements of a GitHub Webhook Request
    """
    def __init__(self, **kwargs):
        self.object_kind = kwargs.get("object_kind")
        self.event_type = kwargs.get("event_type")
        self.repository = Repository(**kwargs.get("repository", {}))
        self.project = Project(**kwargs.get("project", {}))


class AssignableHook(BaseHook):
    """Contains the attributes assignable requests have."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = User(**kwargs.get("user", {}))
        self.labels = [Label(**kwarg) for kwarg in kwargs.get("labels", [])]
        self.changes = kwargs.get("changes", {})
        self.assignees = [User(**kwarg) for kwarg in kwargs.get("assignees", [])]


class IssueHook(AssignableHook):
    """A Issue Hook, sent went a Issue is created, updated or closed."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.issue = Issue(**kwargs.get("object_attributes", {}))


class MergeRequestHook(AssignableHook):
    """A Merge Request Hook, sent when a Merge Request is created, updated, merged or closed."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.merge_request = MergeRequest(**kwargs.get("object_attributes", {}))


class NoteHook(BaseHook):
    """A Note Hook, for comments in commits, issues and merge requests."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.note = Note(**kwargs.get("object_attributes", {}))
        self.user = User(**kwargs.get("user", {}))
        self.issue = Issue(**kwargs.get("issue", {})) if "issue" in kwargs else None
        self.commit = Commit(**kwargs.get("commit", {})) if "commit" in kwargs else None
        self.merge_request = MergeRequest(**kwargs.get("merge_request", {})) if "merge_request" in kwargs else None


class PushHook(BaseHook):
    """A Push Hook, sent every time changes are pushed to a git repository."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.before = kwargs.get("before")
        self.after = kwargs.get("after")
        self.ref = kwargs.get("ref")
        self.checkout_sha = kwargs.get("checkout_sha")
        self.message = kwargs.get("message")
        self.user_id = kwargs.get("user_id")
        self.user_username = kwargs.get("user_username")
        self.user_name = kwargs.get("user_name")
        self.user_email = kwargs.get("user_email")
        self.user_avatar = kwargs.get("user_avatar")
        self.project_id = kwargs.get("project_id")
        self.commits = [Commit(**kwarg) for kwarg in kwargs.get("commits", [])]
        self.total_commits_count = kwargs.get("total_commits_count")

    @property
    def branch(self):
        return self.ref.replace("refs/heads/", "")

    @property
    def user(self):
        return User(name=self.user_name, username=self.user_username, avatar_url=self.user_avatar)


class Author:
    """Represents a git author."""
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.email = kwargs.get("email")

    def __repr__(self):
        return "<%s name=%r email=%r>" % (self.__class__.__name__, self.name, self.email)


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
        return "<%s id=%r message=%r>" % (self.__class__.__name__, self.id, self.message)


class Issue:
    """Represents an Issue"""

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

    def __repr__(self):
        return "<%s title=%r iid=%r>" % (self.__class__.__name__, self.title, self.iid)


class Label:
    """Represents a label that can be assigned to issues or merge requests."""
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


class MergeRequest:
    """Represents a merge request"""
    def __init__(self, **kwargs):
        self.assignee_id = kwargs.get("assignee_id")
        self.author_id = kwargs.get("author_id")
        self.created_at = kwargs.get("created_at")
        self.description = kwargs.get("description")
        self.head_pipeline_id = kwargs.get("head_pipeline_id")
        self.id = kwargs.get("id")
        self.iid = kwargs.get("iid")
        self.last_edited_at = kwargs.get("last_edited_at")
        self.last_edited_by = kwargs.get("last_edited_by")
        self.merge_error = kwargs.get("merge_error")
        self.merge_params = kwargs.get("merge_params")
        self.merge_status = kwargs.get("merge_status")
        self.merge_user_id = kwargs.get("merge_user_id")
        self.merge_when_pipeline_succeeds = kwargs.get("merge_when_pipeline_succeeds")
        self.milestone_id = kwargs.get("milestone_id")
        self.source_branch = kwargs.get("source_branch")
        self.source_project_id = kwargs.get("source_project_id")
        self.state = kwargs.get("state")
        self.target_branch = kwargs.get("target_branch")
        self.target_project_id = kwargs.get("target_project_id")
        self.time_estimate = kwargs.get("time_estimate")
        self.title = kwargs.get("title")
        self.updated_at = kwargs.get("updated_at")
        self.updated_by_id = kwargs.get("updated_by_id")
        self.url = kwargs.get("url")
        self.source = Project(**kwargs.get("source", {}))
        self.target = Project(**kwargs.get("target", {}))
        self.last_commit = Commit(**kwargs.get("last_commit", {}))
        self.work_in_progress = kwargs.get("work_in_progress")
        self.total_time_spent = kwargs.get("total_time_spent")
        self.human_total_time_spent = kwargs.get("human_total_time_spent")
        self.human_time_estimate = kwargs.get("human_time_estimate")
        self.assignee_ids = kwargs.get("assignee_ids", [])
        self.action = kwargs.get("action")

    def __repr__(self):
        return "<%s title=%r iid=%r>" % (self.__class__.__name__, self.title, self.iid)


class Note:
    """Information about the note or comment."""
    def __init__(self, **kwargs):
        self.attachment = kwargs.get("attachment")
        self.author_id = kwargs.get("author_id")
        self.change_position = kwargs.get("change_position")
        self.commit_id = kwargs.get("commit_id")
        self.created_at = kwargs.get("created_at")
        self.discussion_id = kwargs.get("discussion_id")
        self.id = kwargs.get("id")
        self.line_code = kwargs.get("line_code")
        self.note = kwargs.get("note")
        self.noteable_id = kwargs.get("noteable_id")
        self.noteable_type = kwargs.get("noteable_type")
        self.original_position = kwargs.get("original_position")
        self.position = kwargs.get("position")
        self.project_id = kwargs.get("project_id")
        self.resolved_at = kwargs.get("resolved_at")
        self.resolved_by_id = kwargs.get("resolved_by_id")
        self.resolved_by_push = kwargs.get("resolved_by_push")
        self.st_diff = kwargs.get("st_diff")
        self.system = kwargs.get("system")
        self.type = kwargs.get("type")
        self.updated_at = kwargs.get("updated_at")
        self.updated_by_id = kwargs.get("updated_by_id")
        self.description = kwargs.get("description")
        self.url = kwargs.get("url")


class Project:
    """Represents a GitLab project."""
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
        return "<%s name=%r namespace=%r>" % (self.__class__.__name__, self.name, self.namespace)


class Repository:
    """Represents a git repository."""
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.url = kwargs.get("url")
        self.description = kwargs.get("description")
        self.homepage = kwargs.get("homepage")
        self.git_http_url = kwargs.get("git_http_url")
        self.git_ssh_url = kwargs.get("git_ssh_url")
        self.visibility_level = kwargs.get("visibility_level")

    def __repr__(self):
        return "<%s name=%r>" % (self.__class__.__name__, self.name)


class User:
    """Represents a user."""
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.username = kwargs.get("username")
        self.avatar_url = kwargs.get("avatar_url")

    def __repr__(self):
        return "<%s username=%r>" % (self.__class__.__name__, self.username)
