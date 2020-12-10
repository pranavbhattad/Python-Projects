import webbrowser as web

"""This will do a Google Search you Input"""
def google_search(topic):
    '''Searches about the topic on Google'''
    link = 'https://www.google.com/search?q={}'.format(topic)
    web.open(link)
    
google_search(str(input("What can I search for you:")))