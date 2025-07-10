# Consilio Email Service Design

## Overview

Consilio's email interface transforms the CLI-based decision facilitation tool into an accessible email service. Users interact through natural email conversations, with each decision project getting its own subdomain (e.g., `bach-house.cons.il.io`).

## Core Email Architecture

### Email Address Structure

```
{perspective}@{project}.cons.il.io
{system-function}@{project}.cons.il.io
```

Examples:
- `eco-architect@bach-house.cons.il.io` - Interview specific perspective
- `group@bach-house.cons.il.io` - Group discussion
- `secretary@bach-house.cons.il.io` - Project management
- `new@cons.il.io` - Create new project

### System Accounts

1. **Project Creation**
   - `new@cons.il.io` - Initialize new decision project

2. **Project Management** 
   - `secretary@{project}.cons.il.io` - Status, summaries, help
   - `perspectives@{project}.cons.il.io` - List available advisors
   - `add-perspective@{project}.cons.il.io` - Add new perspective
   - `summary@{project}.cons.il.io` - Focused summaries
   - `export@{project}.cons.il.io` - Download project history
   - `pause@{project}.cons.il.io` - Temporarily pause emails

3. **Discussion Aliases**
   - `group@{project}.cons.il.io` - Group discussion
   - `all@{project}.cons.il.io` - Alias for group
   - `everyone@{project}.cons.il.io` - Alias for group

## Email Threading with Postmark

### Message ID Strategy

Use Postmark's MessageStream and Metadata features to maintain conversation threads:

```json
{
  "From": "eco-architect@bach-house.cons.il.io",
  "To": "user@example.com",
  "Subject": "Re: Sustainable design for staged construction",
  "MessageStream": "outbound",
  "Headers": [
    {
      "Name": "Message-ID",
      "Value": "<bach-house.eco-architect.r2.1234567890@cons.il.io>"
    },
    {
      "Name": "In-Reply-To", 
      "Value": "<user.bach-house.eco-architect.r1@example.com>"
    },
    {
      "Name": "References",
      "Value": "<bach-house.initial@cons.il.io> <user.bach-house.eco-architect.r1@example.com>"
    }
  ],
  "Metadata": {
    "project_id": "bach-house",
    "perspective_id": "eco-architect",
    "round": 2,
    "thread_type": "interview"
  }
}
```

### Threading Patterns

1. **Interview Threads**
   - Message-ID: `<{project}.{perspective}.r{round}.{timestamp}@cons.il.io>`
   - Maintains perspective context across exchanges

2. **Group Discussion Threads**
   - Message-ID: `<{project}.group.r{round}.{timestamp}@cons.il.io>`
   - All perspectives respond in single thread

3. **System Message Threads**
   - Message-ID: `<{project}.{system-function}.{timestamp}@cons.il.io>`
   - Status updates, summaries maintain their own threads

## Perspective Memory System

### Global Perspective Bank

Perspectives exist across projects with accumulated memory:

```json
{
  "perspective_id": "eco-architect",
  "name": "Eco-friendly Architect",
  "base_prompt": "You are an architect specializing in sustainable design...",
  "memories": [
    {
      "project_id": "bach-house",
      "key_insights": [
        "User has basic carpentry skills",
        "Prefers staged construction approach",
        "Budget conscious at $30k phase 1"
      ],
      "interaction_count": 3
    },
    {
      "project_id": "renovation-2024", 
      "key_insights": [
        "User values natural materials",
        "Interested in passive cooling"
      ],
      "interaction_count": 5
    }
  ],
  "expertise_tags": ["sustainable", "residential", "small-scale", "DIY-friendly"],
  "communication_style": "practical, encouraging, detail-oriented"
}
```

### Memory Integration

When responding, perspectives reference relevant past experiences:

```
From: eco-architect@tiny-house.cons.il.io
Subject: Re: Designing a minimalist space

I notice you're interested in small-scale living! This reminds me of other 
compact projects where staged construction worked well. 

[Draws on bach-house experience without explicitly mentioning other clients]

Based on what typically works for DIY builders, consider starting with...
```

### Perspective Evolution

