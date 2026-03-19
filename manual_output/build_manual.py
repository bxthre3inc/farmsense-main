#!/usr/bin/env python3
"""
FarmSense Master Manual V2.1 HTML/PDF Builder
Splits comprehensive manual into 17 parts and generates:
- Individual HTML files with navigation
- Consolidated PDF via Playwright
"""

import re
import subprocess
from pathlib import Path

# Configuration
MANUAL_PATH = "/home/workspace/Bxthre3/the-farmsense-project/docs/FarmSense_Master_Manual_Comprehensive_V2.1.md"
OUTPUT_DIR = Path("/home/workspace/Bxthre3/the-farmsense-project/manual_output")
TEMPLATE_PATH = OUTPUT_DIR / "template.html"

# Part definitions with titles
PARTS = [
    ("I", "Executive Foundation", "Hydro-Economic Logic, MAD Framework, PMT Field Hub"),
    ("II", "Market Intelligence", "TAM/SAM/SOM, Competitive Moat, Federal Grants"),
    ("III", "Human Capital", "Leadership, Org Chart, Scientific Advisory Board"),
    ("IV", "Technical Core", "Tri-Layer Compute, SQL Schema, API Specifications"),
    ("V", "Hardware Ecosystem", "RSS/DHU/PMT/PFA, VFA/LRZN/LRZB, SFD Configs"),
    ("VI", "Interface Layer", "3D Farmer Dashboard, Regulatory Portal, ROI Analytics"),
    ("VII", "Hydrologic Oracle", "SPAC Thermodynamics, Cokriging Math, 40 Basins"),
    ("VIII", "Pilot Mission", "CSU SLV Specification, Timeline, Success Criteria"),
    ("IX", "Operations", "Seasonal Deployment, Sled Hospital, Maintenance"),
    ("X", "Infrastructure", "AWS EKS Architecture, GitOps, Disaster Recovery"),
    ("XI", "Cybersecurity", "Zero-Trust Architecture, eBPF Auditing, Lateral Prevention"),
    ("XII", "Water Court Ledger", "NREP Standard, Chain of Custody, Data Sovereignty"),
    ("XIII", "Global Standards", "GlobalG.A.P., Nitrogen Prevention, Carbon MRV"),
    ("XIV", "Financial Backbone", "10-Year Projections, CAPEX/OPEX, Exit Roadmap"),
    ("XV", "Federal Grant Registry", "USDA/NRCS, NSF/DOE, Gates Foundation"),
    ("XVI", "SLV Case Study", "2026 Pilot Results, Reflex Discovery, Legal Validation"),
    ("XVII", "Appendices", "BOM Catalog, Soil Tables, Basin Registry, Glossary"),
]

def read_manual():
    """Read the comprehensive manual."""
    with open(MANUAL_PATH, 'r') as f:
        return f.read()

def split_by_parts(content):
    """Split manual content by PART markers."""
    # Pattern to match PART headers
    pattern = r'(# PART [IVX]+:.*?)(?=# PART [IVX]+:|# APPENDICES|$)'
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    parts = []
    for i, match in enumerate(matches):
        part_content = match.group(1).strip()
        parts.append(part_content)
    
    # Also capture any remaining content (Appendices)
    if matches:
        last_end = matches[-1].end()
        remaining = content[last_end:].strip()
        if remaining:
            parts.append(remaining)
    
    return parts

def markdown_to_html(md_content):
    """Convert markdown to HTML using pandoc."""
    result = subprocess.run(
        ['pandoc', '-f', 'markdown', '-t', 'html', '--wrap=none'],
        input=md_content,
        capture_output=True,
        text=True
    )
    return result.stdout

def generate_html(part_num, part_content, part_info, prev_info, next_info):
    """Generate HTML for a single part."""
    roman, title, key_contents = part_info
    
    # Read template
    with open(TEMPLATE_PATH, 'r') as f:
        template = f.read()
    
    # Convert markdown to HTML
    html_content = markdown_to_html(part_content)
    
    # Replace template variables
    html = template.replace('{{title}}', f"Part {roman}: {title}")
    html = html.replace('{{content}}', html_content)
    html = html.replace('{{current_part}}', str(part_num))
    
    # Navigation
    if prev_info:
        prev_roman, prev_title, _ = prev_info
        html = html.replace('{{prev}}', f"part{part_num-1:02d}.html")
        html = html.replace('{{prev_title}}', f"Part {prev_roman}: {prev_title}")
        html = html.replace('{{prev_disabled}}', '')
    else:
        html = html.replace('{{prev}}', '#')
        html = html.replace('{{prev_title}}', 'None')
        html = html.replace('{{prev_disabled}}', 'opacity-50 pointer-events-none')
    
    if next_info:
        next_roman, next_title, _ = next_info
        html = html.replace('{{next}}', f"part{part_num+1:02d}.html")
        html = html.replace('{{next_title}}', f"Part {next_roman}: {next_title}")
        html = html.replace('{{next_disabled}}', '')
    else:
        html = html.replace('{{next}}', '#')
        html = html.replace('{{next_title}}', 'None')
        html = html.replace('{{next_disabled}}', 'opacity-50 pointer-events-none')
    
    # Active state for navigation
    for i in range(1, 18):
        placeholder = f'{{part{i:02d}_active}}'
        if i == part_num:
            html = html.replace(placeholder, 'active')
        else:
            html = html.replace(placeholder, '')
    
    return html

