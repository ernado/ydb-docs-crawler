---
title: "YDB documentation genres"
url: "https://ydb.tech/docs/en/contributor/documentation/genres?version=v26.1"
doc_path: "en/contributor/documentation/genres"
version: "v26.1"
lang: "en"
source_path: "en/core/contributor/documentation/genres.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/contributor/documentation/genres.md"
description: "This article complements YDB documentation style guide by describing the main genres used in YDB documentation. Understanding these genres helps contributors pl"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# YDB documentation genres

This article complements [YDB documentation style guide](style-guide.md) by describing the main genres used in YDB documentation. Understanding these genres helps contributors place new content in the appropriate section and maintain a consistent structure.

## Theory

**Primary goal for the reader:** build a solid knowledge foundation by understanding the fundamental concepts, architecture, and principles behind YDB.

- Introduces key concepts and terminology
- Explains how things work both from the user's perspective and under the hood
- Provides high-level overviews of system components
- Helps users understand the "why" behind design decisions
- Can be targeted at either a broad audience with minimal prior knowledge or a specific role
- Can include diagrams and other visualizations to help convey information

Theory documentation is primarily found in the ["Concepts"](../../concepts/index.md) section but also appears in role-specific folders when the theoretical information is relevant only to a particular audience.

## Guide

**Primary goal for the reader:** accomplish a specific practical task or implement a particular solution with YDB by following instructions.

Guides are practical, step-by-step instructions that help users accomplish a specific goal with YDB. Each article in this genre:

- Provides a clear goal and sequential instructions to achieve it
- Includes concrete examples and commands
- Focuses on practical implementation
- Addresses specific use cases or scenarios
- Can include screenshots to illustrate steps

Guides are primarily found in role-specific folders like ["For DevOps"](../../devops/index.md), ["For Developers"](../../dev/index.md), and ["For Security Engineers"](../../security/index.md), as well as in the ["Troubleshooting"](../../troubleshooting/index.md) section.

## Reference

**Primary goal for the reader:** find additional information about a specific niche topic related to YDB.

Reference documentation provides comprehensive, detailed information about YDB components, queries, APIs, configuration options, CLI commands, UI pages, and more. This genre:

- Aims for completeness and precision
- Serves as a lookup resource for specific details
- Documents all available options, parameters, and settings
- Is organized for quick information retrieval via a search engine or [LLM](https://en.wikipedia.org/wiki/Large_language_model)
- Includes syntax, data types, parameters, return values, defaults, configuration, and examples

Reference documentation is designed to be found as needed and is the most detailed level of documentation. It's particularly useful when users need specific information about functions, settings, or keywords. This content is primarily found in the ["Reference"](../../reference/index.md) section.

## FAQ

**Primary goal for the reader:** quickly find answers to common questions encountered when working with YDB.

Frequently Asked Questions (FAQ) documentation answers common questions about YDB in a direct question-and-answer format. This genre:

- Addresses specific, commonly asked questions
- Provides concise, focused answers
- Is organized by topic or category
- Helps users quickly find solutions to common problems
- Is optimized for search engine or LLM discovery

FAQ content is primarily found in the ["Questions and answers"](../../faq/index.md) section and is designed to help users who are searching for specific solutions to common situations.

## Recipe

**Primary goal for the reader:** implement a specific, focused solution to a common issue or use case with YDB.

Recipes are short, focused mini-guides that demonstrate how to accomplish specific tasks with YDB. This genre:

- Provides concise solutions to specific problems
- Includes code snippets and examples
- Focuses on practical implementation
- Is more targeted and narrower in scope than full-fledged [guides](genres.md#guide)
- Often follows a problem-solution format

Recipes are primarily found in the ["Recipes"](../../recipes/index.md) section, though similar content may also appear in role-specific folders.

## Release notes

**Primary goal for the reader:** stay informed about new features, improvements, bug fixes, and breaking changes in YDB releases.

Release notes document changes, improvements, and fixes in each new version of YDB. This genre:

- Lists new features and enhancements
- Documents bug fixes and resolved issues
- Highlights breaking changes and deprecations
- Provides upgrade instructions when necessary
- Is organized chronologically by version number

Release notes are found in the ["Changelog"](../../changelog-server.md) section and help users understand what has changed between versions and decide whether to upgrade.

## Collection of links {#links}

**Primary goal for the reader:** discover additional resources, learning materials, and external content related to YDB.

Collections of links provide curated lists of resources related to YDB. This genre:

- Aggregates related external or internal resources
- Provides brief descriptions of each linked resource
- May be organized by topic, format, or relevance
- Helps users discover additional learning materials
- Can include videos, articles, downloads, and other content

Collections of links are primarily found in the ["Public materials"](../../public-materials/videos.md) and ["Downloads"](../../downloads/index.md) sections, serving as gateways to external resources about YDB.
