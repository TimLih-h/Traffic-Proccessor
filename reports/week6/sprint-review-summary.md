# Sprint Review Summary – Week 6 (Sprint 4)

**Sprint Dates:** 6 July 2026 – 12 July 2026
**Sprint Goal:** General improvement on MVP v2, preparations for customer handover
**Total Sprint Size:** 13 Story Points

## Delivered Increment

During this Sprint, we delivered the following improvements as part of the Week 6 trial-release (version **2.1.0**):

- **Separated CNSS and Traffic Processor startup** – services can now be started independently for better development and operational flexibility.
- **Website UI overhaul** – the user interface was redesigned and improved for a cleaner, more intuitive experience.
- **Prepared customer handover materials** – updated architecture, testing, and roadmap documentation in the `docs/` folder.

## Customer Feedback Addressed

The Sprint focused on addressing customer concerns and improving the overall quality of the system:

- Customer feedback indicated that the README was sparse, though other parts were acceptable.
- All customer feedback has been addressed.
- Based on customer input, **[PBI-11](https://github.com/SWP-Team-46/Traffic-Proccessor/issues/121) was created** to track follow-up work.

## UAT Results

The main user-facing behavior was tested manually:

- The separated startup流程 (CNSS and TP) works as expected.
- The UI overhaul improves visibility and usability of traffic data.
- The system remains accessible via the [Week 6 product access artifact](http://localhost:38080/static/index.html).

## Architecture and Workflow Updates

The architecture was refined in preparation for handover:

- CNSS and Traffic Processor startup were **decoupled**, allowing each service to run independently.
- Documentation was updated, including:
  - [Architecture Overview](https://github.com/SWP-Team-46/Traffic-Proccessor/blob/Asignment-6/reports/week6/docs/architecture)
  - [Testing & Quality](https://github.com/SWP-Team-46/Traffic-Proccessor/blob/Asignment-6/reports/week6/docs/testing.md)
  - [Roadmap](https://github.com/SWP-Team-46/Traffic-Proccessor/blob/Asignment-6/reports/week6/docs/roadmap.md)

## Quality and CI Evidence

- Manual testing confirmed the separated startup and UI changes work as expected.
- Documentation updates were reviewed and merged.
- Further CI and integration testing should continue as part of Week 7 follow-up work.

## Remaining Gaps and Follow-up Work

As part of the transition to customer handover, the following items remain for **Week 7**:

- **Bug fixes** – address any remaining issues identified during testing.
- **VM-to-VM compatibility** – add support for running the system across virtual machines.
- **Continue testing** – perform additional integration and end-to-end testing.
- **Formal handover** – complete the customer handover process.

## Product Backlog Updates

- [PBI-11](https://github.com/SWP-Team-46/Traffic-Proccessor/issues/121) was created to capture customer feedback-related work.
- Follow-up work includes bug fixes, VM-to-VM compatibility, and final handover preparations.
