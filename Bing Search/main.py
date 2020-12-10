import webbrowser as web

"""This will do a Bing Search you Input"""
def bing_search(topic):
    '''Searches about the topic on Bing'''
    link = 'https://www.bing.com/search?q={}'.format(topic)
    web.open(link)
    
bing_search(str(input("What can I search for you:")))