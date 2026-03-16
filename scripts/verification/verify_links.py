# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

import os
import re
import sys

def verify_links(directory):
    files_to_check = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".md", ".html")):
                files_to_check.append(os.path.join(root, file))

    errors = []
    
    for filepath in files_to_check:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if filepath.endswith(".md"):
            # 1. Check relative links: [label](path)
            links = re.findall(r'\[.*?\]\((.*?)\)', content)
            for link in links:
                if link.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                    
                path_part = link.split("#")[0]
                if not path_part:
                    continue
                    
                link_path = os.path.normpath(os.path.join(os.path.dirname(filepath), path_part))
                if not os.path.exists(link_path):
                    errors.append(f"❌ {filepath}: Broken link to '{link}'")

            # 2. Check internal anchors: #section-name
            anchors = re.findall(r'\[.*?\]\(#(.*?)\)', content)
            for anchor in anchors:
                slug = anchor.lower().replace("-", " ")
                found = False
                for line in content.splitlines():
                    if line.startswith("#"):
                        header_text = line.lstrip("#").strip().lower()
                        if header_text.replace(" ", "-") == anchor or header_text == slug:
                            found = True
                            break
                if not found:
                    errors.append(f"⚠️ {filepath}: Potential broken internal anchor '#{anchor}'")
        
        elif filepath.endswith(".html"):
            # Check href links in HTML
            links = re.findall(r'href=["\'](.*?)["\']', content)
            for link in links:
                if link.startswith(("http://", "https://", "mailto:", "#", "javascript:")):
                    continue
                
                path_part = link.split("#")[0]
                if not path_part:
                    continue
                
                link_path = os.path.normpath(os.path.join(os.path.dirname(filepath), path_part))
                if not os.path.exists(link_path):
                    errors.append(f"❌ {filepath}: Broken HTML link to '{link}'")

    return errors

if __name__ == "__main__":
    if len(sys.argv) > 1:
        docs_dir = sys.argv[1]
    else:
        docs_dir = "docs/md"
        
    if not os.path.exists(docs_dir):
        print(f"Directory {docs_dir} not found.")
        sys.exit(1)
        
    print(f"Checking documentation integrity in {docs_dir}...")
    link_errors = verify_links(docs_dir)
    
    if link_errors:
        for err in link_errors:
            print(err)
        sys.exit(1)
    else:
        print(f"✅ No broken links detected in {docs_dir}.")
    
    sys.exit(0)
