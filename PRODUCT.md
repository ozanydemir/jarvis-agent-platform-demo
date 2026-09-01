# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Inferred: technical reviewers evaluating agent orchestration, local policy, and human approval.

## Product Purpose

Demonstrate a conversation-first assistant that can classify a request, select a safe adapter,
apply deterministic policy, and produce an inspectable execution trace.

## Positioning

The assistant can suggest and coordinate tools, but authority remains in local allowlists and
human approval gates.

## Capabilities and Constraints

- Synthetic requests and adapters only.
- No microphone, API key, filesystem, shell, or PC control.
- No real model call is required.
- Active-development status remains visible.

## Product Principles

- Conversation first.
- Least authority by default.
- Deterministic policy outside the model.
- Every action leaves an audit trace.
