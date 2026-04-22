<!-- Last updated: 2026-04-21 -->
<!-- Last change: Initial PRD creation -->

# Gamer Rater - Product Requirements Document

## Problem Statement

Board and card game enthusiasts have no centralized place to track games they have played, add games to a shared library, and read or leave reviews. Gamer Rater solves this by giving authenticated users a shared game catalog they can contribute to, rate, and review.

## Target Users

- Board game and card game players who want to track and review games they have played
- Admins who manage the category taxonomy used to classify games

## Core Requirements

### Authentication
- Users can register for an account with a username, first and last name, and password
- Passwords are validated against strength rules on registration
- Users log in and receive a token used to authenticate all subsequent requests
- All game, rating, and picture endpoints require authentication

### Games
- Any authenticated user can add a game to the shared catalog
- Game titles must be unique across the system -- no two games can share the same title
- Games include: title, description, designer, year released, number of players, time to play, age recommendation, and categories
- Each game response includes an `is_owner` boolean indicating whether the requesting user added that game
- Games can be assigned one or more categories
- Any authenticated user can edit or delete any game (for now)

### Categories
- Categories are predefined labels used to classify games (e.g. Strategy, Cooperative, Deck Building)
- Only admin users (`is_staff = True`) can create, update, or delete categories
- Any authenticated user can view the category list
- Admin status is granted through the Django admin panel only -- it cannot be set during registration

### Ratings and Reviews
- Any authenticated user can leave one rating and review per game
- Ratings apply to any game in the system, including games the user added themselves
- A user can edit or delete their own rating

### Game Pictures
- Any authenticated user can upload a picture URL for any game
- Pictures are stored as URLs in the database
- Pictures can be filtered by game via query parameter: `GET /gamepictures?game_id=1`
- A user can delete their own picture uploads

### Player Profiles
- Each user has an extended profile (`Player`) that adds a `bio` field
- The `/me` endpoint returns the authenticated user's data including `is_staff`

## Technical Stack

### Stack Decisions

| Layer | Choice | Rationale |
|---|---|---|
| Backend | Django + Django REST Framework | Bootcamp requirement; provides auth, ORM, serialization, and routing out of the box |
| Authentication | Token-based (DRF authtoken) | Simple, stateless, well-suited for a separate frontend client |
| Database | SQLite (development) | Lightweight, zero-config, appropriate for a bootcamp project |
| Frontend | React | Bootcamp requirement |
| API style | REST | Standard, well-understood, matches DRF conventions |

## Scope

### In Scope (v1)

- User registration and login
- Full CRUD for games with category assignment
- Game ratings and reviews (one per user per game)
- Game picture URL storage and retrieval
- Category management (admin-only writes)
- Player bio profile
- Admin panel access via Django admin
- `is_owner` and `is_staff` flags returned on relevant responses

### Out of Scope (future)

- "Games I own" -- a way for a user to mark that they physically own a game
- "Games I've played" -- tracking play history separate from leaving a review
- Static file serving for uploaded images (currently URL storage only)
- Image upload directly to the server (planned, not yet built)
- Pagination on list endpoints
- Search and filtering beyond game-level picture filtering
- Rating aggregates (e.g. average rating per game)

## Success Criteria

- A user can register, log in, add a game with categories, leave a review, and upload a picture URL entirely through the client
- Admin users can manage categories; non-admin users receive a 403 on write attempts
- No duplicate game titles exist in the system
- All endpoints return appropriate status codes for success, not found, and forbidden cases

## Learning Goals

- **Image handling in Django:** understand how to serve static files and accept image uploads, and decide when to store a URL vs. a file
- **Pagination:** learn how DRF's pagination classes work and when to apply them to list endpoints
- *(More to be added as new topics come up during development)*
