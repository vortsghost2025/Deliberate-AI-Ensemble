"""
Operation Nightingale - Interactive Symptom Checker
WE Framework Medical Data Analysis POC

Interactive interface for symptom selection and multi-AI analysis.
Constitutional Alignment: Layer 0 (Gift) - Free healthcare assistance
"""

import csv
import json
from datetime import datetime

import safe_analysis

def extract_all_symptoms(diseases):
    """Extract unique symptoms from dataset"""
    symptoms = set()
    for disease, symptom_sets in diseases.items():
        for symptom_list in symptom_sets:
            for symptom in symptom_list:
                if symptom.strip():
                    symptoms.add(symptom.strip())
    return sorted(symptoms)

def display_symptom_checklist(symptoms):
    """Display numbered symptom checklist"""
    print("\n" + "="*70)
    print("  SYMPTOM CHECKLIST - Select All That Apply")
    print("="*70 + "\n")
    
    # Display in columns for readability
    col_width = 35
    for i in range(0, len(symptoms), 2):
        left = f"{i+1:3d}. {symptoms[i]}"
        if i+1 < len(symptoms):
            right = f"{i+2:3d}. {symptoms[i+1]}"
            print(f"{left:<{col_width}} {right}")
        else:
            print(left)
    
    print("\n" + "="*70)

def get_user_symptom_selection(symptoms):
    """Get symptom selection from user"""
    print("\nEnter symptom numbers separated by spaces (or 'q' to quit)")
    print("Example: 1 15 23 67")
    print("\nYour selection: ", end="")
    
    user_input = input().strip()
    
    if user_input.lower() == 'q':
        return None
    
    try:
        indices = [int(x.strip()) - 1 for x in user_input.split()]
        selected = [symptoms[i] for i in indices if 0 <= i < len(symptoms)]
        return selected
    except (ValueError, IndexError):
        print("\n⚠️  Invalid input. Please enter valid numbers.")
        return get_user_symptom_selection(symptoms)

def save_markdown_report(report, filename="analysis_report.md"):
    """Generate beautiful markdown report"""
    md = []
    
    md.append("# Medical Symptom Analysis Report")
    md.append("## Operation Nightingale - WE Framework POC\n")
    
    md.append(f"**Analysis Date:** {report['timestamp']}")
    md.append(f"**Input Symptoms:** {', '.join(report['input_symptoms'])}\n")
    
    md.append("---\n")
    
    md.append("## 📊 Analysis Summary\n")
    analysis = report['analysis']
    md.append(f"- **Total Matches:** {analysis['total_matches']}")
    md.append(f"- **High Confidence (≥70%):** {len(analysis['high_confidence'])}")
    md.append(f"- **Medium Confidence (40-70%):** {len(analysis['medium_confidence'])}")
    md.append(f"- **Low Confidence (<40%):** {len(analysis['low_confidence'])}\n")
    
    md.append("---\n")
    
    md.append("## 🏥 Top Diagnostic Matches\n")
    
    for i, diag in enumerate(report['top_diagnoses'], 1):
        md.append(f"### {i}. {diag['disease']} ({diag['confidence']})\n")
        
        md.append("**Matching Symptoms:**")
        for symptom in diag['matching_symptoms']:
            md.append(f"- {symptom}")
        md.append("")
        
        md.append(f"**Description:** {diag['description']}\n")
        
        if diag['precautions']:
            md.append("**Recommended Precautions:**")
            for precaution in diag['precautions']:
                md.append(f"- {precaution}")
            md.append("")
        
        md.append("---\n")
    
    md.append("## ⚠️ Disclaimer\n")
    md.append("This is a proof-of-concept analysis tool developed using the WE Framework ")
    md.append("for multi-AI collaborative decision-making. This tool is intended for ")
    md.append("educational and research purposes only.\n")
    md.append("**Always consult qualified medical professionals for diagnosis and treatment.**\n")
    
    md.append("---\n")
    md.append("**Framework:** WE (Deliberate Ensemble)")
    md.append("**Repository:** https://github.com/vortsghost2025/deliberate-ensemble")
    md.append("**Layer 0 Alignment:** The Gift - Free, replicable, for all")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))
    
    return filename

def interactive_session():
    """Main interactive symptom checking session"""
    print("\n🚀 Loading Operation Nightingale...")
    data = safe_analysis.load_synthetic_data()
    diseases = data["diseases"]
    descriptions = data["descriptions"]
    precautions = data["precautions"]
    
    print(f"✅ Loaded {len(diseases)} diseases")
    
    symptoms = extract_all_symptoms(diseases)
    print(f"✅ Available symptoms: {len(symptoms)}")
    
    while True:
        display_symptom_checklist(symptoms)
        
        selected = get_user_symptom_selection(symptoms)
        
        if selected is None:
            print("\n👋 Exiting Operation Nightingale. Stay healthy!")
            break
        
        if not selected:
            print("\n⚠️  No symptoms selected. Try again.")
            continue
        
        print(f"\n🔍 Analyzing {len(selected)} symptoms...")
        print(f"   Selected: {', '.join(selected)}")
        
        # Run analysis
        matches = safe_analysis.analyze_symptoms(selected, diseases)
        report = safe_analysis.generate_report(selected, matches, descriptions, precautions)
        
        # Display summary
        print("\n" + "="*70)
        print("  ANALYSIS COMPLETE")
        print("="*70)
        print(f"\n📊 Found {report['analysis']['total_matches']} potential matches")
        print(f"   High confidence: {len(report['analysis']['high_confidence'])}")
        
        if report['top_diagnoses']:
            top = report['top_diagnoses'][0]
            print(f"\n🏥 Top Match: {top['disease']} ({top['confidence']})")
        
        # Print wrapped report with disclaimer banner
        safe_analysis.print_report(report)

        # Save reports
        json_file = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        md_file = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        save_markdown_report(report, md_file)
        
        print(f"\n📄 Reports saved:")
        print(f"   - {json_file}")
        print(f"   - {md_file}")
        
        print("\n" + "="*70)
        print("\nAnalyze more symptoms? (y/n): ", end="")
        if input().strip().lower() != 'y':
            print("\n👋 Thank you for using Operation Nightingale!")
            print("   For US - The Gift is free for all. 🚀")
            break

if __name__ == "__main__":
    interactive_session()
