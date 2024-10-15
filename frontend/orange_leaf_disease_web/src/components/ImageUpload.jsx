import axios from "axios";
import { useState } from "react";

const ImageUpload = () => {
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [className, setClassName] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImageChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setImage(file);
      setImagePreview(URL.createObjectURL(file));
      setPrediction(null);
      setClassName(null);
    } else {
      setImage(null);
      setImagePreview(null);
    }
  };

  const handlePredict = async () => {
    setLoading(true);
    const formData = new FormData();
    if (image) {
      formData.append("file", image);
      // onPredict(formData);
    } else {
      alert("Please upload an image before predicting.");
    }
    try {
      const response = await axios.post(
        "http://localhost:8000/predict",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      console.log(response?.data?.Class_Name);
      console.log(response?.data?.Confidence);
      setPrediction(response?.data?.Confidence);
      setClassName(response?.data?.Class_Name);
    } catch (error) {
      console.error("Error while predicting:", error);
      setPrediction("Error occurred while predicting.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        textAlign: "center",
        padding: "20px",
      }}
    >
      <h3>Upload an Image for Prediction</h3>
      <input type="file" accept="image/*" onChange={handleImageChange} />
      {imagePreview && (
        <div style={{ marginTop: "10px" }}>
          <img src={imagePreview} alt="Preview" width="500" height="500" />
        </div>
      )}
      <button
        onClick={handlePredict}
        style={{ marginTop: "10px" }}
        disabled={loading}
      >
        {loading ? "Predicting..." : "Predict"}
      </button>

      {prediction && (
        <>
          <div style={{ marginTop: 20 }}>Class: {className}</div>
          <div style={{ marginTop: 20 }}>
            Prediction: {(prediction * 100).toFixed(2)} %
          </div>
        </>
      )}
    </div>
  );
};

export default ImageUpload;
