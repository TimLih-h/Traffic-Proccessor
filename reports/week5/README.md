# Traffic Processor (TP)

## Project Information

**Project Name:** Traffic Processor (TP)  
**Short Description:** A network visibility and control tool that captures live packet counters, per-connection statistics, traffic history, and supports blocking, tunneling, and failover behaviours.  
**LICENSE:** [LICENSE](/LICENSE)

1. [Product Backlog board](https://github.com/SWP-Team-46/Traffic-Proccessor/issues)
2. [Sprint Backlog board](https://github.com/orgs/SWP-Team-46/projects/3)
3. [Sprint 3 milestone](https://github.com/SWP-Team-46/Traffic-Proccessor/milestone/3)
4. Deliver MVP v2, 2026-06-29 - 2026-07-05, Add traffic gate, add more data for analysing
5. **18** story points for the current sprint, much more than previous velocity
6. Add traffic gate, added per-IP data to be displayed, UI changes, backend changes
7. Link to the relevant [product access artifact](http://147.45.234.218:8080)
8. [Run instructions](/README.md)
9. Customer feedback response table with feedback points and resulting PBIs or issues

| Customer Feedback | Resulting PBI / Issue |
|-------------------|------------------------|
| Customer suggested testing the software with real application | Find opensource docker application and test the software with it as a target |
| Frontend block buttons are non‑functional. | Implement missing buttons functionality to enable full UI interaction. |
| Cutomer wants to know max throughput capability. | Implement stresstests to check not only the lowerbound, but the upperbounds to. |

11. All the provided feedback was addressed
12. [Roadmap](/docs/roadmap.md)
13. [Definition of done](/docs/definition-of-done.md)
14. [Testing](/docs/testing.md)
15. [Quality requirements](/docs/quality-requirements.md)
16. [Quality requirements tests](/docs/quality-requirement-tests.md)
17. [User acceptance tests](/docs/user-acceptance-tests.md)
18. [Development proccess](/docs/development-process.md)
19. [Architecture](/docs/architecture/README.md)
20. [Static](/docs/architecture/static-view), [Dynamic](/docs/architecture/dynamic-view), [Deployment](/docs/architecture/deployment-view)
21. [ADR directory](/docs/architecture/adr)
22. The Traffic Processor (packet sniffer) and CNSS (FastAPI dashboard) communicate asynchronously via HTTP, enabling real‑time visibility while keeping components loosely coupled and deployable via Docker Compose
23. Asynchronous HTTP and in‑memory storage (ADR‑001/002) ensure sub‑second dashboard updates; Scapy (ADR‑003) keeps startup fast and throughput adequate
24. CI runs linting, unit/integration tests, coverage (≥30% threshold), Docker build, and a smoke test; the latest run passed
25. [CI pipeline](/.github/workflows/main.yml)
26. [latest protected-default-branch CI run](https://github.com/SWP-Team-46/Traffic-Proccessor/actions) <!--Finish the link-->
27. [MVP v2 release](https://github.com/SWP-Team-46/Traffic-Proccessor/releases/tag/2.0.0)
28. [Changelog](/CHANGELOG.md)
29. Public sanitized demo video shorter than two minutes - not done
30. All four UAT tests (UAT-001, UAT-002, UAT-003, and UAT-004) executed during Sprint 2 passed successfully, covering live traffic statistics, Docker Compose operation, directional packet classification, and the additional validation introduced in the assignment-5 branch, the customer reported no critical issues
31. Link to the hosted documentation site - not done
32. [Sprint Review transcript](/reports/week5/sprint-review-transcript.md)
33. [Sprint review summary](reports/week5/sprint-review-summary.md)
34. [Reflection](reports/week5/reflection.md)
35. [Retrospective](reports/week5/retrospective.md)
36. [LLM report](reports/week5/llm-report.md)
37. The main branch delivers a working Traffic Processor with packet capture, CNSS dashboard, blocking, tunneling, and separate in/out counters
38. Polishing, stresstesting, improving throughtput, add more statistics and ability to export them
39. Contribution traceability table mapping each team member to issues, PRs or MRs, review activity, testing, quality, automation, architecture, or documentation work
    
| Team member | Issues / work items | Pull requests / merge requests | Review activity | Testing, quality, and automation work | Architecture and documentation work |
|---|---|---|---|---|---|
| [`mrZom49`](https://github.com/mrZom49) | Opened [#94 — Assignment 5 task](https://github.com/SWP-Team-46/Traffic-Proccessor/issues/94). | [#106 — Update CHANGELOG for version 2.0.0](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/106); [#107 — Fix typo in changelog](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/107). | Approved [#102](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/102). | Reviewed the test-update PR [#102](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/102); repository checks passed on the reviewed and authored PRs. | Updated release documentation through [#106](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/106) and [#107](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/107), and published [release 2.0.0](https://github.com/SWP-Team-46/Traffic-Proccessor/releases/tag/2.0.0). |
| [`TimLih-h`](https://github.com/TimLih-h) | Opened [#98 — Docker structure redesign](https://github.com/SWP-Team-46/Traffic-Proccessor/issues/98) and [#99 — Per-IP statistics and management-traffic filtering](https://github.com/SWP-Team-46/Traffic-Proccessor/issues/99). | [#100 — Restructurisation and Traffic Processor upgrade](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/100); [#103 — Dev branch update and issue-closure fix](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/103); [#105 — Bug fix](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/105). | Approved [#97](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/97), [#101](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/101), [#102](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/102), [#106](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/106), and [#107](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/107). | Reviewed backend and test changes in [#101](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/101) and [#102](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/102); contributed integration and bug-fix work in [#103](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/103) and [#105](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/105). | Redesigned Docker/network structure, Traffic Processor data flow, per-IP tracking, and management-traffic filtering in [#100](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/100); synchronized the development branch in [#103](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/103). |
| [`jan-ajata`](https://github.com/jan-ajata) | Implemented work linked to [#10 — Graphical representation](https://github.com/SWP-Team-46/Traffic-Proccessor/issues/10) through PR [#104](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/104). | [#104 — Update frontend and configure Docker](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/104). | Approved and merged [#100](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/100). | Performed architecture/configuration review of [#100](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/100) against the repository reviewer checklist. | Updated the frontend and Docker configuration in [#104](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/104); reviewed the Docker/network and Traffic Processor restructuring in [#100](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/100). |
| [`LimpingCoronation`](https://github.com/LimpingCoronation) | Implemented and closed [#99 — Per-IP statistics and management-traffic filtering](https://github.com/SWP-Team-46/Traffic-Proccessor/issues/99) through [#102](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/102). | [#101 — Update backend](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/101); [#102 — Update tests](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/102). | No repository-visible PR review submitted during this period. | Updated backend tests in [#101](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/101) and added the dedicated test update in [#102](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/102); both merged PRs passed repository checks. | Changed the packet-data scheme and added a reset endpoint in [#101](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/101), supporting the per-IP statistics work item. |
| [`inseeee`](https://github.com/inseeee) | Opened [#96 — Gate reverse proxy for IP-based access control](https://github.com/SWP-Team-46/Traffic-Proccessor/issues/96). | [#97 — Add Gate reverse proxy with IP-based blocking](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/97). | No repository-visible PR review submitted during this period. | Documented manual VM tests for both allowed and blocked client-IP scenarios in [#97](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/97); repository checks passed before merge. | Designed and implemented the Gate reverse-proxy service, IP blacklist enforcement, Docker integration, and internal-only CNSS exposure in [#97](https://github.com/SWP-Team-46/Traffic-Proccessor/pull/97). |


![Sprint milestone](/reports/week5/images/milestone.png)
![Board or project workflow view](/reports/week5/images/project_backboard.png)
![Latest protected-default-branch CI run](/reports/week5/images/CI_run.png)
![SemVer release](/reports/week5/images/release.png)
![Example reviewed issue-linked PR or MR](/reports/week5/images/reviewed_issue-linked_PR.png)
![Hosted docs site](/reports/week5/images/) - not done

