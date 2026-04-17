#!/usr/bin/env python3
"""
Zero-Cost Orchestrator - Uses Ollama instead of paid APIs
Total cost: $0/month
"""
import json
from agents.scanner import ScannerAgent
from agents.researcher import ResearcherAgent
from agents.analyst import AnalystAgent
from agents.reporter import ReporterAgent
from agents.ollama_agent import OllamaAgent

class FreeOrchestrator:
    """Zero-cost orchestrator using Ollama"""
    
    def __init__(self):
        self.scanner = ScannerAgent()
        self.researcher = ResearcherAgent()
        self.analyst = AnalystAgent()
        self.reporter = ReporterAgent()
        self.ollama = OllamaAgent(model='llama3.2:3b')  # FREE!
        
        print("🎉 Zero-Cost Mode: Using Ollama (FREE)")
        print(f"   Model: {self.ollama.model}")
        print(f"   Cost: $0/month")
        print()
    
    def run_free_pipeline(self, config: dict, criteria: dict):
        """
        Run complete pipeline with zero cost
        
        Args:
            config: Scanning configuration
            criteria: Investor criteria
        """
        print("🚀 Starting ZERO-COST Land Development Pipeline")
        print("=" * 60)
        print("💰 Total Cost: $0")
        print("🤖 AI: Ollama (local)")
        print("📊 Data: Free public sources")
        print("=" * 60)
        
        # Step 1: Scan
        print("\n📡 STEP 1: SCANNING (Cost: $0)")
        print("-" * 60)
        scan_results = self.scanner.scan_all(config)
        
        all_parcels = (
            scan_results['county_records'] +
            scan_results['rezoning_announcements']
        )
        
        if not all_parcels:
            print("\n❌ No parcels found")
            return
        
        print(f"\n✅ Found {len(all_parcels)} parcels (Cost: $0)")
        
        # Process each parcel
        total_cost = 0.0
        reports = []
        
        for i, parcel in enumerate(all_parcels, 1):
            print(f"\n{'='*60}")
            print(f"PARCEL {i}/{len(all_parcels)} - Cost So Far: ${total_cost:.4f}")
            print(f"{'='*60}")
            
            # Step 2: Research (free data sources)
            print("\n🔬 STEP 2: RESEARCH (Cost: $0)")
            print("-" * 60)
            research = self.researcher.research_parcel(parcel)
            
            # Step 3: AI Analysis with Ollama (FREE!)
            print("\n🤖 STEP 3: AI ANALYSIS (Cost: $0)")
            print("-" * 60)
            
            # Use Ollama for zoning analysis
            zoning_analysis = self.ollama.analyze_zoning(
                research['zoning']['current_zoning'],
                parcel
            )
            print(f"  🧠 Zoning Analysis: {zoning_analysis['analysis'][:100]}...")
            
            # Regular analysis
            analysis = self.analyst.analyze_parcel(research, criteria)
            
            # Use Ollama for investment evaluation
            investment_eval = self.ollama.evaluate_investment(research, criteria)
            print(f"  💰 Investment Eval: {investment_eval['evaluation'][:100]}...")
            
            # Add AI insights to analysis
            analysis['ai_insights'] = {
                'zoning_analysis': zoning_analysis,
                'investment_evaluation': investment_eval
            }
            
            # Step 4: Report
            print("\n📄 STEP 4: REPORT (Cost: $0)")
            print("-" * 60)
            
            # Generate AI summary
            summary = self.ollama.generate_summary(analysis)
            analysis['ai_summary'] = summary
            
            report = self.reporter.generate_report(analysis, research)
            
            reports.append({
                'parcel_id': parcel.get('parcel_id'),
                'match_score': analysis['evaluation']['match_score'],
                'roi': analysis['roi']['roi_percentage'],
                'report_file': report['report_file'],
                'ai_summary': summary,
                'cost': 0.0  # FREE!
            })
            
            print(f"  💰 Parcel Cost: $0.00")
            print(f"  📊 Total Cost: ${total_cost:.4f}")
        
        # Summary
        print(f"\n{'='*60}")
        print("📊 ZERO-COST PIPELINE COMPLETE")
        print(f"{'='*60}")
        print(f"\nTotal Parcels: {len(reports)}")
        print(f"Total Cost: ${total_cost:.4f}")
        print(f"Cost per Parcel: ${total_cost/len(reports) if reports else 0:.4f}")
        print(f"\n🎉 SAVINGS vs GPT-4: ${len(reports) * 0.50:.2f}")
        print(f"🎉 SAVINGS vs Claude: ${len(reports) * 0.30:.2f}")
        
        print(f"\nResults:")
        for report in sorted(reports, key=lambda x: x['match_score'], reverse=True):
            print(f"\n  {report['parcel_id']}")
            print(f"    Match: {report['match_score']:.1f}%")
            print(f"    ROI: {report['roi']:.1f}%")
            print(f"    Cost: ${report['cost']:.4f}")
            print(f"    Summary: {report['ai_summary'][:80]}...")
        
        # Save summary
        with open('free_pipeline_summary.json', 'w') as f:
            json.dump({
                'total_analyzed': len(reports),
                'total_cost': total_cost,
                'cost_per_parcel': total_cost / len(reports) if reports else 0,
                'model_used': self.ollama.model,
                'reports': reports
            }, f, indent=2)
        
        print(f"\n💾 Summary: free_pipeline_summary.json")
        print(f"\n✅ Done! Total cost: ${total_cost:.4f} (basically FREE!)")

def main():
    """Run zero-cost pipeline"""
    orchestrator = FreeOrchestrator()
    
    config = {
        'counties': [
            {'county': 'Travis', 'state': 'TX'},
        ],
        'cities': [
            {'city': 'Austin', 'state': 'TX'},
        ],
        'regions': []
    }
    
    criteria = {
        'min_acres': 5,
        'max_price': 500000,
        'allowed_zoning': ['R-1', 'Residential'],
        'utilities_required': ['water', 'sewer', 'electric'],
        'value_per_acre_after_dev': 120000,
        'target_roi': 25,
        'development_timeline_years': 2
    }
    
    orchestrator.run_free_pipeline(config, criteria)

if __name__ == '__main__':
    main()
