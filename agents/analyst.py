#!/usr/bin/env python3
"""
Agent C: Analyst
Evaluates parcels against investor criteria and calculates feasibility
"""
import os
import json
from typing import Dict, List

class AnalystAgent:
    """Analyzes parcel feasibility and investment potential"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
    
    def evaluate_criteria(self, research: Dict, criteria: Dict) -> Dict:
        """
        Evaluate parcel against investor criteria
        
        Args:
            research: Research data from ResearcherAgent
            criteria: Investor requirements
            
        Returns:
            Evaluation results with match score
        """
        print(f"📊 Evaluating {research['parcel_id']} against criteria...")
        
        matches = []
        mismatches = []
        score = 0
        max_score = 0
        
        # Check size requirements
        if 'min_acres' in criteria:
            max_score += 10
            acres = research['gis_data']['boundaries']['area_acres']
            if acres >= criteria['min_acres']:
                matches.append(f"Size: {acres} acres (meets {criteria['min_acres']} min)")
                score += 10
            else:
                mismatches.append(f"Size: {acres} acres (below {criteria['min_acres']} min)")
        
        # Check zoning
        if 'allowed_zoning' in criteria:
            max_score += 15
            current = research['zoning']['current_zoning']
            if any(z in current for z in criteria['allowed_zoning']):
                matches.append(f"Zoning: {current} (acceptable)")
                score += 15
            else:
                mismatches.append(f"Zoning: {current} (not in allowed list)")
        
        # Check utilities
        if criteria.get('utilities_required'):
            max_score += 10
            utils = research['gis_data']['infrastructure']['utilities']
            if all(utils.get(u) == 'available' for u in criteria['utilities_required']):
                matches.append("All required utilities available")
                score += 10
            else:
                mismatches.append("Some utilities not available")
        
        # Check environmental
        max_score += 10
        if not research['environmental']['wetlands']['present']:
            matches.append("No wetlands present")
            score += 5
        if research['environmental']['hazards']['flood_risk'] == 'Low':
            matches.append("Low flood risk")
            score += 5
        
        match_percentage = (score / max_score * 100) if max_score > 0 else 0
        
        evaluation = {
            'parcel_id': research['parcel_id'],
            'match_score': match_percentage,
            'matches': matches,
            'mismatches': mismatches,
            'recommendation': 'STRONG MATCH' if match_percentage >= 80 else 
                            'POTENTIAL' if match_percentage >= 60 else 'WEAK MATCH'
        }
        
        print(f"  ✅ Match score: {match_percentage:.1f}%")
        return evaluation
    
    def estimate_development_cost(self, research: Dict) -> Dict:
        """
        Estimate development costs
        
        Args:
            research: Research data
            
        Returns:
            Cost estimates
        """
        print(f"💰 Estimating development costs...")
        
        acres = research['gis_data']['boundaries']['area_acres']
        
        # Rough estimates (would use real data in production)
        costs = {
            'land_prep': acres * 5000,  # $5k per acre
            'utilities': 50000 if research['gis_data']['infrastructure']['utilities']['water'] != 'available' else 0,
            'roads': acres * 3000,  # $3k per acre
            'permits': 15000,
            'environmental': 10000,
            'contingency_20pct': 0
        }
        
        subtotal = sum(costs.values())
        costs['contingency_20pct'] = subtotal * 0.20
        costs['total_estimated'] = subtotal + costs['contingency_20pct']
        
        print(f"  ✅ Estimated total: ${costs['total_estimated']:,.0f}")
        return costs
    
    def calculate_roi(self, research: Dict, costs: Dict, criteria: Dict) -> Dict:
        """
        Calculate potential ROI
        
        Args:
            research: Research data
            costs: Development costs
            criteria: Investor criteria with expected returns
            
        Returns:
            ROI calculations
        """
        print(f"📈 Calculating ROI...")
        
        purchase_price = research['basic_info'].get('price', 0)
        total_investment = purchase_price + costs['total_estimated']
        
        # Estimate value after development (simplified)
        acres = research['gis_data']['boundaries']['area_acres']
        estimated_value = acres * criteria.get('value_per_acre_after_dev', 100000)
        
        profit = estimated_value - total_investment
        roi_percentage = (profit / total_investment * 100) if total_investment > 0 else 0
        
        roi = {
            'purchase_price': purchase_price,
            'development_costs': costs['total_estimated'],
            'total_investment': total_investment,
            'estimated_value_after_dev': estimated_value,
            'estimated_profit': profit,
            'roi_percentage': roi_percentage,
            'payback_period_years': criteria.get('development_timeline_years', 2)
        }
        
        print(f"  ✅ Estimated ROI: {roi_percentage:.1f}%")
        return roi
    
    def analyze_parcel(self, research: Dict, criteria: Dict) -> Dict:
        """
        Complete analysis of a parcel
        
        Args:
            research: Research data from ResearcherAgent
            criteria: Investor criteria
            
        Returns:
            Complete analysis
        """
        print(f"\n📊 Analyzing parcel: {research['parcel_id']}")
        
        evaluation = self.evaluate_criteria(research, criteria)
        costs = self.estimate_development_cost(research)
        roi = self.calculate_roi(research, costs, criteria)
        
        analysis = {
            'parcel_id': research['parcel_id'],
            'evaluation': evaluation,
            'costs': costs,
            'roi': roi,
            'risks': [
                'Market conditions may change',
                'Permit approval not guaranteed',
                'Cost estimates are preliminary'
            ],
            'next_steps': [
                'Site visit recommended',
                'Detailed survey needed',
                'Consult with local planning department'
            ]
        }
        
        print(f"✅ Analysis complete for {research['parcel_id']}\n")
        return analysis

def main():
    """Example usage"""
    analyst = AnalystAgent()
    
    # Load research results
    with open('research_results.json', 'r') as f:
        research = json.load(f)
    
    # Investor criteria
    criteria = {
        'min_acres': 5,
        'allowed_zoning': ['R-1', 'Residential'],
        'utilities_required': ['water', 'sewer', 'electric'],
        'value_per_acre_after_dev': 120000,
        'development_timeline_years': 2
    }
    
    analysis = analyst.analyze_parcel(research, criteria)
    
    # Save results
    with open('analysis_results.json', 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"💾 Results saved to analysis_results.json")

if __name__ == '__main__':
    main()
