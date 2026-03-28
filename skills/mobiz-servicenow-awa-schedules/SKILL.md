---
name: mobiz-servicenow-awa-schedules
description: >
  ServiceNow schedule management and AWA (Advanced Work Assignment) eligibility validation.
  Use this skill whenever the user asks about: fetching a user's schedule or working hours,
  adding time off or vacation to a schedule, updating or changing working hours, checking
  if someone is available during a time range, or diagnosing why a user is not receiving
  tickets through AWA routing. Why user is online/offline when they shouldn't be.
  Also triggers on: cmn_schedule, schedule span, schedule entry, time off, PTO,
  agent availability, AWA eligibility, why am I not getting tickets, agent presence,
  agent capacity, excluded from AWA, AWA group, working hours, check availability,
  schedule mismatch, wrong timezone in schedule, agent shows offline, shift hours,
  rotate schedule, split shift, schedule has no entries, working days, on-call hours.
  Always invoke this skill for any ServiceNow schedule or AWA question.
---

You are performing a ServiceNow schedule or AWA eligibility operation. All operations use the
ServiceNow REST Table API with Basic Auth or Bearer token.

**Execution method:** Use the `servicenow_table_api` MCP tool for all API calls below.
Pass the method (GET/POST/PATCH), table path, and query parameters as described in each
flow. If the MCP tool is unavailable, fall back to direct REST calls using the base URL
and auth headers below.

**Base URL:** `https://{instance}.service-now.com/api/now/table`
**Headers:** `Content-Type: application/json`, `Accept: application/json`
**Always include:** `sysparm_display_value=all` on every request — this returns each field in
both its raw `value` (UTC datetime, sys_id references) and its human-readable `display_value`,
which is essential for correct timezone handling and resolving reference fields.

---

## Determining What to Do

Match the user's request to one of these flows:

| User says... | Flow |
|---|---|
| "What is my/someone's schedule?", "Show me working hours" | A: Fetch Schedule |
| "Add time off", "vacation", "PTO", "block out days" | B: Add Time Off (write — requires admin check) |
| "Change working hours", "update schedule", "new start time" | C: Update Working Hours (write — requires admin check) |
| "Is [user] available?", "Are they working on [date]?" | D: Check Availability |
| "Why am I not getting tickets?", "AWA not routing", "ticket assignment issue" | E: AWA Eligibility Validation |

**Before starting any write operation (B or C):** if the user hasn't provided all required
information (target user, dates, new hours, etc.), ask for it before making any API calls.
This prevents half-completed operations if something is missing mid-flow.

---

## Step 1 — Resolve the User

Every operation starts by finding the target user's `sys_id` in ServiceNow. Try identifiers in this order:

**By Slack ID:**
```
GET /sys_user?sysparm_query=u_slack_id={slack_id}&sysparm_limit=10&sysparm_display_value=all
```

**By email:**
```
GET /sys_user?sysparm_query=email={email}&sysparm_limit=10&sysparm_display_value=all
```

**By name:**
```
GET /sys_user?sysparm_query=first_name={first}^last_name={last}&sysparm_limit=10&sysparm_display_value=all
```

If multiple results, prefer: (1) company domain email (e.g. `@mobizinc.com`), (2) `active=true`.

Key fields: `sys_id`, `name`, `email`, `schedule` (reference to `cmn_schedule` — extract `.value` for the schedule sys_id).

If `schedule` is empty/null → report "No schedule found" and stop (for schedule operations).

---

## Step 2 — Fetch Schedule Details

```
GET /cmn_schedule/{schedule_sys_id}?sysparm_display_value=all
```

Extract: `sys_id`, `name`, `time_zone` (e.g., `US/Central`, `Europe/Kiev`, `Asia/Karachi`).

Save `time_zone` — you'll need it for every datetime conversion.

---

## Step 3 — Fetch Schedule Entries (Spans)

```
GET /cmn_schedule_span?sysparm_query=schedule={schedule_sys_id}&sysparm_limit=100&sysparm_display_value=all
```

Key fields per span: `sys_id`, `name`, `user`, `start_date_time`, `end_date_time`, `type`, `show_as`,
`repeat_type`, `repeat_until`, `repeat_count`, `days_of_week`, `all_day`.

