#!/usr/bin/env python3
"""
Ollama Integration - Zero-cost AI reasoning
"""
import json
import subprocess
from typing import Dict, List

class OllamaAgent:
    """Uses local Ollama models for zero-cost AI reasoning"""
    
    def __init__(self, model: str = 'llama3.2:3b'):
        self.model = model
        self.check_ollama()
    
    def check_ollama(self):
        """Check if Ollama is installed and model is available"""
        try:
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if self.model not in result.stdout:
                print(f"⚠️  Model {self.model} not found. Pulling...")
                self.pull_model()
        except FileNotFoundError:
            print("❌ Ollama not installed!")
            print("Install: curl -fsSL https://ollama.com/install.sh | sh")
            print("Then run: ollama pull llama3.2:3b")
            raise
    
    def pull_model(self):
        """Pull the model if not available"""
        print(f"📥 Pulling {self.model}...")
        subprocess.run(['ollama', 'pull', self.model], check=True)
        print(f"✅ Model {self.model} ready")
    
    def chat(self, prompt: str, system: str = None) -> str:
        """
        Send prompt to Ollama and get response
        
        Args:
            prompt: User prompt
            system: System prompt (optional)
            
        Returns:
            Model response
        """
        messages = []
        if system:
            messages.append({'role': 'system', 'content': system})
        messages.append({'role': 'user', 'content': prompt})
        
        # Build ollama command
        cmd = ['ollama', 'run', self.model]
        
        # Send prompt
        result = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        return result.stdout.strip()
    
    def analyze_zoning(self, zoning_code: str, parcel_info: Dict) -> Dict:
        """
        Analyze zoning regulations using AI
        
        Args:
            zoning_code: Zoning designation
            parcel_info: Parcel information
            
        Returns:
            Analysis results
        """
        prompt = f"""Analyze this zoning code for land development:

Zoning: {zoning_code}
Parcel Size: {parcel_info.get('acres', 'unknown')} acres
Location: {parcel_info.get('address', 'unknown')}

Provide:
1. What can be built here?
2. Key restrictions
3. Development potential (1-10 score)
4. Risks to consider

Be concise and practical."""

        response = self.chat(prompt)
        
        # Parse response (simplified)
        return {
            'zoning_code': zoning_code,
            'analysis': response,
            'model_used': self.model,
            'cost': 0.0  # FREE!
        }
    
    def evaluate_investment(self, research: Dict, criteria: Dict) -> Dict:
        """
        Evaluate investment potential using AI
        
        Args:
            research: Research data
            criteria: Investment criteria
            
        Returns:
            Investment evaluation
        """
        prompt = f"""Evaluate this land investment opportunity:

PROPERTY:
- Size: {research['gis_data']['boundaries']['area_acres']} acres
- Zoning: {research['zoning']['current_zoning']}
- Price: ${research['basic_info'].get('price', 0):,}
- Utilities: {', '.join(k for k, v in research['gis_data']['infrastructure']['utilities'].items() if v == 'available')}

INVESTOR CRITERIA:
- Min Size: {criteria.get('min_acres', 0)} acres
- Budget: ${criteria.get('max_price', 0):,}
- Target ROI: {criteria.get('target_roi', 0)}%

ANALYSIS NEEDED:
1. Match score (0-100)
2. Investment grade (A-F)
3. Top 3 pros
4. Top 3 cons
5. Recommended action

Be direct and data-driven."""

        response = self.chat(prompt)
        
        return {
            'parcel_id': research['parcel_id'],
            'evaluation': response,
            'model_used': self.model,
            'cost': 0.0  # FREE!
        }
    
    def generate_summary(self, analysis: Dict) -> str:
        """
        Generate executive summary using AI
        
        Args:
            analysis: Complete analysis data
            
        Returns:
            Executive summary
        """
        prompt = f"""Create a 3-sentence executive summary for this land development opportunity:

Match Score: {analysis['evaluation']['match_score']:.1f}%
ROI: {analysis['roi']['roi_percentage']:.1f}%
Investment: ${analysis['roi']['total_investment']:,}
Profit: ${analysis['roi']['estimated_profit']:,}

Make it compelling for an investor."""

        return self.chat(prompt)

def main():
    """Test Ollama integration"""
    agent = OllamaAgent()
    
    # Test zoning analysis
    result = agent.analyze_zoning('R-1', {
        'acres': 5.2,
        'address': '123 Main St'
    })
    
    print("🤖 Ollama Analysis:")
    print(result['analysis'])
    print(f"\n💰 Cost: ${result['cost']} (FREE!)")

if __name__ == '__main__':
    main()
