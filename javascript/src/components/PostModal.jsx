import React from "react";

const PostModal = ({ isOpen, onClose, onSubmit }) => {
  if (!isOpen) return null;
  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Tạo bài viết mới</h2>
        <textarea id="postContent" placeholder="Bạn đang nghĩ gì?"></textarea>
        <button
          onClick={() => onSubmit(document.getElementById("postContent").value)}
        >
          Đăng
        </button>
        <button onClick={onClose}>Hủy</button>
      </div>
    </div>
  );
};

export default PostModal;