### Critical: Timezone Conversion for Reading

When you receive datetime values with `sysparm_display_value=all`, each field has:
- **`value`** — real UTC with `Z` suffix (e.g., `20260131T190000Z`) — USE THIS
- **`display_value`** — integration user's timezone — IGNORE THIS (it reflects whoever is
  authenticated to the API, not the schedule owner)

Always convert `value` from UTC to the schedule's `time_zone`:

```
UTC time + schedule timezone offset = local display time

Asia/Karachi (UTC+5):   20260131T190000Z → 7:00 PM UTC + 5h = 12:00 AM Karachi
Europe/Kiev (UTC+2):    20260115T070000Z → 7:00 AM UTC + 2h = 9:00 AM Kiev
US/Central (UTC-6):     20260115T150000Z → 3:00 PM UTC - 6h = 9:00 AM Central
```

Common offsets: `US/Central` = UTC-6 (winter)/-5 (summer), `US/Eastern` = UTC-5/-4,
`Europe/Kiev` = UTC+2/+3, `Europe/Rome` = UTC+1/+2, `Asia/Karachi` = UTC+5 (no DST).

### Filter Spans

Skip entries that are:
1. Repeating entries where `repeat_until` is in the past
2. Time-off/busy entries (`type=exclude` or `show_as=time_off|busy`) where `end_date_time` is in the past

### Days of Week Mapping

`1`=Mon, `2`=Tue, `3`=Wed, `4`=Thu, `5`=Fri, `6`=Sat, `7`=Sun.
`days_of_week=1,2,3,4,5` → display as "Mon–Fri".

### Empty Schedule Check

If the query returns zero spans, the schedule record exists but has no entries configured.
Report: *"Schedule '{schedule_name}' exists but has no entries. Contact your ServiceNow
admin to add working hours."* — then stop. This is a common misconfiguration where someone
creates the schedule record but never populates it with spans.

---

## Authorization Check (REQUIRED Before ANY Write)

Before adding time off or updating working hours, verify the **requesting user** (who issued
the command, not the target user) has the `admin` role in ServiceNow.

**1. Find requesting user by their Slack ID:**
```
GET /sys_user?sysparm_query=u_slack_id={requesting_slack_id}&sysparm_limit=1&sysparm_display_value=all
```

**2. Check admin role:**
```
GET /sys_user_has_role?sysparm_query=user={requesting_user_sys_id}^role.name=admin&sysparm_limit=1&sysparm_display_value=all
```

- Record exists → admin confirmed → proceed
- Empty result → stop and respond: *"You don't have admin permissions to modify schedules. Please ask an admin to make this change."*

Run this check fresh on every write request — never reuse a cached result from earlier in the
conversation, because roles can be revoked between requests and a stale check would be a
security gap. Read-only operations (fetch, availability, AWA) skip this check.

---

## Flow A: Fetch Schedule

Run Steps 1–3, then generate a readable summary grouped by type:

- **Working hours**: "Works 9:00 AM – 5:00 PM Mon–Fri" (remember to convert UTC to schedule TZ)
- **Time off**: "Time Off: Feb 10–14, 2026 (Vacation)" (sort chronologically, skip past entries)

Present using the appropriate format (see Presentation section below).

---

## ⚠️ Mixed Timezone Warning (Read Before ANY Write)

A known production issue arises when **working days are defined in one timezone** but
**working hours are defined in a different timezone**. This creates a silent mismatch that
ServiceNow will accept without error, but results in the agent appearing offline at the
wrong times.

### Real-World Example (Junaid's Case)

HR configured the schedule thinking in PST (LA), but stated hours in PKT (Karachi, UTC+13 from PST):

| HR intent (PST days) | Stored hours (PKT) | Actual ServiceNow entry |
|---|---|---|
| Saturday 08:00–17:00 PST | 21:00 PKT – 06:00 PKT | Sat 21:00 → **Sunday** 06:00 PKT |
| Sunday 08:00–17:00 PST | 21:00 PKT – 06:00 PKT | Sun 21:00 → **Monday** 06:00 PKT |
| Monday 11:00–17:00 PST | 00:00 PKT – 06:00 PKT | **Tuesday** 00:00–06:00 PKT |

