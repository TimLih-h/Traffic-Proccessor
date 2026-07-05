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
9. Customer feedback response table with feedback points and resulting PBIs or issues.
10. All the provided feedback was addressed
11. [Roadmap](/docs/roadmap.md)
12. [Definition of done](/docs/definition-of-done.md)
13. [Testing](/docs/testing.md)
14. [Quality requirements](/docs/quality-requirements.md)
15. [Quality requirements tests](/docs/quality-requirement-tests.md)
16. [User acceptance tests](/docs/user-acceptance-tests.md)
17. [Development proccess](/docs/development-process.md)
18. [Architecture](/docs/architecture/README.md)
19. [Static](/docs/architecture/static-view), [Dynamic](/docs/architecture/dynamic-view), [Deployment](/docs/architecture/deployment-view)
20. [ADR directory](/docs/architecture/adr)
21. The Traffic Processor (packet sniffer) and CNSS (FastAPI dashboard) communicate asynchronously via HTTP, enabling real‑time visibility while keeping components loosely coupled and deployable via Docker Compose
22. Asynchronous HTTP and in‑memory storage (ADR‑001/002) ensure sub‑second dashboard updates; Scapy (ADR‑003) keeps startup fast and throughput adequate
23. CI runs linting, unit/integration tests, coverage (≥30% threshold), Docker build, and a smoke test; the latest run passed
24. [CI pipeline](/.github/workflows/main.yml)
25. [latest protected-default-branch CI run](https://github.com/SWP-Team-46/Traffic-Proccessor/actions) <!--Finish the link-->
26. Link to the SemVer release mapped to `MVP v2`
27. [Changelog](/CHANGELOG.md)
28. Public sanitized demo video shorter than two minutes
29. Public sanitized UAT results summary
30. Link to the hosted documentation site
31. [Sprint Review transcript](/reports/week5/sprint-review-transcript.md)
32. [Sprint review summary](reports/week5/sprint-review-summary.md)
33. [Reflection](reports/week5/reflection.md)
34. [Retrospective](reports/week5/retrospective.md)
35. [LLM report](reports/week5/llm-report.md)
36. The main branch delivers a working Traffic Processor with packet capture, CNSS dashboard, blocking, tunneling, and separate in/out counters
37. Summary of the next steps
38. Contribution traceability table mapping each team member to issues, PRs or MRs, review activity, testing, quality, automation, architecture, or documentation work.
39. Embedded screenshots from `reports/week5/images/` for:

     ![Sprint milestone](/reports/week5/images/)
     ![Board or project workflow view](/reports/week5/images/)
     ![Latest protected-default-branch CI run](/reports/week5/images/)
     ![SemVer release](/reports/week5/images/)
     ![Example reviewed issue-linked PR or MR](/reports/week5/images/)
     ![Hosted docs site](/reports/week5/images/)

42. Include product access artifact screenshots where relevant or where public links may not be inspectable by graders.
