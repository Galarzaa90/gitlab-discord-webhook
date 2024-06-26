from __future__ import annotations

import datetime
from typing import Any, Literal, Annotated

from pydantic import BaseModel, BeforeValidator


def parse_gitlab_timestamp(value: str):
    return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S %Z").replace(tzinfo=datetime.timezone.utc)


GitLabTimestamp = Annotated[datetime.datetime, BeforeValidator(parse_gitlab_timestamp)]


class BaseSchema(BaseModel):
    object_kind: str
    object_attributes: ObjectAttributes
    merge_request: None
    user: User
    project: Project
    commit: Commit
    builds: list[Build]


class ObjectAttributes(BaseModel):
    id: int
    iid: int
    name: None
    ref: str
    tag: bool
    sha: str
    before_sha: str
    source: str
    status: str
    detailed_status: str
    stages: list[str]
    created_at: str
    finished_at: str
    duration: int
    queued_duration: int
    variables: list[Any]
    url: str


class User(BaseModel):
    id: int
    name: str
    username: str
    avatar_url: str
    email: str


class Project(BaseModel):
    id: int
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
    ci_config_path: str | None


class Commit(BaseModel):
    id: str
    message: str
    title: str
    timestamp: datetime.datetime
    url: str
    author: Author


class Author(BaseModel):
    name: str
    email: str


class Build(BaseModel):
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
    environment: None


class Runner(BaseModel):
    id: int
    description: str
    runner_type: str
    active: bool
    is_shared: bool
    tags: list[str]


class ArtifactsFile(BaseModel):
    filename: str | None
    size: int | None


class Repository(BaseModel):
    name: str
    url: str
    description: str | None
    homepage: str


class RepositoryDetails(Repository):
    git_http_url: str
    git_ssh_url: str
    visibility_level: int


class Label(BaseModel):
    id: int
    title: str
    color: str
    project_id: int
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
    updated_at: str
    updated_by_id: int | None
    last_edited_at: None
    last_edited_by_id: None
    relative_position: int | None
    description: str
    milestone_id: None
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
    iid: int
    url: str
    state: str
    action: str
    severity: str
    escalation_status: str | None = None
    escalation_policy: EscalationPolicy | None = None
    labels: list[Label]


class MergeRequestObjectAttributes(BaseModel):
    assignee_id: None
    author_id: int
    created_at: str
    description: str
    draft: bool
    head_pipeline_id: None
    id: int
    iid: int
    last_edited_at: str | None
    last_edited_by_id: int | None
    merge_commit_sha: str | None
    merge_error: None
    merge_params: MergeParams
    merge_status: str
    merge_user_id: None
    merge_when_pipeline_succeeds: bool
    milestone_id: int | None
    source_branch: str
    source_project_id: int
    state_id: int
    target_branch: str
    target_project_id: int
    time_estimate: int
    title: str
    updated_at: str
    updated_by_id: int | None
    prepared_at: str
    assignee_ids: list[Any]
    blocking_discussions_resolved: bool
    detailed_merge_status: str
    first_contribution: bool
    human_time_change: None
    human_time_estimate: None
    human_total_time_spent: None
    labels: list[Label]
    last_commit: Commit
    reviewer_ids: list[Any]
    source: Project
    state: str
    target: Project
    time_change: int
    total_time_spent: int
    url: str
    work_in_progress: bool
    approval_rules: list[Any]
    action: str


class Note(BaseModel):
    attachment: None
    author_id: int
    change_position: None
    commit_id: str | None
    created_at: str
    discussion_id: str
    id: int
    line_code: None
    note: str
    noteable_id: int | None
    noteable_type: str
    original_position: None
    position: None
    project_id: int
    resolved_at: None
    resolved_by_id: None
    resolved_by_push: None
    st_diff: None
    system: bool
    type: None
    updated_at: str
    updated_by_id: None
    description: str
    url: str
    action: str


class IssueNote(BaseModel):
    author_id: int
    closed_at: None
    confidential: bool
    created_at: str
    description: str
    discussion_locked: None
    due_date: None
    id: int
    iid: int
    last_edited_at: None
    last_edited_by_id: None
    milestone_id: None
    moved_to_id: None
    duplicated_to_id: None
    project_id: int
    relative_position: int
    state_id: int
    time_estimate: int
    title: str
    updated_at: str
    updated_by_id: None
    weight: None
    health_status: None
    type: str
    url: str
    total_time_spent: int
    time_change: int
    human_total_time_spent: None
    human_time_change: None
    human_time_estimate: None
    assignee_ids: list[Any]
    assignee_id: None
    labels: list[Any]
    state: str
    severity: str
    customer_relations_contacts: list[Any]


class MergeParams(BaseModel):
    force_remove_source_branch: str


class MergeRequest(BaseModel):
    assignee_id: None
    author_id: int
    created_at: str
    description: str
    draft: bool
    head_pipeline_id: None
    id: int
    iid: int
    last_edited_at: str
    last_edited_by_id: int
    merge_commit_sha: str
    merge_error: None
    merge_params: MergeParams
    merge_status: str
    merge_user_id: None
    merge_when_pipeline_succeeds: bool
    milestone_id: int
    source_branch: str
    source_project_id: int
    state_id: int
    target_branch: str
    target_project_id: int
    time_estimate: int
    title: str
    updated_at: str
    updated_by_id: int
    prepared_at: str
    assignee_ids: list[Any]
    blocking_discussions_resolved: bool
    detailed_merge_status: str
    first_contribution: bool
    human_time_change: None
    human_time_estimate: None
    human_total_time_spent: None
    labels: list[Label]
    last_commit: Commit
    reviewer_ids: list[Any]
    source: Project
    state: str
    target: Project
    time_change: int
    total_time_spent: int
    url: str
    work_in_progress: bool
    approval_rules: list[Any]


class PushHookPayload(BaseModel):
    object_kind: Literal["push"]
    event_name: Literal["push"]
    before: str
    after: str
    ref: str
    ref_protected: bool
    checkout_sha: str | None
    message: str | None
    user_id: int
    user_name: str
    user_username: str
    user_email: str
    user_avatar: str
    project_id: int
    project: Project
    commits: list[Commit]
    total_commits_count: int
    push_options: Any
    repository: RepositoryDetails

    @property
    def branch(self):
        return self.ref.replace("refs/heads/", "")


class IssueHookPayload(BaseModel):
    object_kind: Literal['issue']
    event_type: Literal['issue']
    user: User
    project: Project
    object_attributes: Issue

    @property
    def issue(self) -> Issue:
        return self.object_attributes


class NoteHookPayload(BaseModel):
    object_kind: Literal['note']
    event_type: Literal['note']
    user: User
    project_id: int
    project: Project
    object_attributes: Note
    repository: Repository
    issue: IssueNote | None = None
    commit: Commit | None = None
    merge_request: MergeRequest | None = None

    @property
    def note(self) -> Note:
        return self.object_attributes


class Change(BaseModel):
    previous: str | None
    current: str


class Changes(BaseModel):
    merge_status: Change
    updated_at: Change
    prepared_at: Change


class MergeRequestHookPayload(BaseModel):
    object_kind: Literal["merge_request"]
    event_type: Literal["merge_request"]
    user: User
    project: Project
    object_attributes: MergeRequestObjectAttributes
    labels: list[Label]
    changes: Changes
    repository: Repository

    @property
    def merge_request(self) -> MergeRequestObjectAttributes:
        return self.object_attributes
