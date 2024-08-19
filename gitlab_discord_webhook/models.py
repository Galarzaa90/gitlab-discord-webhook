import datetime
from typing import Annotated, Any, Generic, Literal, TypeVar

from pydantic import BaseModel, BeforeValidator


def parse_gitlab_timestamp(value: str) -> datetime.datetime:
    """Parse GitLab timestamps into datetime objects."""
    try:
        return datetime.datetime.fromisoformat(value)
    except ValueError:
        return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S %Z").replace(tzinfo=datetime.timezone.utc)


GitLabTimestamp = Annotated[datetime.datetime, BeforeValidator(parse_gitlab_timestamp)]


class SimpleUser(BaseModel):
    """Simple user information."""

    name: str
    username: str
    avatar_url: str


class User(BaseModel):
    """User information."""

    id: int
    name: str
    username: str
    avatar_url: str
    email: str


class Project(BaseModel):
    """A GitLab project (repository)."""

    id: int | None
    name: str
    description: str | None
    web_url: str
    avatar_url: str | None
    git_ssh_url: str
    git_http_url: str
    namespace: str
    visibility_level: int
    path_with_namespace: str
    default_branch: str
    ci_config_path: str | None = None


class Author(BaseModel):
    """A commit author."""

    name: str
    email: str


class Commit(BaseModel):
    """Information about a commit."""

    id: str
    message: str
    title: str | None = None
    timestamp: datetime.datetime
    url: str
    author: Author


class Runner(BaseModel):
    """Information about the runner that executed a build."""

    id: int
    description: str
    runner_type: str
    active: bool
    is_shared: bool
    tags: list[str]


class ArtifactsFile(BaseModel):
    """A file containing an artifact."""

    filename: str | None
    size: int | None


class Build(BaseModel):
    """Information about a build."""

    id: int
    stage: str
    name: str
    status: str
    created_at: str
    started_at: str | None
    finished_at: str | None
    duration: float | None
    queued_duration: float | None
    failure_reason: str | None
    when: str
    manual: bool
    allow_failure: bool
    user: User
    runner: Runner | None
    artifacts_file: ArtifactsFile
    environment: str | None


class Repository(BaseModel):
    """A git repository."""

    name: str
    url: str
    description: str | None
    homepage: str


class RepositoryDetails(Repository):
    """A repository with additional details."""

    git_http_url: str
    git_ssh_url: str
    visibility_level: int


class Label(BaseModel):
    """A label in a issue or merge request."""

    id: int
    title: str
    color: str
    project_id: int | None
    created_at: GitLabTimestamp
    updated_at: GitLabTimestamp
    template: bool
    description: str | None
    type: str
    group_id: int | None


class EscalationPolicy(BaseModel):
    id: int
    name: str


class Issue(BaseModel):
    id: int
    title: str
    assignee_ids: list[int]
    assignee_id: int | None
    author_id: int
    project_id: int
    created_at: GitLabTimestamp
    updated_at: GitLabTimestamp
    position: int | None = None
    branch_name: str | None = None
    description: str
    milestone_id: int | None
    state: str
    iid: int
    labels: list[Label]


class IssueDetails(Issue):
    updated_by_id: int | None
    last_edited_at: None
    last_edited_by_id: None
    relative_position: int | None
    state_id: int
    confidential: bool
    discussion_locked: bool | None
    due_date: None
    moved_to_id: None
    duplicated_to_id: None
    time_estimate: int
    total_time_spent: int
    time_change: int
    human_total_time_spent: None
    human_time_estimate: None
    human_time_change: None
    weight: None
    health_status: str | None
    type: str
    url: str
    action: str
    severity: str
    escalation_status: str | None = None
    escalation_policy: EscalationPolicy | None = None


class MergeParams(BaseModel):
    force_remove_source_branch: str


class MergeRequest(BaseModel):
    assignee: SimpleUser | None = None
    assignee_id: int | None
    author_id: int
    created_at: GitLabTimestamp
    description: str
    detailed_merge_status: str
    draft: bool
    id: int
    iid: int
    labels: list[Label]
    last_commit: Commit
    merge_status: str
    milestone_id: int | None
    position: int | None = None
    source: Project
    source_branch: str
    source_project_id: int
    state: str
    target: Project
    target_branch: str
    target_project_id: int
    title: str
    updated_at: GitLabTimestamp
    work_in_progress: bool


