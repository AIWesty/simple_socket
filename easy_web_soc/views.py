def index() -> str:
    with open('easy_web_soc/templates/index.html', 'r') as template:
        return template.read()
    
    

def blog() -> str:
    with open('easy_web_soc/templates/blog.html', 'r') as template:
        return template.read()
    
    