# Browser Control Patterns

## n8n Workflow Management

### Connect to n8n
```python
# Check if n8n is running
browser action:navigate targetUrl:"http://localhost:5678"
browser action:snapshot
```

### Common Actions
- `browser action:navigate` - Go to URL
- `browser action:snapshot` - Get page state
- `browser action:type` - Fill forms
- `browser action:click` - Click elements
- `browser action:screenshot` - Capture screen

## Web UI Testing

### Pattern: Login + Action
1. Navigate to login page
2. Fill credentials (type)
3. Submit (click or press Enter)
4. Wait for redirect
5. Perform action
6. Screenshot result

### Pattern: Form Submission
1. Snapshot to see form
2. Fill required fields by ref
3. Click submit
4. Wait for success indicator
5. Screenshot confirmation

## Monitoring

- Set up periodic screenshots
- Compare states over time
- Alert on changes
