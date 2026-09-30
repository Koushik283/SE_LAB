
PROBLEM STATEMENT #02
Campus & Academic Operations Automated Rubric Assignment Evaluator

Problem Context & Overview Academic evaluators require an automated workflow to process batch code submissions, execute syntax and test suites, run rubric-based scoring breakdowns, and assign peer reviews without manual distribution overhead. Target Stakeholders / Actors: Student, Faculty Evaluator
Sample Functional Requirement (FR) Guideline Sample Requirement: FR-001 [Priority: High] Description: The system shall automatically queue uploaded student project zip files, execute pre-configured unit test suites, and generate an itemized rubric score breakdown. Sample Acceptance Criteria: Pass: Rubric breakdown is rendered with test results within 10 seconds of submission; Fail: File queue stalls or invalid rubric tally.
Sample Non-Functional Requirement (NFR) Guideline Sample Requirement: NFR-001 [Type: Performance & Security] Description: The system shall handle up to 100 concurrent project submissions without dropping queue items or exceeding 1.5 GB memory footprint. Sample Acceptance Criteria: Pass: Benchmarking tests confirm target latency and security standards under simulated peak load.
