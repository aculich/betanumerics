# Product Requirements Document (PRD): Betanumerics Identifier Generator MVP

## Overview

Build a web-based MVP application that generates short, unique, human-friendly identifiers (“betanumerics”) for users. The system should allow users to enter their email address (used as a namespace/scope), then generate and return unique identifiers via a simple web interface and API. The app will also include a hidden “slug/lug” easter egg feature triggered by a specific input.

---

## Core Features

### 1\. User Scoping & Authentication

- Users enter their email address on the main page.  
- The email is used as an opaque namespace (hashed or encoded in URLs; not visible in plain text).  
- No password or verification required; minimal security due to low threat model.

### 2\. Identifier Generation

- Generates short, random-looking strings using the “betanumerics” character set:  
  - Excludes vowels and letter L to avoid confusion.  
  - No more than two letters in a row before inserting a digit.  
  - Check digit/character at end for error detection.  
  - Starts with three-character strings; expands to four/five/etc. as needed per user scope.  
- Ensures no duplication within each user’s namespace.  
- Stateless operation: Optionally allows user to provide last string received; otherwise, system tracks last issued string per email.

### 3\. Web Interface

- Simple landing page: Enter email → receive unique identifier \+ URL containing identifier.  
- Display most recent identifiers generated for that user session.  
- Option to copy/share generated URLs.

### 4\. API Endpoint

- POST endpoint: Accepts {email} (and optionally last string); returns next unique identifier \+ URL.

### 5\. Opaque URLs

- Generated URLs are of the form:  
  `https://betanumerics.app/u/<opaque_user_id>/id/<identifier>`  
  - `<opaque_user_id>` is an encoded/hash of the user's email (not reversible from URL).  
  - `<identifier>` is the betanumeric string.

---

## Technical Details

**Character Set:**  
Lowercase letters excluding vowels (`a`, `e`, `i`, `o`, `u`) and `l`; digits 0–9; optionally allow denser sets with some uppercase if needed.

**Uniqueness:**  
Identifiers are unique within each user’s namespace (email). Not globally unique—contextual uniqueness only.

**Statelessness:**  
System can operate statelessly if user provides last identifier; otherwise, store minimal state mapping `{email: last_identifier}` in memory or lightweight DB (e.g., SQLite).

**Check Digit:**  
Add check digit/character at end using simple algorithm (e.g., mod-N checksum).

---

## Whimsical Easter Egg: Slug/Lug Feature

**Background:**  
In reference to prior discussions about “slug/lug” and image generation attempts:

**Implementation:**

- If a user enters “slug” or “lug” as their email address OR requests an identifier containing “SLG”, trigger an easter egg:  
  - Display an animated SVG/cartoon image of a whimsical slug wearing sunglasses (“cool lug/slug”).  
  - Add playful tooltip text: "You found the secret slug/lug\!"  
  - Hide this feature unless specifically triggered by above input pattern.

---

## Stretch Goals / Nice-to-Haves

- Allow download/export of all generated identifiers for current session/user.  
- Add basic rate limiting per IP/email to prevent abuse.  
- Responsive design for mobile use.

---

## Out-of-Scope / Not Required For MVP

- User registration/login beyond entering email address.  
- Persistent storage beyond minimal mapping of emails → last issued identifier.  
- Advanced admin features or analytics dashboard.

---

## Example User Flow

1. User visits betanumerics.app  
2. Enters their email address (“[alice@example.com](mailto:alice@example.com)”) into form field  
3. Clicks “Generate Identifier”  
4. Receives output:  
   - Unique betanumeric string (e.g., "b7q")  
   - Full URL: [https://betanumerics.app/u/8f3d.../id/b7qz](https://betanumerics.app/u/8f3d.../id/b7qz)  
5. Can copy/share URL or generate another identifier  
6. If they enter "slug" or "lug" as their email, see animated slug/lug cartoon with secret message\!

---

## Tech Stack Suggestions

- Backend: Python (Flask/FastAPI), Node.js, or similar lightweight framework  
- Frontend: Simple HTML/CSS/JS; React optional but not required for MVP speed  
- Storage: In-memory dict or SQLite DB for mapping emails → last ID issued  
- Deployment: Replit/Cursor cloud deployment target