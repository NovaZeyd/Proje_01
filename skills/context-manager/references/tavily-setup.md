# Tavily Web Search Setup

## API Configuration

Add to `openclaw.json`:

```json
{
  "tools": {
    "web": {
      "search": {
        "enabled": true,
        "provider": "tavily",
        "apiKey": "tvly-...",
        "maxResults": 5,
        "timeoutSeconds": 30
      }
    }
  }
}
```

## Getting Tavily API Key

1. Go to: https://tavily.com
2. Sign up for free account
3. Generate API key
4. Add key to config

## Alternative: Keep Brave

Current working setup:
```json
{
  "tools": {
    "web": {
