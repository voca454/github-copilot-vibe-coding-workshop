import React, { useState, useEffect } from "react";
import Home from "./components/Home";
import Search from "./components/Search";
import PostModal from "./components/PostModal";
import NameInputModal from "./components/NameInputModal";

function App() {
  const [posts, setPosts] = useState([]);
  const [username, setUsername] = useState(
    localStorage.getItem("username") || "",
  );
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Gọi API lấy bài đăng từ Backend Python
  const fetchPosts = async () => {
    try {
      const response = await fetch("http://localhost:8000/posts");
      const data = await response.json();
      setPosts(data);
    } catch (err) {
      console.error("Không thể kết nối Backend:", err);
    }
  };

  useEffect(() => {
    if (username) fetchPosts();
  }, [username]);

  if (!username) {
    return (
      <NameInputModal
        onSubmit={(name) => {
          localStorage.setItem("username", name);
          setUsername(name);
        }}
      />
    );
  }

  return (
    <div className="container">
      <nav className="navbar">
        <h1>Contoso Vibe</h1>
        <button onClick={() => setIsModalOpen(true)}>Đăng bài</button>
      </nav>
      <Search
        onSearch={(term) => {
          /* Logic tìm kiếm */
        }}
      />
      <Home posts={posts} />
      <PostModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </div>
  );
}

export default App;
