import { useState } from "react";
import { Input, Button } from "antd";

export default function Home() {
  const [PId, setPId] = useState<string>("");
  const [product, setProduct] = useState<any>(null);
  const [error, setError] = useState<string>("");

  const daSearch = async () => {
    if (!PId) return;
    try {
      const response = await fetch(`http://localhost:5000/products/${PId}`);
      const data = await response.json();
      setProduct(data);
    } catch (error) {
      setError((error as Error).message);
    }
  };

  const daError = () => {
    if (!error) return null;
    return <div>{error}</div>;
  };
  
  const daProduct = () => {
    if (!product) return null;
    return (
      <div style={{ marginTop: "10px" }}>
        <p>ID - {product.id}</p>
        <p>Name - {product.name}</p>
        <p>Description - {product.description}</p>
        <p>Price - ${product.price}</p>
      </div>
    );
  };
  
  return (
    <div>
      <h3>Product Search</h3>
      <div>
        <Input
          placeholder="Enter the product ID"
          value={PId}
          onChange={(e) => setPId(e.target.value)}
          style={{ width: "175px", marginRight: "10px" }}
        />
        <Button onClick={daSearch}>Search</Button>
      </div>
      {daError()}
      {daProduct()}
    </div>
  );
}