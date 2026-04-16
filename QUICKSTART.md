# Quick Start Guide

Get your land development AI agent running in 5 minutes.

## Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/land-dev-agent.git
cd land-dev-agent

# Install dependencies
pip install -r requirements.txt

# Make scripts executable
chmod +x orchestrator.py agents/*.py
```

## Run the MVP

```bash
# Run the complete pipeline
python orchestrator.py
```

This will:
1. Scan for land opportunities
2. Research each parcel
3. Analyze feasibility
4. Generate reports

## Customize for Your Needs

Edit `orchestrator.py` to set your criteria:

```python
criteria = {
    'min_acres': 10,  # Minimum 10 acres
    'allowed_zoning': ['R-1', 'Agricultural'],
    'utilities_required': ['water', 'electric'],
    'value_per_acre_after_dev': 150000,
}
```

## Output

Check the generated files:
- `report_*.md` - Detailed feasibility reports
- `pipeline_summary.json` - Summary of all analyzed parcels

## Next Steps

1. Integrate with real data sources (GIS APIs, county records)
2. Add AI reasoning with OpenAI/Claude
3. Build web interface
4. Deploy to production

See README.md for full documentation.
