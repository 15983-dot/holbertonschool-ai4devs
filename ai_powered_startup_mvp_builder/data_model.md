Data Model - Peer Request & Real-Time Collaboration HubEntity Relationship Overview+----------------------+       1:N       +----------------------+
|        Users         |---------------->|       Requests       |
+----------------------+                 +----------------------+
| PK id (TEXT)         |                 | PK id (TEXT)         |
|    display_name      |                 | FK author_id (TEXT)  |
|    avatar_color      |                 |    title             |
|    created_at        |                 |    category          |
+----------------------+                 |    priority          |
           |                             |    description       |
           |             1:N             |    status            |
           +---------------------------->|    created_at        |
           |                             |    updated_at        |
           |                             +----------------------+
           |                                        |
           |                             1:N (Optional Link)
           |                                        v
           |             1:N             +----------------------+
           +---------------------------->|       Messages       |
                                         +----------------------+
                                         | PK id (TEXT)         |
                                         | FK sender_id (TEXT)  |
                                         | FK request_id (TEXT) |
                                         |    body              |
                                         |    created_at        |
                                         +----------------------+
Entity Definitions1. Users (Lightweight Session Profiles)Represents an active participant in the single-room workspace without requiring full OAuth credentials.FieldTypeConstraintsDescriptionidTEXTPRIMARY KEY, UUIDv4Unique client-generated session identifier.display_nameTEXTNOT NULL, LEN(1..30)Name displayed on request cards and chat bubbles.avatar_colorTEXTNOT NULL, Default #2563ebHex color code assigned to the user's initials badge.created_atTEXTNOT NULL, ISO-8601Timestamp when the session was first initialized.2. Requests (Structured Peer Help / Task Items)Represents a help request or task submitted through the structured request form.FieldTypeConstraintsDescriptionidTEXTPRIMARY KEY, UUIDv4Unique identifier for the request.author_idTEXTNOT NULL, FOREIGN KEY -> Users(id)Reference to the user who created the request.titleTEXTNOT NULL, LEN(3..100)Concise summary of the help or task request.categoryTEXTNOT NULL, EnumOne of: 'Debugging', 'Code Review', 'Design', 'General'.priorityTEXTNOT NULL, EnumOne of: 'Low', 'Medium', 'High'.descriptionTEXTNOT NULL, LEN(1..1000)Detailed context, error logs, or acceptance criteria.statusTEXTNOT NULL, Default 'Open'Lifecycle state: 'Open', 'In Progress', or 'Resolved'.created_atTEXTNOT NULL, ISO-8601Timestamp when the request was submitted.updated_atTEXTNOT NULL, ISO-8601Timestamp of the most recent status update.3. Messages (Real-Time Chat Feed)Represents individual messages sent within the shared Chat tab, with optional linkage to a specific request.FieldTypeConstraintsDescriptionidTEXTPRIMARY KEY, UUIDv4Unique identifier for the chat message.sender_idTEXTNOT NULL, FOREIGN KEY -> Users(id)Reference to the user who sent the message.request_idTEXTNULLABLE, FOREIGN KEY -> Requests(id)Optional reference if the message tags a specific request.bodyTEXTNOT NULL, LEN(1..500)Plain-text content of the chat message.created_atTEXTNOT NULL, ISO-8601Timestamp used for chronological message ordering.MVP Storage & Validation RulesCapacity Limits: The backend enforces a rolling cap of 200 rows in Requests and 500 rows in Messages by pruning the oldest records upon insert.Indexing: Indexes are maintained on Requests(status, created_at DESC) and Messages(created_at ASC) to ensure sub-50ms query performance.
