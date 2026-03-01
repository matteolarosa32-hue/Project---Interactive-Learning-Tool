import os

def get_available_topics():
    """
    Centralized function to scan for .json files.
    Excludes system files and disabled files.
    """
    files = os.listdir('.') 
    
    # Combined filtering logic
    json_files = [
        f for f in files 
        if f.endswith('.json') 
        and f != 'disabled_questions.json' 
        and not f.endswith('_disabled.json')
        and "_disabled" not in f # Covers both class and main logic
    ]
    
    topics = []
    for f in json_files:
        pretty_name = f.replace('.json', '').replace('_', ' ').title()
        topics.append({
            "pretty": pretty_name,
            "filename": f
        })
    
    return topics