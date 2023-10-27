import "./index.css";
import { useState } from "react";

const App = () => {
  const [file, setFile] = useState();
  const [similarImages, setSimilarImages] = useState();

  const handleImageUpload = async (event) => {
    const file = await event.target.files[0];
    console.log(file);
    const image = window.URL.createObjectURL(file);

    // Find nearest neighbours
    setFile(image);
    const formData = new FormData();
    formData.append("image", file);

    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      body: formData,
    });
    try {
      console.log(response);
      const res = await response.json();
      let similar_images = res["similar_images"];
      setSimilarImages(similar_images);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="container">
      <h2> Add Image:</h2>
      <br></br>
      <input type="file" onChange={handleImageUpload} />
      <br></br>
      <br></br>
      {file && <img src={file} width="100" />}
      <br></br>
      <br></br>
      <h2 className="title">Similar Images:</h2>
      {similarImages && (
        <div className="images">
          {similarImages.map((imageUrl, index) => (
            <img
              key={index}
              src={`backend\\fashion\\images\\${imageUrl}`}
              alt={`Similar ${index}`}
              width="100"
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default App;
