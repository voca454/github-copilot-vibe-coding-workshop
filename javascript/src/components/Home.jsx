import React from "react";

const Home = ({ posts }) => {
  return (
    <div className="home-container">
      <header className="header">
        <h1>Contoso Social</h1>
      </header>
      <main className="post-list">
        {posts.map((post) => (
          <div key={post.id} className="post-card">
            <h4>@{post.username}</h4>
            <p>{post.content}</p>
            <small>{new Date(post.createdAt).toLocaleString()}</small>
          </div>
        ))}
      </main>
    </div>
  );
};

export default Home;
