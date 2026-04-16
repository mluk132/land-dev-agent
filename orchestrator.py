#!/usr/bin/env python3
"""
Main Orchestrator - Coordinates all agents
"""
import json
from agents.scanner import ScannerAgent
from agents.researcher import ResearcherAgent
from agents.analyst import AnalystAgent
from agents.reporter import ReporterAgent

class LandDevOrchestrator:
    """Orchestrates the multi-agent land development system"""
    
    def __init__(self):
        self.scanner = ScannerAgent()
        self.researcher = ResearcherAgent()
        self.analyst = AnalystAgent()
        self.reporter = ReporterAgent()
    
    def run_full_pipeline(self, config: dict, criteria: dict, recipient: str = None):
        """
        Run complete pipeline: Scan → Research → Analyze → Report
        
        Args:
            config: Scanning configuration
            criteria: Investor criteria
            recipient: Email for alerts
        """
        print("🚀 Starting Land Development AI Pipeline")
        print("=" * 60)
        
        # Step 1: Scan for opportunities
        print("\n📡 STEP 1: SCANNING FOR OPPORTUNITIES")
        print("-" * 60)
        scan_results = self.scanner.scan_all(config)
        
        all_parcels = (
            scan_results['county_records'] +
            scan_results['rezoning_announcements']
        )
        
        if not all_parcels:
            print("\n❌ No parcels found. Adjust search criteria.")
            return
        
        print(f"\n✅ Found {len(all_parcels)} parcels to analyze")
        
        # Process each parcel
        reports = []
        
        for i, parcel in enumerate(all_parcels, 1):
            print(f"\n{'='*60}")
            print(f"PROCESSING PARCEL {i}/{len(all_parcels)}")
            print(f"{'='*60}")
            
            # Step 2: Research
            print("\n🔬 STEP 2: RESEARCHING PARCEL")
            print("-" * 60)
            research = self.researcher.research_parcel(parcel)
            
            # Step 3: Analyze
            print("\n📊 STEP 3: ANALYZING FEASIBILITY")
            print("-" * 60)
            analysis = self.analyst.analyze_parcel(research, criteria)
            
            # Step 4: Report
            print("\n📄 STEP 4: GENERATING REPORT")
            print("-" * 60)
            report = self.reporter.generate_report(analysis, research, recipient)
            
            reports.append({
                'parcel_id': parcel.get('parcel_id'),
                'match_score': analysis['evaluation']['match_score'],
                'roi': analysis['roi']['roi_percentage'],
                'report_file': report['report_file'],
                'recommendation': analysis['evaluation']['recommendation']
            })
        
        # Summary
        print(f"\n{'='*60}")
        print("📊 PIPELINE COMPLETE - SUMMARY")
        print(f"{'='*60}")
        print(f"\nTotal Parcels Analyzed: {len(reports)}")
        print(f"\nResults:")
        
        for report in sorted(reports, key=lambda x: x['match_score'], reverse=True):
            print(f"\n  {report['parcel_id']}")
            print(f"    Match Score: {report['match_score']:.1f}%")
            print(f"    ROI: {report['roi']:.1f}%")
            print(f"    Recommendation: {report['recommendation']}")
            print(f"    Report: {report['report_file']}")
        
        # Save summary
        with open('pipeline_summary.json', 'w') as f:
            json.dump({
                'total_analyzed': len(reports),
                'reports': reports
            }, f, indent=2)
        
        print(f"\n💾 Summary saved to pipeline_summary.json")
        print(f"\n✅ All done! Check the generated reports.")

def main():
    """Example usage"""
    orchestrator = LandDevOrchestrator()
    
    # Scanning configuration
    config = {
        'counties': [
            {'county': 'Travis', 'state': 'TX'},
        ],
        'cities': [
            {'city': 'Austin', 'state': 'TX'},
        ],
        'regions': []
    }
    
    # Investor criteria
    criteria = {
        'min_acres': 5,
        'allowed_zoning': ['R-1', 'Residential'],
        'utilities_required': ['water', 'sewer', 'electric'],
        'value_per_acre_after_dev': 120000,
        'development_timeline_years': 2
    }
    
    # Run pipeline
    orchestrator.run_full_pipeline(
        config,
        criteria,
        recipient='developer@example.com'
    )

if __name__ == '__main__':
    main()