Result: On Thursday at 00:00 PKT, the schedule showed the agent as **offline** — because no
entry covered Thursday, even though the HR team believed they had configured a Thursday shift.
The root cause was days set by PST but hours set by PKT, causing a one-day slip in the schedule.

### Mandatory Clarification Before Any Write (Flows B & C)

**Before creating or modifying any schedule entry, always ask:**

> "To avoid a timezone mismatch, please confirm:
> 1. **What timezone are the working days based on?** (e.g., the timezone the HR team or manager thinks in when they say 'Monday')
> 2. **What timezone are the working hours based on?** (e.g., the timezone the agent actually works in when they say '9 AM')"

If both answers are the same timezone → proceed normally using that timezone.

If they **differ** (e.g., days in PST, hours in PKT):
1. Convert the hours to the days' timezone first to find the true local start/end
2. Then identify which calendar days in the schedule timezone those hours fall on
3. A shift crossing midnight will span **two** days — create an entry that covers both

### Midnight-Crossing Shifts

When a shift in the agent's timezone crosses midnight (e.g., 21:00–06:00 PKT), it spans two
calendar days. ServiceNow schedule spans cannot automatically handle this — you must account
for the day boundary manually when setting `days_of_week`.

Example — shift is Sat 21:00 to Sun 06:00 PKT:
- The entry starts on Saturday and ends on Sunday
- `days_of_week` must include **both** `6` (Sat) and `7` (Sun)
- `start_date_time` uses the Saturday date, `end_date_time` uses the Sunday date
- Or split into two entries if the hours differ per day

---

## Flow B: Add Time Off

> Requires admin check first. Confirm the target user, date range, and label with the requester before making any changes.
> **Also ask the mandatory timezone clarification** (see ⚠️ Mixed Timezone Warning above) if the user's schedule timezone may differ from the timezone the requester is thinking in.

After resolving the user and fetching their schedule (for timezone), POST a new span:

```
POST /cmn_schedule_span?sysparm_display_value=all
{
  "name": "{user_name} - Time Off",
  "schedule": "{schedule_sys_id}",
  "user": "{user_sys_id}",
  "type": "exclude",
  "show_as": "time_off",
  "start_date_time": "{start_utc}",
  "end_date_time": "{end_utc}",
  "all_day": true,
  "repeat_type": "does_not_repeat",
  "repeat_count": 1
}
```

### Timezone Conversion for Writing

ServiceNow stores times in UTC. Convert the user's requested local time to UTC before sending.

**Always include the `Z` suffix** when writing datetime values. Without `Z`, ServiceNow treats the value as local time (not UTC), which will store the wrong time silently.

Format: `YYYYMMDDTHHmmssZ`

```
local time − UTC offset = UTC to send (with Z)

9:00 AM Asia/Karachi (UTC+5):  9:00 - 5h = 04:00 UTC → 20260115T040000Z
9:00 AM Europe/Kiev (UTC+2):   9:00 - 2h = 07:00 UTC → 20260115T070000Z
9:00 AM Europe/Rome (UTC+1):   9:00 - 1h = 08:00 UTC → 20260115T080000Z
```

