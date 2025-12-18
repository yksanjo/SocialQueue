#!/usr/bin/env python3
"""
Social Media Post Scheduler
Schedule and post to Twitter, LinkedIn, Mastodon
"""

import os
import sys
import argparse
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv
import schedule
import pytz

try:
    import tweepy
    TWITTER_AVAILABLE = True
except ImportError:
    TWITTER_AVAILABLE = False

try:
    from mastodon import Mastodon
    MASTODON_AVAILABLE = True
except ImportError:
    MASTODON_AVAILABLE = False

load_dotenv()

class SocialMediaScheduler:
    def __init__(self):
        self.posts_file = 'scheduled_posts.json'
        self.posts = self.load_posts()
        
        # Initialize platform clients
        self.twitter_client = None
        self.linkedin_client = None
        self.mastodon_client = None
        
        self.init_clients()
    
    def load_posts(self) -> Dict:
        """Load scheduled posts from file"""
        if os.path.exists(self.posts_file):
            with open(self.posts_file, 'r') as f:
                return json.load(f)
        return {'posts': []}
    
    def save_posts(self):
        """Save scheduled posts to file"""
        with open(self.posts_file, 'w') as f:
            json.dump(self.posts, f, indent=2)
    
    def init_clients(self):
        """Initialize social media API clients"""
        # Twitter
        if TWITTER_AVAILABLE:
            api_key = os.getenv('TWITTER_API_KEY')
            api_secret = os.getenv('TWITTER_API_SECRET')
            access_token = os.getenv('TWITTER_ACCESS_TOKEN')
            access_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            
            if all([api_key, api_secret, access_token, access_secret]):
                try:
                    auth = tweepy.OAuthHandler(api_key, api_secret)
                    auth.set_access_token(access_token, access_secret)
                    self.twitter_client = tweepy.API(auth, wait_on_rate_limit=True)
                except Exception as e:
                    print(f"⚠️  Twitter client error: {e}")
        
        # Mastodon
        if MASTODON_AVAILABLE:
            instance = os.getenv('MASTODON_INSTANCE')
            token = os.getenv('MASTODON_ACCESS_TOKEN')
            
            if instance and token:
                try:
                    self.mastodon_client = Mastodon(
                        access_token=token,
                        api_base_url=instance
                    )
                except Exception as e:
                    print(f"⚠️  Mastodon client error: {e}")
    
    def post_to_twitter(self, text: str) -> bool:
        """Post to Twitter/X"""
        if not self.twitter_client:
            print("⚠️  Twitter not configured")
            return False
        
        try:
            self.twitter_client.update_status(text)
            return True
        except Exception as e:
            print(f"❌ Twitter post error: {e}")
            return False
    
    def post_to_linkedin(self, text: str) -> bool:
        """Post to LinkedIn"""
        # LinkedIn API requires more complex setup
        # This is a simplified version
        print("⚠️  LinkedIn posting requires additional setup")
        return False
    
    def post_to_mastodon(self, text: str) -> bool:
        """Post to Mastodon"""
        if not self.mastodon_client:
            print("⚠️  Mastodon not configured")
            return False
        
        try:
            self.mastodon_client.toot(text)
            return True
        except Exception as e:
            print(f"❌ Mastodon post error: {e}")
            return False
    
    def post_to_platforms(self, text: str, platforms: List[str]) -> Dict[str, bool]:
        """Post to multiple platforms"""
        results = {}
        
        for platform in platforms:
            platform = platform.lower().strip()
            
            if platform == 'twitter' or platform == 'x':
                results['twitter'] = self.post_to_twitter(text)
            elif platform == 'linkedin':
                results['linkedin'] = self.post_to_linkedin(text)
            elif platform == 'mastodon':
                results['mastodon'] = self.post_to_mastodon(text)
            else:
                print(f"⚠️  Unknown platform: {platform}")
                results[platform] = False
        
        return results
    
    def schedule_post(self, text: str, platforms: List[str], schedule_time: datetime):
        """Schedule a post for later"""
        post_id = f"post_{int(time.time())}"
        
        post = {
            'id': post_id,
            'text': text,
            'platforms': platforms,
            'scheduled_time': schedule_time.isoformat(),
            'created': datetime.now().isoformat(),
            'posted': False
        }
        
        self.posts['posts'].append(post)
        self.save_posts()
        
        # Schedule the post
        schedule_time_str = schedule_time.strftime('%Y-%m-%d %H:%M:%S')
        schedule.every().day.at(schedule_time_str[11:]).do(
            self.execute_scheduled_post, post_id
        )
        
        print(f"✅ Post scheduled for {schedule_time_str}")
        print(f"   Post ID: {post_id}")
        print(f"   Platforms: {', '.join(platforms)}")
        
        return post_id
    
    def execute_scheduled_post(self, post_id: str):
        """Execute a scheduled post"""
        post = next((p for p in self.posts['posts'] if p['id'] == post_id), None)
        
        if not post or post['posted']:
            return
        
        print(f"📤 Executing scheduled post: {post_id}")
        
        results = self.post_to_platforms(post['text'], post['platforms'])
        
        # Update post status
        post['posted'] = True
        post['posted_at'] = datetime.now().isoformat()
        post['results'] = results
        
        self.save_posts()
        
        # Print results
        for platform, success in results.items():
            status = "✅" if success else "❌"
            print(f"   {status} {platform}")
    
    def list_posts(self):
        """List all scheduled posts"""
        posts = self.posts.get('posts', [])
        
        if not posts:
            print("No scheduled posts")
            return
        
        print("\n" + "="*80)
        print("SCHEDULED POSTS")
        print("="*80)
        
        for post in posts:
            scheduled_time = datetime.fromisoformat(post['scheduled_time'])
            status = "✅ Posted" if post.get('posted') else "⏰ Scheduled"
            
            print(f"\n[{post['id']}] {status}")
            print(f"Text: {post['text'][:50]}...")
            print(f"Platforms: {', '.join(post['platforms'])}")
            print(f"Scheduled: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def cancel_post(self, post_id: str):
        """Cancel a scheduled post"""
        posts = self.posts.get('posts', [])
        post = next((p for p in posts if p['id'] == post_id), None)
        
        if not post:
            print(f"❌ Post {post_id} not found")
            return
        
        if post.get('posted'):
            print(f"⚠️  Post {post_id} already posted")
            return
        
        self.posts['posts'] = [p for p in posts if p['id'] != post_id]
        self.save_posts()
        
        print(f"✅ Cancelled post: {post_id}")
    
    def check_scheduled_posts(self):
        """Check and execute due posts"""
        now = datetime.now()
        
        for post in self.posts.get('posts', []):
            if post.get('posted'):
                continue
            
            scheduled_time = datetime.fromisoformat(post['scheduled_time'])
            
            if now >= scheduled_time:
                self.execute_scheduled_post(post['id'])
    
    def run_continuous(self):
        """Run continuous scheduler"""
        print("🚀 Starting continuous post scheduler")
        
        schedule.every(1).minutes.do(self.check_scheduled_posts)
        
        while True:
            schedule.run_pending()
            time.sleep(60)


def main():
    parser = argparse.ArgumentParser(description='Social Media Post Scheduler')
    parser.add_argument('--post', help='Post text')
    parser.add_argument('--platforms', help='Comma-separated platforms (twitter,linkedin,mastodon)')
    parser.add_argument('--schedule', help='Schedule time (YYYY-MM-DD HH:MM)')
    parser.add_argument('--now', action='store_true', help='Post immediately')
    parser.add_argument('--list', action='store_true', help='List scheduled posts')
    parser.add_argument('--cancel', help='Cancel scheduled post by ID')
    parser.add_argument('--watch', action='store_true', help='Run continuous scheduler')
    
    args = parser.parse_args()
    
    try:
        scheduler = SocialMediaScheduler()
        
        if args.post and args.platforms:
            platforms = [p.strip() for p in args.platforms.split(',')]
            
            if args.now:
                # Post immediately
                print(f"📤 Posting to {', '.join(platforms)}...")
                results = scheduler.post_to_platforms(args.post, platforms)
                for platform, success in results.items():
                    status = "✅" if success else "❌"
                    print(f"   {status} {platform}")
            elif args.schedule:
                # Schedule post
                schedule_time = datetime.strptime(args.schedule, '%Y-%m-%d %H:%M')
                scheduler.schedule_post(args.post, platforms, schedule_time)
            else:
                print("❌ Specify --now or --schedule")
        elif args.list:
            scheduler.list_posts()
        elif args.cancel:
            scheduler.cancel_post(args.cancel)
        elif args.watch:
            scheduler.run_continuous()
        else:
            parser.print_help()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()


