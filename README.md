# SocialQueue 📱

> **Social Media Post Scheduler** - Schedule and post to multiple social media platforms (Twitter, LinkedIn, Mastodon) from one place. Perfect for content creators and marketers.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status: Active](https://img.shields.io/badge/status-active-success.svg)](https://github.com/yksanjo/SocialQueue)
[![GitHub stars](https://img.shields.io/github/stars/yksanjo/SocialQueue?style=social)](https://github.com/yksanjo/SocialQueue)

**SocialQueue** simplifies social media management by letting you schedule posts across multiple platforms from one tool. Save time, maintain consistency, and grow your audience with automated posting.

## Features

- 🐦 Twitter/X posting
- 💼 LinkedIn posting
- 🐘 Mastodon posting
- 📅 Schedule posts in advance
- 📊 Post analytics
- 🔄 Recurring posts
- 📝 Post templates

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file:

```env
# Twitter/X API
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_token_secret

# LinkedIn API
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret
LINKEDIN_ACCESS_TOKEN=your_access_token

# Mastodon
MASTODON_INSTANCE=https://mastodon.social
MASTODON_ACCESS_TOKEN=your_access_token
```

## Usage

### Schedule a Post

```bash
python scheduler.py --post "Hello world!" --platforms twitter,linkedin --schedule "2024-01-15 10:00"
```

### Post Immediately

```bash
python scheduler.py --post "Hello world!" --platforms twitter,linkedin --now
```

### List Scheduled Posts

```bash
python scheduler.py --list
```

### Cancel Scheduled Post

```bash
python scheduler.py --cancel post_id
```

## Supported Platforms

- Twitter/X
- LinkedIn
- Mastodon
- (More coming soon)

## License

MIT License


