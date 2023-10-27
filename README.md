# Content based Image Retrieval

## Aim:
To build a content based image retrieval system that retrieves similar images matching the search image
## Method:
I trained a VGG model to give embeddings for images of Fashion dataset. Then used KNN to give similar images based on the embeddings of the search Image.
## To run:
Add the folder of your images and create a csv with image paths like styles.csv. Open two terminals, one for frontend and one for backend and run the the commands as follows:

## Frontend: React 
```bash
npm run dev
```
## Backend: Flask
```bash
python -m flask run
```
## Example 1:
![image](https://github.com/mudrap17/content-based-image-retrieval/assets/76879120/2a5d94a0-1e5a-498a-8be4-20b207c66e30)

## Example 2
![image](https://github.com/mudrap17/content-based-image-retrieval/assets/76879120/9e9ab190-2cad-4f02-9af8-5c2b7a961fc5)




