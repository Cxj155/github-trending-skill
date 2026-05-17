import os
from datetime import datetime
from config import SAVE_DIR

def save_content_to_file(content, filename=None):
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    if not filename:
        now = datetime.now()
        filename = f"github_trending_{now.strftime('%Y%m%d_%H%M%S')}.txt"

    filepath = os.path.join(SAVE_DIR, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 已保存到: {filepath}")
        return filepath
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return None