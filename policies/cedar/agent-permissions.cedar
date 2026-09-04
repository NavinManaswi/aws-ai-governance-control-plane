// Cedar Policy: Agent Permissions
// Fine-grained authorization for AI agents
// Based on AWS Cedar policy language for Bedrock AgentCore[reference:32]

// ============================================================================
// Policy 1: Allow read-only access to approved data sources
// ============================================================================

@id("policy-001")
permit (
    principal is Agent,
    action in [DataAction::Read, DataAction::Query],
    resource is DataSource
)
when {
    principal.hasAttribute("clearance_level") >= resource.hasAttribute("classification_level")
};
unless {
    resource.hasAttribute("sensitive_data") == true
};

// ============================================================================
// Policy 2: Allow tool execution with approval
// ============================================================================

@id("policy-002")
permit (
    principal is Agent,
    action is ToolAction::Execute,
    resource is Tool
)
when {
    principal.hasAttribute("permission_level") >= resource.hasAttribute("required_permission")
};
unless {
    resource.hasAttribute("requires_approval") == true
};

// ============================================================================
// Policy 3: Forbid high-risk actions without human escalation
// ============================================================================

@id("policy-003")
forbid (
    principal is Agent,
    action is Action::HighRisk,
    resource is Resource
)
when {
    resource.hasAttribute("risk_level") == "critical"
};

// ============================================================================
// Policy 4: Allow cost-limited operations
// ============================================================================

@id("policy-004")
permit (
    principal is Agent,
    action is Action::Any,
    resource is Resource
)
when {
    principal.hasAttribute("remaining_budget") > 0
};
unless {
    principal.hasAttribute("remaining_budget") < resource.hasAttribute("estimated_cost")
};

// ============================================================================
// Policy 5: Forbid unauthorized delegation
// ============================================================================

@id("policy-005")
forbid (
    principal is Agent,
    action is Action::Delegate,
    resource is Agent
)
unless {
    principal.hasAttribute("delegation_allowed") == true
};

// ============================================================================
// Policy 6: Allow logging and audit
// ============================================================================

@id("policy-006")
permit (
    principal is Agent,
    action is AuditAction::Log,
    resource is AuditLog
);