For all-day: use `T000000Z` to `T235959Z` in UTC (adjust for timezone if "all day" is in user's local time).

**Validation rules (enforced by ServiceNow):**
- `repeat_count` must be > 0
- `end_date_time` must be after `start_date_time`
- Time-off entries cannot overlap existing time-off

---

## Flow C: Update Working Hours

> Requires admin check first. Confirm the target user, new hours, days, and effective date with the requester before making any changes.
> **Also ask the mandatory timezone clarification** (see ⚠️ Mixed Timezone Warning above) — confirm that the days and hours provided are in the same timezone before proceeding.

This is a two-step operation that preserves schedule history — never delete the old span, because
it serves as an audit trail of when working hours changed and why.

**Step 1: Find the active working hours span(s)**
From Step 3 results, find spans where `type=work` and `repeat_type` is not `does_not_repeat`:
```
GET /cmn_schedule_span?sysparm_query=schedule={schedule_sys_id}^type=work&sysparm_limit=10&sysparm_display_value=all
```

### Handling Multiple Work Spans

Schedules often have more than one active work span — for example, different hours on
different days, or split shifts. When Step 1 returns multiple `type=work` spans:

1. Present all active spans to the user with their days and hours
2. Ask which span(s) to modify — or whether to replace all of them
3. Apply the end-old / create-new pattern (Steps 2–3 below) to each selected span individually

Never silently pick the first span — modifying the wrong one will break the schedule.

**Step 2: End the old span** — set `repeat_until` to the day before the effective date:
```
PATCH /cmn_schedule_span/{original_span_sys_id}?sysparm_display_value=all
{ "repeat_until": "{YYYYMMDD_day_before_effective}" }
```
Example: effective Feb 1 → set `repeat_until` to `20260131`.

**Step 3: Create new span** starting on the effective date, copying unchanged fields from the original:
```
POST /cmn_schedule_span?sysparm_display_value=all
{
  "name":             "{original_name}",
  "schedule":         "{schedule_sys_id}",
  "user":             "{user_sys_id}",
  "type":             "{copy from original}",
  "show_as":          "{copy from original}",
  "start_date_time":  "{effective_date}T{new_start_utc}Z",
  "end_date_time":    "{effective_date}T{new_end_utc}Z",
  "repeat_type":      "{new or copy from original}",
  "repeat_count":     "{copy or default 1}",
  "days_of_week":     "{new or copy from original}",
  "all_day":          false,
  "repeat_until":     "20400101"
}
```

`repeat_until: "20400101"` is a far-future sentinel meaning "repeats indefinitely" — it ensures
the new schedule entry stays active long-term without needing to set a real end date.

Convert desired local hours to UTC with `Z` suffix before sending (see timezone conversion in Flow B).

### Choosing repeat_type and days_of_week

Use the lowest-complexity preset that fits. If no preset matches, use `specific`:

| Days needed | repeat_type | days_of_week |
|---|---|---|
| Mon–Fri | `weekdays` | not required |
| Sat–Sun | `weekends` | not required |
| Mon, Wed, Fri | `weekMWF` | not required |
| Tue, Thu | `weekTT` | not required |
| Every day | `daily` | not required |
| Any other combination | `specific` | comma-separated: `1,2,3,6,7` |

**Days of week values:** `1`=Mon, `2`=Tue, `3`=Wed, `4`=Thu, `5`=Fri, `6`=Sat, `7`=Sun.
Format is comma-separated (e.g. `1,2,3,6,7` for Mon+Tue+Wed+Sat+Sun).

Example — set Sat, Sun, Mon, Tue, Wed, 11 AM–7 PM Europe/Rome (UTC+1):
```json
{
  "start_date_time": "20140101T100000Z",
  "end_date_time":   "20140101T180000Z",
  "repeat_type":     "specific",
  "days_of_week":    "1,2,3,6,7"
}
```

---

## Flow D: Check Availability

Run Steps 1–3. If the user hasn't specified a timezone for their requested time range, assume
the schedule's `time_zone`. Convert the requested start and end to UTC before comparing.

For each span where `show_as=time_off` or `show_as=busy`, check overlap:

```
requested_start < entry_end  AND  requested_end > entry_start
```

**Report:**
- **Available**: "No conflicts found — {user_name} appears to be available from {start} to {end} ({time_zone})."
- **Unavailable**: List each conflicting span with its name and dates/times converted to the schedule's timezone.

---

## Flow E: AWA Eligibility Validation

Diagnose why a user isn't receiving tickets. Run **all 6 checks** and collect every blocker
found — don't stop at the first one. Users often have multiple issues simultaneously, and
reporting only one leads to repeated troubleshooting rounds.

**1. Excluded from AWA assignment group (blocks everything)**
```
GET /sys_user_grmember?sysparm_query=user={user_sys_id}^group.name=Excluded from AWA assignment&sysparm_limit=1
```
Record exists → **BLOCKED**: "User is in the 'Excluded from AWA assignment' group."

**2. AWA group membership**
```
GET /sys_user_grmember?sysparm_query=user={user_sys_id}
```
Collect all group sys_ids, then:
```
GET /awa_group_queue_priority?sysparm_query=groupIN{comma_separated_group_sys_ids}
```
No records → **BLOCKED**: "User is not in any AWA-enabled group."

**3. Agent presence**
```
GET /awa_agent_presence_capacity?sysparm_query=ap_agent={user_sys_id}
```
`aca_available=false` → **BLOCKED**: "Agent is offline — AWA only assigns to online agents."

**4. Channel capacity**
From the same record: if `ac_workload >= ac_applied_max_capacity` → **BLOCKED**: "Channel at max capacity."

**5. Universal capacity**
If `uc_universal_workload` exceeds limits → **BLOCKED**: "Universal workload limit reached."

**6. Schedule / working hours**
Use Flow A to check if current time falls within the user's scheduled working hours.
Outside working hours → **BLOCKED**: "User is currently outside their scheduled working hours."

**Present results as:**
- **Blockers found ({count}):** list each with its check number, description, and recommended fix
- **Checks passed ({count}):** list briefly for confirmation

If all 6 checks pass → AWA should be routing — escalate for further investigation.

---

## Correcting Write Mistakes

**Wrong time-off entry (Flow B):** PATCH the span to fix dates/times, or DELETE it if
created in error:
```
DELETE /cmn_schedule_span/{span_sys_id}
```
Deletion is safe for time-off entries — they have no audit trail dependencies.

**Wrong working hours (Flow C):** Do NOT delete either span. Instead:
1. PATCH the incorrectly created new span's `repeat_until` to yesterday (deactivates it)
2. PATCH the original span's `repeat_until` back to `20400101` (reactivates it)
3. Re-run Flow C with the correct values

This preserves the full history of changes while correcting the error.

---

## Presentation

Always display times in the schedule's `time_zone` (never the integration user's timezone).
Render empty values as `—`. Sort time-off entries chronologically. Skip past/expired entries.

