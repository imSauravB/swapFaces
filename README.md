# swapFaces

Install the following dependencies:

1. python3
2. pip
3. ffmpeg
4. visual studio 2022 runtimes (windows)

pip install -r requirements.txt

## CLI Commands
python swapFacesMain.py

python swapFacesMain.py --[options]

```
options:
  -f SOURCE_IMG, --face SOURCE_IMG
                        use this face
  -t TARGET_PATH, --target TARGET_PATH
                        replace this face
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        save output to this file
  --gpu                 use gpu
  --keep-fps            maintain original fps
```