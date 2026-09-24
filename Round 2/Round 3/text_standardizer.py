import re

def normalize_platform_text(text):
    """
    Cleans raw social media text from X, Reddit, and Web APIs 
    to match the clean format expected by the Round 2 model.
    """
    if not isinstance(text, str):
        return ""
    
    # 1. Lowercase the text
    text = text.lower()
    
    # 2. Strip out HTML remnants (e.g., &amp;, <div>, <br>)
    text = re.sub(r"&amp;|&lt;|&gt;|<br\s*/?>|<div>|</div>", " ", text)
    
    # 3. Remove platform handles and links (e.g., @user, HTTP links)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    
    # 4. Strip out Reddit specific markers (e.g., /r/technology, r/programming)
    text = re.sub(r"/?r/\w+", "", text)
    
    # 5. Clean up extra whitespaces
    text = re.sub(r"\s+", " ", text).strip()
    
    return text

if __name__ == "__main__":
    # Example Usage:
    raw_reddit_post = "Check out /r/sysadmin! My server has a crazy memory leak anomaly &amp; dropping nodes! @user https://test.com"
    clean_text = normalize_platform_text(raw_reddit_post)
    print(clean_text)
    # Output: "check out ! my server has a crazy memory leak anomaly dropping nodes!"

