#!/usr/bin/env python3
"""
Generate consolidated PDF from HTML parts using Playwright
"""

import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

HTML_DIR = Path("/home/workspace/Bxthre3/the-farmsense-project/manual_output/html")
PDF_OUTPUT = Path("/home/workspace/Bxthre3/the-farmsense-project/manual_output/pdf/FarmSense_Master_Manual_Comprehensive_V2.1.pdf")

async def generate_pdf():
    """Generate consolidated PDF from all HTML parts."""
    print("🎨 Starting PDF generation with Playwright...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # Create a combined HTML file for PDF generation
        combined_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>FarmSense Master Manual V2.1</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        code, pre { font-family: 'JetBrains Mono', monospace; }
        h1 { font-size: 2.5rem; font-weight: 900; margin-bottom: 2rem; page-break-before: always; }
        h1:first-of-type { page-break-before: avoid; }
        h2 { font-size: 1.75rem; font-weight: 700; margin-top: 3rem; margin-bottom: 1rem; border-bottom: 3px solid #10b981; padding-bottom: 0.5rem; }
        h3 { font-size: 1.25rem; font-weight: 700; margin-top: 2rem; margin-bottom: 0.75rem; color: #059669; }
        h4 { font-size: 1.125rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.5rem; }
        p { line-height: 1.7; margin-bottom: 1rem; color: #4b5563; }
        ul, ol { margin-bottom: 1rem; padding-left: 2rem; }
        li { margin-bottom: 0.5rem; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 1.5rem; font-size: 0.875rem; }
        th { background-color: #f3f4f6; padding: 0.75rem; text-align: left; font-weight: 700; border: 1px solid #d1d5db; }
        td { padding: 0.75rem; border: 1px solid #d1d5db; }
        tr:nth-child(even) { background-color: #f9fafb; }
        code { background-color: #f3f4f6; padding: 0.25rem 0.5rem; border-radius: 0.25rem; color: #059669; font-size: 0.875rem; }
        pre { background-color: #111827; color: #e5e7eb; padding: 1rem; border-radius: 0.5rem; overflow-x: auto; margin-bottom: 1.5rem; font-size: 0.75rem; }
        blockquote { border-left: 4px solid #10b981; padding-left: 1rem; font-style: italic; color: #6b7280; margin: 1.5rem 0; }
        .cover { text-align: center; padding: 8rem 2rem; background: linear-gradient(135deg, #064e3b 0%, #065f46 50%, #059669 100%); color: white; page-break-after: always; }
        .cover h1 { font-size: 3.5rem; margin-bottom: 1rem; page-break-before: avoid; }
        .cover p { color: #d1fae5; font-size: 1.25rem; }
        .toc { page-break-after: always; }
        .toc h2 { border-bottom: 2px solid #10b981; }
        .toc table { font-size: 0.9rem; }
        .confidential { text-align: center; padding: 2rem; background: #fef3c7; border: 2px solid #f59e0b; margin: 2rem 0; }
        @page { size: A4; margin: 20mm; }
        @page :first { margin: 0; }
    </style>
</head>
<body class="bg-white">
"""
        
        # Add cover page
        combined_html += """
    <div class="cover">
        <div style="display: inline-flex; align-items: center; gap: 0.75rem; padding: 0.75rem 1.5rem; background: rgba(255,255,255,0.2); border-radius: 9999px; margin-bottom: 2rem;">
            <span style="width: 0.5rem; height: 0.5rem; background: #34d399; border-radius: 50%;"></span>
            <span style="font-size: 0.875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em;">Comprehensive Technical Specification</span>
        </div>
        <h1>FarmSense Master Manual</h1>
        <p style="font-size: 1.5rem; margin-bottom: 0.5rem;">V2.1 — The Deterministic Farming Operating System</p>
        <p style="font-size: 1rem; opacity: 0.8;">6,214 lines | 45,000+ words | 245KB</p>
        <div style="margin-top: 4rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.2);">
            <p style="font-size: 0.875rem;">Bxthre3 Inc.</p>
            <p style="font-size: 0.75rem; opacity: 0.6;">March 2026</p>
        </div>
    </div>
"""
        
        # Add TOC
        combined_html += """
    <div class="toc">
        <h2>Table of Contents</h2>
        <table>
            <tr><th>Part</th><th>Title</th><th>Key Contents</th></tr>
            <tr><td><strong>I</strong></td><td>Executive Foundation</td><td>Hydro-Economic Logic; MAD Framework; PMT Field Hub</td></tr>
            <tr><td><strong>II</strong></td><td>Market Intelligence</td><td>TAM/SAM/SOM Analysis; Competitive Moat; Federal Grants</td></tr>
            <tr><td><strong>III</strong></td><td>Human Capital</td><td>Leadership; Org Chart; Scientific Advisory Board</td></tr>
            <tr><td><strong>IV</strong></td><td>Technical Core</td><td>Tri-Layer Compute; SQL Schema; API Specifications</td></tr>
            <tr><td><strong>V</strong></td><td>Hardware Ecosystem</td><td>RSS/DHU/PMT/PFA; VFA/LRZN/LRZB; SFD Configs</td></tr>
            <tr><td><strong>VI</strong></td><td>Interface Layer</td><td>3D Farmer Dashboard; Regulatory Portal; ROI Analytics</td></tr>
            <tr><td><strong>VII</strong></td><td>Hydrologic Oracle</td><td>SPAC Thermodynamics; Cokriging Math; 40 Global Basins</td></tr>
            <tr><td><strong>VIII</strong></td><td>Pilot Mission</td><td>CSU SLV Specification; Timeline; Success Criteria</td></tr>
            <tr><td><strong>IX</strong></td><td>Operations</td><td>Seasonal Deployment; Sled Hospital; Maintenance</td></tr>
            <tr><td><strong>X</strong></td><td>Infrastructure</td><td>AWS EKS Architecture; GitOps; Disaster Recovery</td></tr>
            <tr><td><strong>XI</strong></td><td>Cybersecurity</td><td>Zero-Trust; eBPF Auditing; Lateral Movement Prevention</td></tr>
            <tr><td><strong>XII</strong></td><td>Water Court Ledger</td><td>NREP Standard; Chain of Custody; Data Sovereignty</td></tr>
            <tr><td><strong>XIII</strong></td><td>Global Standards</td><td>GlobalG.A.P.; Nitrogen Prevention; Carbon MRV</td></tr>
            <tr><td><strong>XIV</strong></td><td>Financial Backbone</td><td>10-Year Projections; CAPEX/OPEX; Exit Roadmap</td></tr>
            <tr><td><strong>XV</strong></td><td>Federal Grant Registry</td><td>USDA/NRCS; NSF/DOE; Gates Foundation</td></tr>
            <tr><td><strong>XVI</strong></td><td>SLV Case Study</td><td>2026 Pilot Results; Reflex Discovery; Legal Validation</td></tr>
            <tr><td><strong>XVII</strong></td><td>Appendices</td><td>BOM Catalog; Soil Tables; Basin Registry; Glossary</td></tr>
        </table>
        <div class="confidential">
            <p style="font-weight: 700; color: #b45309; margin-bottom: 0.5rem;">⚠️ CONFIDENTIAL</p>
            <p style="font-size: 0.875rem; color: #92400e;">This document contains proprietary and confidential information of Bxthre3 Inc. Distribution limited to cleared investors and partners.</p>
        </div>
    </div>
"""
        
        # Read and combine all part HTML files
        for i in range(1, 18):
            part_file = HTML_DIR / f"part{i:02d}.html"
            if part_file.exists():
                with open(part_file, 'r') as f:
                    content = f.read()
                    # Extract body content
                    body_start = content.find('<main class="flex-1')
                    body_end = content.find('</main>')
                    if body_start > 0 and body_end > 0:
                        body_content = content[body_start:body_end + 7]
                        # Clean up template variables
                        body_content = body_content.replace('{{prev_disabled}}', '')
                        body_content = body_content.replace('{{next_disabled}}', '')
                        body_content = body_content.replace('opacity-50 pointer-events-none', '')
                        combined_html += body_content
                        print(f"  ✅ Added Part {i:02d}")
        
        combined_html += """
</body>
</html>
"""
        
        # Write combined HTML
        combined_path = HTML_DIR / "combined_for_pdf.html"
        with open(combined_path, 'w') as f:
            f.write(combined_html)
        
        print(f"📄 Combined HTML written: {combined_path}")
        
        # Generate PDF
        print("🖨️ Generating PDF (this may take a moment)...")
        page = await browser.new_page()
        await page.goto(f"file://{combined_path}")
        await page.wait_for_timeout(3000)  # Wait for fonts to load
        
        await page.pdf(
            path=str(PDF_OUTPUT),
            format='A4',
            print_background=True,
            margin={'top': '20mm', 'right': '20mm', 'bottom': '20mm', 'left': '20mm'},
            display_header_footer=True,
            header_template='<div style="font-size: 9px; margin-left: 20px; color: #6b7280;">FarmSense Master Manual V2.1 | CONFIDENTIAL</div>',
            footer_template='<div style="font-size: 9px; margin: 0 auto; color: #6b7280;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>'
        )
        
        await browser.close()
        
        print(f"✅ PDF generated: {PDF_OUTPUT}")
        print(f"   Size: {PDF_OUTPUT.stat().st_size / 1024:.0f}KB")

if __name__ == "__main__":
    asyncio.run(generate_pdf())
