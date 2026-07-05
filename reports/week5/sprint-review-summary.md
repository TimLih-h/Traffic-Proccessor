# Sprint Review Summary

## Sprint Goal
The goal of Sprint was to deliver MVP v2 by improving traffic visibility, access control, Docker deployment structure, and maintainability of the system.

## Delivered Increment
During this Sprint, we delivered the following MVP v2 improvements:
- Added a Gate component as an HTTP reverse proxy in front of a protected target container.
- Added mock-target as an example protected container behind Gate.
- Added IP-based blocking using `BLOCKED_IPS`.
- Verified that CNSS does not receive requests from blocked client IPs.
- Added a Top IPs list to show the most active source/client IP addresses.
- Updated the dashboard design and improved the traffic graph view.
- Moved Gate and error server files into the `src` directory.
- Updated Docker Compose configuration for the Gate setup.

## Customer Feedback Addressed
The Sprint focused on improving system visibility and access control. The updated dashboard makes traffic data easier to understand, while the Gate component adds a first access-control layer before the protected mock-target container.

## UAT Results
The main user-facing behavior was tested manually:
- Allowed client IPs can access the protected mock-target through Gate.
- Mock-target does not process requests from blocked client IPs
- The dashboard displays updated traffic information, including Top IPs and graph improvements.

## Architecture and Workflow Updates
The architecture was updated by introducing Gate as a separate reverse proxy service before the protected mock-target container. External traffic now goes through Gate first, while mock-target stays behind Gate inside the Docker network. The PR was also retargeted to the `dev` branch before merging, and Gate-related source files were moved into `src` to match the project structure.

## Quality and CI Evidence
Manual testing confirmed both allow and deny modes for IP filtering. Docker configuration was adjusted and tested locally. Further CI and integration testing should continue after merging into `dev`.

## Remaining Gaps and Follow-up Work
- Connect Gate blacklist management with CNSS/backend so blocked IPs can be modified from the web interface.
- Decide whether the separate error server is still needed.
- Continue testing the full Docker setup after merge.
- Improve automated test coverage for Gate and dashboard behavior.

## Product Backlog Updates
Follow-up work should include backend-managed blacklist support, further dashboard improvements, and additional Docker/integration testing.
