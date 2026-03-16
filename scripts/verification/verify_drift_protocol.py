# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

import os
import sys

REQUIRED_MARKER = "MODULAR DAP (Drift Aversion Protocol)"
REQUIRED_MODULE_D = "Module: D-DAP (Documentation)"
REQUIRED_MODULE_E = "Module: E-DAP (Engineering)"
REQUIRED_FIELDS = ["Status:", "Last Audited:", "Drift Aversion: REQUIRED"]

def check_file(filepath, module_type="D-DAP"):
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            
        missing = []
        
        # Meta fields are only required for Documentation (D-DAP)
        if module_type == "D-DAP":
            for field in REQUIRED_FIELDS:
                if field not in content:
                    missing.append(field)
                
        if REQUIRED_MARKER not in content:
            missing.append("MODULAR DAP Header")
        
        target_module = REQUIRED_MODULE_D if module_type == "D-DAP" else REQUIRED_MODULE_E
        if target_module not in content:
            missing.append(f"DAP Module Marker ({target_module})")
            
        return missing
    except Exception as e:
        return [f"Read Error: {e}"]

def main():
    docs_dir = "docs"
    non_compliant = []
    
    # Check root files
    for root_file in ["README.md", "todo.md"]:
        if os.path.exists(root_file):
            missing = check_file(root_file)
            if missing:
                non_compliant.append((root_file, missing))
    
    # Check docs directory
    if os.path.exists(docs_dir):
        for root, dirs, files in os.walk(docs_dir):
            for file in files:
                if file.endswith(".md"):
                    filepath = os.path.join(root, file)
                    missing = check_file(filepath)
                    if missing:
                        non_compliant.append((filepath, missing))
    
    # Check codebase for E-DAP
    code_dirs = ["farmsense-code/backend", "farmsense-code/edge-compute", "scripts"]
    for d in code_dirs:
        if os.path.exists(d):
            for root, dirs, files in os.walk(d):
                for file in files:
                    if file.endswith(".py") or file.endswith(".sh"):
                        filepath = os.path.join(root, file)
                        # Skip the verifier itself to avoid circular confusion during dev
                        if "verify_drift_protocol.py" in filepath:
                            continue
                        missing = check_file(filepath, module_type="E-DAP")
                        if missing:
                            non_compliant.append((filepath, missing))

    if non_compliant:
        print("❌ DAP NON-COMPLIANCE DETECTED (Modular Protocol v2):")
        for path, missing in non_compliant:
            print(f"  - {path}: Missing {', '.join(missing)}")
        
    # E-DAP checks
    ext_violations = []
    for root, dirs, files in os.walk("."):
        if "node_modules" in root or ".git" in root or "ARCHIVE" in root:
            continue
        for file in files:
            if file.endswith(".bak") or file.endswith(".old") or ".py.bak" in file:
                ext_violations.append(os.path.join(root, file))
                
    if ext_violations:
        print("\\n❌ E-DAP INFRASTRUCTURE VIOLATIONS (Prohibited File Sprawl):")
        for v in ext_violations:
            print(f"  - {v}")
            
    if non_compliant or ext_violations:
        sys.exit(1)
    else:
        print("✅ ALL SYSTEMS COMPLIANT WITH D-DAP AND E-DAP PROTOCOLS.")
        sys.exit(0)

if __name__ == "__main__":
    main()