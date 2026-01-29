import React from "react";

const PostDetails = ({ post, comments }) => {
  if (!post) return null;
  return (
    <div className="post-details">
      <h3>{post.username}</h3>
      <p>{post.content}</p>
      <hr />
      <h5>Bình luận:</h5>
      {comments.map((c) => (
        <div key={c.id} className="comment">
          <strong>{c.username}: </strong> {c.content}
        </div>
      ))}
    </div>
  );
};

export default PostDetails;
