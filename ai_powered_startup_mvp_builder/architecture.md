System Architecture - Peer Request & Real-Time Collaboration Hub

High-Level System Diagram

+-----------------------------------------------------------------------+
|                        Client Browser (Mobile / Desktop)              |
|                                                                       |
|  +-------------------------------+  +------------------------------+  |
|  |       Requests Tab View       |  |        Chat Tab View         |  |
|  | - Submission Form & Validator |  | - Message Feed Container     |  |
|  | - Status Filter Bar           |  | - Message Composer Input     |  |
|  | - Responsive Request Cards    |  | - Unread Badge Notifier      |  |
|  +---------------+---------------+  +--------------+---------------+  |
|                  |                                 |                  |
|                  +----------------+----------------+                  |
|                                   |                                   |
|                        +----------v-----------+                       |
|                        |  UI State & Toast    |                       |
|                        |  Manager (Vanilla JS)|                       |
|                        +----------+-----------+                       |
+-----------------------------------|-----------------------------------+
                                    |
                          HTTPS / JSON REST API
                     (GET/POST/PATCH + Polling/SSE)
                                    |
+-----------------------------------v-----------------------------------+
|                   Val Town Serverless HTTP Backend                    |
|                                                                       |
|  +-----------------------------------------------------------------+  |
|  |                     API Router & Validation                     |  |
|  |  - GET  /api/requests       - POST /api/requests                |  |
|  |  - PATCH /api/requests/:id  - GET  /api/messages                |  |
|  |  - POST /api/messages       - POST /api/sessions                |  |
|  +--------------------------------+--------------------------------+  |
|                                   |                                   |
|                        +----------v-----------+                       |
|                        |  Data Access Layer   |                       |
|                        |  (Retention & Cap    |                       |
|                        |   Enforcement)       |                       |
|                        +----------+-----------+                       |
+-----------------------------------|-----------------------------------+
                                    |
                             SQL Queries (HTTP)
                                    |
+-----------------------------------v-----------------------------------+
|                     Val Town SQLite Persistence                       |
|                                                                       |
|   +-------------------+   +-------------------+   +---------------+   |
|   |   Users/Sessions  |   |     Requests      |   |   Messages    |   |
|   |     (<= 100)      |   |     (<= 200)      |   |   (<= 500)    |   |
|   +-------------------+   +-------------------+   +---------------+   |
+-----------------------------------------------------------------------+


Component Breakdown

1. Frontend Layer (HTML5 / CSS3 / Vanilla JS)

Tab Controller: Manages client-side switching between the Requests view and Chat view without full page reloads, preserving scroll position and form state.

Responsive Layout Engine: Uses CSS Grid (auto-fit, minmax) for request cards and Flexbox for the chat viewport so the interface scales cleanly across mobile (375px) and desktop (1440px+) viewports.

Feedback & Sync Manager: Displays non-blocking toast notifications on API success/error responses and periodically syncs new requests and messages from the backend.

2. Backend Layer (Val Town HTTP Val)

REST Endpoints: Handles incoming JSON payloads, validates required fields and string lengths, and returns standardized HTTP status codes (200, 201, 400, 404, 500).

Retention Guard: Automatically prunes oldest records if table counts exceed MVP constraints (200 requests, 500 messages).

3. Data Persistence Layer (Val Town SQLite)

Stores lightweight user session profiles, structured help requests, and chronological chat messages with indexed timestamps for fast retrieval.