1. **Cross-Project Learning**
   - Perspectives become more nuanced over time
   - Build domain expertise from multiple projects
   - Maintain appropriate confidentiality boundaries

2. **Specialization Emergence**
   - Track which perspectives users find most valuable
   - Suggest specialized variants (e.g., "eco-architect-tropical" for beach projects)

## Email Content Structure

### Footer Navigation

Every email includes contextual navigation:

```
---
📧 group@{project}.cons.il.io - Share with everyone
📧 {other-perspective}@{project}.cons.il.io - Talk to specific advisor
📧 secretary@{project}.cons.il.io - Project status
📧 perspectives@{project}.cons.il.io - See all advisors
```

### Smart Context Preservation

1. **Inline Quotations**
   - Previous responses prefixed with `> ` 
   - Maintains readability in any email client

2. **Metadata Headers**
   - `X-Consilio-Project: bach-house`
   - `X-Consilio-Round: 3`
   - `X-Consilio-Perspective: eco-architect`

3. **Reply Detection**
   - Parse email content to extract user's response
   - Handle various email client quote formats
   - Maintain context without duplication

## Implementation with Postmark

### Inbound Processing

```python
@app.route('/postmark/inbound', methods=['POST'])
def handle_inbound():
    message = request.json
    
    # Extract routing information
    to_address = message['To']
    perspective, project = parse_address(to_address)
    
    # Thread tracking
    message_id = message.get('MessageID')
    in_reply_to = extract_header(message, 'In-Reply-To')
    
    # Retrieve context
    thread = get_thread(project, perspective, in_reply_to)
    
    # Process based on address type
    if perspective in SYSTEM_ACCOUNTS:
        response = handle_system_request(perspective, project, message)
    else:
        response = handle_perspective_interview(perspective, project, message, thread)
    
    # Send response via Postmark
    send_email(response, thread_headers)
```

### Perspective Memory Integration

```python
def handle_perspective_interview(perspective_id, project_id, message, thread):
    # Load perspective with memories
    perspective = load_perspective(perspective_id)
    
    # Retrieve project-specific context
    project_memory = perspective.get_project_memory(project_id)
    
    # Include relevant cross-project insights (anonymized)
    relevant_insights = perspective.get_relevant_insights(message['Subject'])
    
    # Generate response
    response = generate_perspective_response(
        perspective=perspective,
        project_context=thread.context,
        project_memory=project_memory,
        relevant_insights=relevant_insights,
        user_message=message['TextBody']
    )
    
    # Update memories
    perspective.add_memory(project_id, extract_key_points(response))
    
    return response
```

## User Experience Flow

### 1. Project Initialization
- Email to `new@cons.il.io`
- Receive project subdomain and secretary intro
- Secretary provides initial clarifying questions

### 2. Perspective Discovery
- Email `perspectives@{project}.cons.il.io` for list
- See which perspectives are currently active
- Add new perspectives as needed

### 3. Interview Sessions
- Email specific perspective directly
- Maintain threaded conversation
- Perspective builds understanding over exchanges

### 4. Group Discussions
- Email `group@{project}.cons.il.io`
- All active perspectives contribute
- Structured multi-perspective response

### 5. Project Management
- Secretary provides status updates
- Export full history anytime
- Pause/resume as needed

## Privacy and Data Management

1. **Project Isolation**
   - Each project has unique subdomain
   - No cross-project data leakage
   - Clear project boundaries

2. **Perspective Memories**
   - Anonymized insights only
   - No specific client details shared
   - User can request memory deletion

3. **Export Control**
   - Users own all their data
   - Full export available anytime
   - Standard formats (MD, PDF, JSON)

## Future Enhancements

1. **Perspective Marketplace**
   - Users contribute specialized perspectives
   - Rate and review perspectives
   - Custom perspective creation

2. **Team Decisions**
   - Multiple users per project
   - Permission levels
   - Collaborative features

3. **Integration Options**
   - Slack/Teams connectors
   - API access
   - Webhook notifications

4. **Advanced Memory**
   - Perspective relationship mapping
   - Decision pattern recognition
   - Outcome tracking for advice quality