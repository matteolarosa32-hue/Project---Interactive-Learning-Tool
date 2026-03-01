import os

def get_available_topics(): 
        files = [f for f in os.listdir('.') if f.endswith('.json') and "_disabled" not in f] # the listdir function gets all the files in the current directory, it is part of the os module.
        return [
                {
                        "pretty": f.replace('.json', '').replace('_', ' ').title(),
                        "filename": f
                } 
                  for f in files
                ] #the function returns a list of dictionaries, where each one has a user friendly name.