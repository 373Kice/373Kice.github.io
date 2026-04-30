import os
files = [f for f in os.listdir('D:/github/373Kice.github.io') if f.endswith('.pptx')]
print('PPT files found:')
for f in files:
    size = os.path.getsize(f'D:/github/373Kice.github.io/{f}')
    print(f'  {f}  ({size//1024} KB)')
