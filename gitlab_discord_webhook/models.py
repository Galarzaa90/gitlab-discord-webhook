import datetime
from typing import Annotated, Any, Generic, Literal, Optional, TypeVar

from pydantic import BaseModel, BeforeValidator


def parse_gitlab_timestamp(value: str) -> datetime.datetime:
    """Parse GitLab timestamps into datetime objects."""
    try:
        return datetime.datetime.fromisoformat(value)
    except ValueError:
        return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S %Z").replace(tzinfo=datetime.timezone.utc)


GitLabTimestamp = Annotated[datetime.datetime, BeforeValidator(parse_gitlab_timestamp)]


class SimpleUser(BaseModel):
    name: str
    username: str
    avatar_url: str


class User(BaseModel):
    id: int
    name: str
    username: str
    avatar_url: str
    email: str


class Project(BaseModel):
    id: Optional[int] = int
    name: str
    description: Optional[str]
    web_url: str
    avatar_url: Optional[str]
    git_ssh_url: str
    git_http_url: str
    namespace: str
    visibility_level: int
    path_with_namespace: str
    default_branch: str
    ci_config_path: Optional[str] = None


class Author(BaseModel):
    name: str
    email: str


class Commit(BaseModel):
    id: str
    message: str
    title: Optional[str] = None
    timestamp: datetime.datetime
    url: str
    author: Author


class Runner(BaseModel):
    id: int
    description: str
    runner_type: str
    active: bool
    is_shared: bool
    tags: list[str]


class ArtifactsFile(BaseModel):
    filename: Optional[str]
    size: Optional[int]


class Build(BaseModel):
    id: int
    stage: str
    name: str
    status: str
    created_at: str
    started_at: Optional[str]
    finished_at: Optional[str]
    duration: Optional[float]
    queued_duration: Optional[float]
    failure_reason: Optional[str]
    when: str
    manual: bool
    allow_failure: bool
    user: User
    runner: Optional[Runner]
    artifacts_file: ArtifactsFile
    environment: None


class Repository(BaseModel):
    name: str
    url: str
    description: Optional[str]
    homepage: str


class RepositoryDetails(Repository):
    git_http_url: str
    git_ssh_url: str
    visibility_level: int


class Label(BaseModel):
    id: int
    title: str
    color: str
    project_id: Optional[int]
    created_at: GitLabTimestamp
    updated_at: GitLabTimestamp
    template: bool
    description: Optional[str]
    type: str
    group_id: Optional[int]


class EscalationPolicy(BaseModel):
    id: int
    name: str


class Issue(BaseModel):
    id: int
    title: str
    assignee_ids: list[int]
    assignee_id: Optional[int]
    author_id: int
    project_id: int
    created_at: GitLabTimestamp
    updated_at: GitLabTimestamp
    position: Optional[int] = None
    branch_name: Optional[str] = None
    description: str
    milestone_id: Optional[int]
    state: str
    iid: int
    labels: list[Label]


class IssueDetails(Issue):
    updated_by_id: Optional[int]
    last_edited_at: None
    last_edited_by_id: None
    relative_position: Optional[int]
    state_id: int
    confidential: bool
    discussion_locked: Optional[bool]
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
    health_status: Optional[str]
    type: str
    url: str
    action: str
    severity: str
    escalation_status: Optional[str] = None
    escalation_policy: Optional[EscalationPolicy] = None


class MergeParams(BaseModel):
    force_remove_source_branch: str


class MergeRequest(BaseModel):
    assignee: Optional[SimpleUser] = None
    assignee_id: Optional[int]
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
    milestone_id: Optional[int]
    position: Optional[int] = None
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
    approval_rules: Optional[list[Any]] = None
    assignee_ids: list[int]
    blocking_discussions_resolved: bool
    first_contribution: bool
    head_pipeline_id: Any = None
    human_time_change: Optional[str]
    human_time_estimate: Optional[str]
    human_total_time_spent: Optional[str]
    last_edited_at: Optional[GitLabTimestamp] = None
    last_edited_by_id: Optional[int] = None
    merge_commit_sha: Optional[str] = None
    merge_error: Optional[Any] = None
    merge_params: Optional[MergeParams] = None
    merge_user_id: Optional[int] = None
    merge_when_pipeline_succeeds: Optional[bool] = None
    prepared_at: str
    reviewer_ids: list[Any]
    state_id: int
    time_change: Optional[int] = None
    time_estimate: Optional[int] = None
    total_time_spent: Optional[int] = None
    updated_by_id: Optional[int] = None
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


class Note(BaseModel):
    attachment: None = None
    author_id: int
    change_position: None = None
    commit_id: Optional[str]
    created_at: GitLabTimestamp
    discussion_id: Optional[str] = None
    id: int
    line_code: Optional[str] = None
    note: str
    noteable_id: Optional[int]
    noteable_type: str
    original_position: None = None
    position: None = None
    project_id: int
    resolved_at: None = None
    resolved_by_id: None = None
    resolved_by_push: None = None
    st_diff: Optional[StDiff] = None
    system: bool
    type: Optional[str] = None
    updated_at: GitLabTimestamp
    updated_by_id: None = None
    description: Optional[str] = None
    url: str
    action: str


class PushHookPayload(BaseModel):
    object_kind: Literal["push"]
    event_name: Literal["push"]
    before: str
    after: str
    ref: str
    ref_protected: bool
    checkout_sha: Optional[str]
    message: Optional[str] = None
    user_id: int
    user_name: str
    user_username: str
    user_email: str
    user_avatar: str
    project_id: int
    project: Project
    commits: list[Commit]
    total_commits_count: int
    push_options: Optional[Any] = None
    repository: RepositoryDetails

    @property
    def branch(self) -> str:
        return self.ref.replace("refs/heads/", "")


class IssueHookPayload(BaseModel):
    object_kind: Literal["issue"]
    event_type: Literal["issue"]
    user: User
    project: Project
    object_attributes: IssueDetails

    @property
    def issue(self) -> IssueDetails:
        return self.object_attributes


class NoteHookPayload(BaseModel):
    object_kind: Literal["note"]
    event_type: Literal["note"]
    user: User
    project_id: int
    project: Project
    object_attributes: Note
    repository: Repository
    issue: Optional[Issue] = None
    commit: Optional[Commit] = None
    merge_request: Optional[MergeRequest] = None

    @property
    def note(self) -> Note:
        return self.object_attributes


ChangeT = TypeVar("ChangeT")


class Change(BaseModel, Generic[ChangeT]):
    previous: Optional[ChangeT]
    current: Optional[ChangeT]


class MergeRequestHookPayload(BaseModel):
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
        return self.object_attributes
