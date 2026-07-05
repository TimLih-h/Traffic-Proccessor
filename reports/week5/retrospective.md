# Assignment 5 Retrospective

## What went well
- Added and tested the Gate component as an HTTP reverse proxy in front of CNSS.
- Verified IP-based blocking: if a client IP is blocked, CNSS does not receive traffic from this client.
- Added a Top IPs list to show the most active client/source IP addresses.
- Updated the application design and improved the traffic graph/dashboard view.

## What did not go well
- Docker networking caused some issues during local testing.
- The first Flask-based Gate had problems with the `/static` path.
- Moving files to the correct project structure and changing the PR target branch took extra time.

## What we changed compared to the previous Sprint
- Added a Gate layer before CNSS.
- Moved Gate and error server files into `src`.
- Updated the UI design, traffic graph, and Top IPs display.
- Prepared the implementation through a PR targeting the `dev` branch.

## Action points
- Connect Gate blacklist management with CNSS/backend.
- Decide whether the separate error server is still needed.
- Continue testing after merging into `dev`.
