import os

directory = r'c:\Users\Admin\Desktop\Tamilverse_app\templates\pages'

for filename in os.listdir(directory):
    if filename.endswith('.html'):
        path = os.path.join(directory, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content.replace('\"\"https\":', '\"https:')
        new_content = new_content.replace('\"\"http\":', '\"http:')
        
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        
print('Fixed URLs in templates.')