class MergeRequestDetails(MergeRequest):
    action: str
    approval_rules: list[Any] | None = None
    assignee_ids: list[int]
    blocking_discussions_resolved: bool
    first_contribution: bool
    head_pipeline_id: Any = None
    human_time_change: str | None
    human_time_estimate: str | None
    human_total_time_spent: str | None
    last_edited_at: GitLabTimestamp | None = None
    last_edited_by_id: int | None = None
    merge_commit_sha: str | None = None
    merge_error: Any | None = None
    merge_params: MergeParams | None = None
    merge_user_id: int | None = None
    merge_when_pipeline_succeeds: bool | None = None
    prepared_at: str
    reviewer_ids: list[Any]
    state_id: int
    time_change: int | None = None
    time_estimate: int | None = None
    total_time_spent: int | None = None
    updated_by_id: int | None = None
    url: str


class StDiff(BaseModel):
    diff: str
    new_path: str
    old_path: str
    a_mode: str
    b_mode: str
    new_file: bool
    renamed_file: bool
    deleted_file: bool


class LineRangePart(BaseModel):
    """Details about the start or end of a line range."""

    line_code: str
    type: str
    old_line: int | None
    new_line: int | None


class LineRange(BaseModel):
    """Describes a range between two lines."""

    start: LineRangePart
    end: LineRangePart


class Position(BaseModel):
    """Information about the position of a comment."""

    base_sha: str | None
    start_sha: str | None
    head_sha: str | None
    old_path: str | None
    new_path: str | None
    position_type: str | None
    old_line: int | None
    new_line: int | None
    line_range: LineRange | None


class Note(BaseModel):
    """A note (or comment) in GitLab."""

    attachment: None = None
    author_id: int
    change_position: Position | None = None
    commit_id: str | None
    created_at: GitLabTimestamp
    discussion_id: str | None = None
    id: int
    line_code: str | None = None
    note: str
    noteable_id: int | None
    noteable_type: str
    original_position: Position | None = None
    position: Position | None = None
    project_id: int
    resolved_at: None = None
    resolved_by_id: None = None
    resolved_by_push: None = None
    st_diff: StDiff | None = None
    system: bool
    type: str | None = None
    updated_at: GitLabTimestamp
    updated_by_id: None = None
    description: str | None = None
    url: str
    action: str


class PushHookPayload(BaseModel):
    """Payload schema for push events."""

    object_kind: Literal["push"]
    event_name: Literal["push"]
    before: str
    after: str
    ref: str
    ref_protected: bool
    checkout_sha: str | None
    message: str | None = None
    user_id: int
    user_name: str
    user_username: str
    user_email: str
    user_avatar: str
    project_id: int
    project: Project
    commits: list[Commit]
    total_commits_count: int
    push_options: Any | None = None
    repository: RepositoryDetails

    @property
    def branch(self) -> str:
        """The name of the branch."""
        return self.ref.replace("refs/heads/", "")


class IssueHookPayload(BaseModel):
    """Payload schema for a issue event."""

    object_kind: Literal["issue"]
    event_type: Literal["issue"]
    user: User
    project: Project
    object_attributes: IssueDetails

    @property
    def issue(self) -> IssueDetails:
        """Alias to access the issue's information."""
        return self.object_attributes


class NoteHookPayload(BaseModel):
    """Payload schema for note events."""

    object_kind: Literal["note"]
    event_type: Literal["note"]
    user: User
    project_id: int
    project: Project
    object_attributes: Note
    repository: Repository
    issue: Issue | None = None
    commit: Commit | None = None
    merge_request: MergeRequest | None = None

    @property
    def note(self) -> Note:
        """Alias to access the issue's information."""
        return self.object_attributes


ChangeT = TypeVar("ChangeT")


class Change(BaseModel, Generic[ChangeT]):
    """Represents a change done to an attribute."""

    previous: ChangeT | None
    current: ChangeT | None


class MergeRequestHookPayload(BaseModel):
    """Payload schema for a merge request."""

    object_kind: Literal["merge_request"]
    event_type: Literal["merge_request"]
    user: User
    project: Project
    object_attributes: MergeRequestDetails
    labels: list[Label]
    changes: dict[str, Change]
    repository: Repository
    assignees: list[User]
    reviewers: list[User]

    @property
    def merge_request(self) -> MergeRequestDetails:
        """Alias to a merge request information."""
        return self.object_attributes


class JobCommit(BaseModel):
    """Commit information."""

    id: int
    sha: str
    message: str
    author_url: str
    author_name: str
    status: str


class JobHookPayload(BaseModel):
    """Payload schema for a job event."""

    object_kind: Literal["build"]
    user: User
    commit: JobCommit
    repository: Repository
    project: Project
    environment: str | None

    build_id: int
    build_name: str
    build_stage: str
    build_status: str
    build_created_at: GitLabTimestamp
    build_started_at: GitLabTimestamp | None
    build_finished_at: GitLabTimestamp | None
    pipeline_id: int

    @property
    def job_url(self) -> str:
        """URL to the job's detail page."""
        return f"{self.project.web_url}/~/jobs/{self.build_id}"
