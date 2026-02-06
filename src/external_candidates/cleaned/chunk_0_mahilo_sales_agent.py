# Extracted from: C:\DEV\PyAgent\src\external_candidates\auto\chunk_0_mahilo_sales_agent.py
# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-mahilo\examples\team_of_agents\mahilo_sales_agent.py
# NOTE: extracted with static-only rules; review before use

def analyze_lead_sources() -> str:

    """Analyze effectiveness of different lead sources"""

    return """

    We've been getting more leads from Reddit lately. 

    """



def collect_feature_feedback() -> str:

    """Analyse past interactions and collect customer feedback about desired features"""

    return """I've analyzed last month's calls. 40 percent of all 

    enterprise customers are interested in an integration with mahilo. 

    """



def generate_sales_insights() -> str:

    """Generate insights about sales patterns and customer preferences"""

    return """

    We should focus on getting more enterprise customers and integrations with mahilo. 

    """



tools = [

    {

        "tool": {

            "type": "function",

            "function": {

                "name": "analyze_lead_sources",

                "description": "Analyze effectiveness of different lead sources",

                "parameters": {}

            }

        },

        "function": analyze_lead_sources,

    },

    {

        "tool": {

            "type": "function",

            "function": {

                "name": "collect_feature_feedback",

                "description": "Analyse past interactions and collect customer feedback about desired features",

                "parameters": {}

            }

        },

        "function": collect_feature_feedback,

    },

    {

        "tool": {

            "type": "function",

            "function": {

                "name": "generate_sales_insights",

                "description": "Generate insights about sales patterns and customer preferences",

                "parameters": {}

            }

        },

        "function": generate_sales_insights,

    }

]