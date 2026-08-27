import feedparser
import os
from datetime import datetime

# Configuration
FEED_URL = "https://qubuhub.blogpost.com"  # Replace with your actual feed URL
README_PATH = "profile/README.md"
MAX_POSTS = 5

def fetch_recent_posts(feed_url, max_posts=5):
    """Fetch recent blog posts from RSS/Atom feed"""
    feed = feedparser.parse(feed_url)
    posts = []
    
    for entry in feed.entries[:max_posts]:
        posts.append({
            'title': entry.get('title', 'Untitled'),
            'link': entry.get('link', '#'),
            'published': entry.get('published', 'No date'),
        })
    
    return posts

def format_posts_markdown(posts):
    """Format posts as markdown list"""
    if not posts:
        return "No recent blog posts.\n"
    
    markdown = "## Recent Blog Posts\n\n"
    for post in posts:
        markdown += f"- [{post['title']}]({post['link']}) - {post['published']}\n"
    
    return markdown

def update_readme(feed_url, readme_path, max_posts=5):
    """Update README with recent blog posts"""
    
    # Fetch posts
    posts = fetch_recent_posts(feed_url, max_posts)
    posts_markdown = format_posts_markdown(posts)
    
    # Read existing README
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as f:
            content = f.read()
    else:
        content = "# Profile\n\n"
    
    # Replace or add blog posts section
    if "## Recent Blog Posts" in content:
        # Replace existing section
        start = content.find("## Recent Blog Posts")
        end = content.find("\n## ", start + 1)
        if end == -1:
            end = len(content)
        content = content[:start] + posts_markdown + content[end:]
    else:
        # Append new section
        content += "\n" + posts_markdown
    
    # Write updated README
    with open(readme_path, 'w') as f:
        f.write(content)
    
    print("README updated successfully!")

if __name__ == "__main__":
    update_readme(FEED_URL, README_PATH, MAX_POSTS)
