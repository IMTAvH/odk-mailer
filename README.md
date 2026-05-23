# odk-mailer
odk-mailer is a lightweight FastAPI microservice that listens to events from ODK Central (via central-webhook) and sends email notifications using aiosmtplib. It is designed to support automated alerts and integrations for public health surveillance and field data collection systems.


## `forms_registry.json` Configuration
File: `config/forms_registry.json`

Initialize it from the example:
```bash
cp config/forms_registry.example.json config/forms_registry.json
```

This file has two sections:
- `routes`: maps each form (`project_id` + `form_id`) to a `handler`.
- `projects`: project-level general settings (cc, name, etc.).

### Base Structure
```json
{
  "routes": [],
  "projects": []
}
```

### Supported Fields in `routes`
- `project_id` (required): ODK project ID.
- `form_id` (required): ODK form ID.
- `handler` (required): registered handler name.
- `project_name` (optional): display name used in templates/logs.
- `next_form_url` (optional): link inserted into preregistration/backup emails.
- `reminder_enabled` (optional, bool): enables/disables reminders for participants from this route.
- `reminder_url` (optional): URL used by reminders for this route.
- `email_optional` (optional, bool): if email is empty, it is not treated as a warning.
- `cc` (optional, string or list): CC recipients for this route.

### Supported Fields in `projects`
- `project_id` (required): project ID.
- `project_name` (optional): default project display name.
- `cc` (optional, string or list): default CC recipients for all emails in that project.

### Important Rules
- If `project_id`, `form_id`, or `handler` is missing in a route, that route is ignored.
- Final `cc` is combined as: `project.cc + route.cc`.
- A participant enters reminder flow only if their route stored `reminder_enabled=true` and `reminder_url`.
