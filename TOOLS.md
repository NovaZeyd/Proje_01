# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### Context Limits & APIs
**Mevcut:**
- NVIDIA Kimi K2.5: 262k context (BEDAVA) - Primary
- Groq Llama 3.3 70B: 128k context (BEDAVA) - Fallback

**Daha Büyük İhtiyaç Olursa:**
- Google Gemini: 2M context
- Grok: 1M context  
- Anthropic Claude: 200k context

**Günlük Kontrol:** Cron job her gün 09:00'da çalışır (%80+ uyarı)

---

Add whatever helps you do your job. This is your cheat sheet.