### Default format (markdown)

Use this when responding in Cowork, chat, API, or any non-Slack context:

```
**{user_name}'s Schedule**

| Field    | Value          |
|----------|----------------|
| Schedule | {schedule_name}|
| Timezone | {time_zone}    |

**Working Hours**

| Field   | Value                             |
|---------|-----------------------------------|
| Days    | {days}                            |
| Hours   | {start} – {end} ({time_zone})     |
| Repeats | {repeat_type} until {repeat_until} |

**Upcoming Time Off**
- {name} — {start_date} to {end_date}
```

If no upcoming time off: "No upcoming time off scheduled."

### Slack format (Block Kit)

When responding via Slack, use Block Kit with `mrkdwn` sections. Use code blocks for
aligned key-value pairs in threads, and `fields` layout for channel posts:

```json
{
  "blocks": [
    { "type": "section", "text": { "type": "mrkdwn", "text": "*{user_name}'s Schedule*" } },
    { "type": "section", "fields": [
        { "type": "mrkdwn", "text": "*Schedule*\n{schedule_name}" },
        { "type": "mrkdwn", "text": "*Timezone*\n{time_zone}" }
    ]},
    { "type": "section", "text": { "type": "mrkdwn", "text": "*Working Hours*" } },
    { "type": "section", "fields": [
        { "type": "mrkdwn", "text": "*Days*\n{days}" },
        { "type": "mrkdwn", "text": "*Hours*\n{start} – {end} ({time_zone})" }
    ]},
    { "type": "section", "text": { "type": "mrkdwn", "text": "*Upcoming Time Off*" } },
    { "type": "section", "text": { "type": "mrkdwn", "text": "- {name} — {start_date} to {end_date}" } }
  ]
}
```

---

## Error Handling

| Situation | Response |
|---|---|
| User not found | "No user found matching that identifier — try email, Slack ID, or full name." |
| No schedule on user | "This user has no schedule assigned in ServiceNow." |
| Schedule has no entries | "Schedule exists but has no entries configured — contact your ServiceNow admin." |
| HTTP 403 on write | Integration user needs `schedule_admin` or `itil_admin` role. |
| Business Rule abort | Check: `repeat_count > 0`, end after start, no overlapping time-off. |
| No repeating work entry | "No active weekly schedule found — the user may need a base schedule set up." |

---

## Server Time

To get the current ServiceNow server time, make any lightweight GET request and read the `Date`
response header — it contains the server's current UTC time. For example:
```
GET /sys_properties?sysparm_query=name=glide.sys.date_format&sysparm_limit=1&sysparm_fields=sys_updated_on
```
Then read the `Date` header from the HTTP response (not the body).
