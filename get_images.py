## Importing Necessary Modules
import requests  # to get image from the web
import shutil  # to save it locally
import os
## Set up the image URL and filename
base_url = "https://nccf.church/Images/Blogs"

# bobby_posts =  [6, 7, 8, 12, 13, 14, 16, 18, 20, 22, 23, 24, 25, 26, 27, 29, 31, 34, 37, 38, 41, 43, 48, 52, 55, 56, 60, 63, 64, 67, 71, 73, 80, 81, 82, 83, 84, 90, 97, 98, 99, 100, 109, 111, 112, 114, 119, 124, 127, 130, 136, 137, 146, 154, 156, 157, 158, 159, 166, 170, 177, 178, 186, 187, 190, 195, 196, 198, 203, 207, 210, 214, 217, 221]
# bobby_posts_with_pictures = [6, 7, 8, 12, 25, 43, 97, 98, 99, 100, 109, 111, 112, 114, 119, 124, 127, 130, 136, 137, 146, 154, 156, 157, 158, 159, 166, 170, 177, 178, 186, 187, 190, 195, 196, 198, 203, 207, 210, 214, 217, 221]

lpath = "images/blog/large/"
spath = "images/blog/small/"
for p in [lpath, spath]:
    if not os.path.exists(p):
         os.makedirs(p)


for i in range(0,250):
    lname, sname = f'{i}.jpg', f'{i}_lq.jpg'
    for name, path in {lname:lpath, sname: spath}.items():
        r = requests.get(f'{base_url}/{name}', stream=True)

        print(path, name)
        if r.status_code == 200:
            r.raw.decode_content = True
            with open(f'{path}/{name}', 'wb') as f:
                shutil.copyfileobj(r.raw, f)
            print('passed')
        else:
            print('failed')