def generate_index_page():
    """Generate the index/navigation page."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FarmSense Master Manual V2.1 | Index</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>body { font-family: 'Inter', sans-serif; }</style>
</head>
<body class="bg-gradient-to-br from-slate-900 via-slate-800 to-emerald-900 min-h-screen">
    <div class="max-w-5xl mx-auto px-6 py-20">
        <!-- Header -->
        <div class="text-center mb-16">
            <div class="inline-flex items-center gap-2 px-4 py-2 bg-emerald-500/20 border border-emerald-500/30 rounded-full mb-6">
                <svg class="w-4 h-4 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
                <span class="text-emerald-400 font-bold text-xs uppercase tracking-widest">Comprehensive Technical Specification</span>
            </div>
            <h1 class="text-5xl md:text-6xl font-black text-white tracking-tight mb-4">FarmSense Master Manual</h1>
            <p class="text-xl text-slate-400 mb-2">V2.1 — The Deterministic Farming Operating System</p>
            <p class="text-slate-500">6,214 lines | 45,000+ words | CONFIDENTIAL</p>
        </div>

        <!-- Download Section -->
        <div class="bg-white/10 backdrop-blur border border-white/20 rounded-2xl p-8 mb-12">
            <div class="flex flex-col md:flex-row items-center justify-between gap-6">
                <div>
                    <h2 class="text-2xl font-bold text-white mb-2">Download Complete Manual</h2>
                    <p class="text-slate-400">Full comprehensive specification in PDF format</p>
                </div>
                <a href="FarmSense_Master_Manual_Comprehensive_V2.1.pdf" class="px-8 py-4 bg-emerald-500 hover:bg-emerald-600 text-white font-bold rounded-xl transition-all shadow-lg shadow-emerald-500/25 flex items-center gap-2">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                    </svg>
                    Download PDF (245KB)
                </a>
            </div>
        </div>

        <!-- Parts Grid -->
        <div class="grid gap-4">
"""
    
    for i, (roman, title, key_contents) in enumerate(PARTS, 1):
        html += f'''
            <a href="part{i:02d}.html" class="group bg-white/10 backdrop-blur border border-white/10 hover:border-emerald-500/30 rounded-xl p-6 transition-all hover:bg-white/15">
                <div class="flex items-start gap-5">
                    <div class="w-14 h-14 bg-emerald-500/20 rounded-xl flex items-center justify-center shrink-0 group-hover:bg-emerald-500/30 transition-colors">
                        <span class="text-xl font-black text-emerald-400">{roman}</span>
                    </div>
                    <div class="flex-1">
                        <h3 class="text-lg font-bold text-white group-hover:text-emerald-400 transition-colors mb-1">{title}</h3>
                        <p class="text-slate-400 text-sm">{key_contents}</p>
                    </div>
                    <svg class="w-6 h-6 text-slate-500 group-hover:text-emerald-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                    </svg>
                </div>
            </a>
'''
    
    html += """
        </div>

        <!-- Footer -->
        <div class="mt-16 pt-8 border-t border-white/10 text-center">
            <div class="flex items-center justify-center gap-3 mb-4">
                <div class="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center">
                    <svg class="w-5 h-5 text-slate-900" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M4 2a2 2 0 00-2 2v11a3 3 0 106 0V4a2 2 0 00-2-2H4zm1 14a1 1 0 100-2 1 1 0 000 2zm5-1.757l4.9-4.9a2 2 0 000-2.828L13.485 5.1a2 2 0 00-2.828 0L10 5.757v8.486zM16 18H9.071l6-6H16a2 2 0 012 2v2a2 2 0 01-2 2z" clip-rule="evenodd"></path>
                    </svg>
                </div>
                <span class="text-white font-bold">FarmSense™</span>
            </div>
            <p class="text-slate-600 text-sm">© 2026 Bxthre3 Inc. All rights reserved. | CONFIDENTIAL</p>
        </div>
    </div>
</body>
</html>"""
    
    return html

def main():
    """Main build function."""
    print("🌱 Building FarmSense Master Manual V2.1...")
    
    # Read manual
    print("📖 Reading manual...")
    content = read_manual()
    
    # Split by parts
    print("✂️ Splitting into 17 parts...")
    parts = split_by_parts(content)
    
    if len(parts) != 17:
        print(f"⚠️ Warning: Found {len(parts)} parts, expected 17")
    
    # Generate HTML for each part
    html_dir = OUTPUT_DIR / "html"
    print(f"🎨 Generating HTML pages in {html_dir}...")
    
    for i, part_content in enumerate(parts[:17], 1):
        prev_info = PARTS[i-2] if i > 1 else None
        next_info = PARTS[i] if i < 17 else None
        
        html = generate_html(i, part_content, PARTS[i-1], prev_info, next_info)
        
        output_path = html_dir / f"part{i:02d}.html"
        with open(output_path, 'w') as f:
            f.write(html)
        
        print(f"  ✅ Part {i:02d}: {PARTS[i-1][0]} - {PARTS[i-1][1]}")
    
    # Generate index page
    print("📑 Generating index page...")
    index_html = generate_index_page()
    with open(html_dir / "index.html", 'w') as f:
        f.write(index_html)
    
    print(f"\n✨ HTML build complete! Output: {html_dir}")
    print(f"   - index.html (navigation)")
    print(f"   - part01.html through part17.html")
    print(f"\n🎨 Next: Run PDF generation with Playwright")

if __name__ == "__main__":
    main()
