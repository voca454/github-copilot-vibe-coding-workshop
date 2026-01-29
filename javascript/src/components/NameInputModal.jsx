import React from "react";

const NameInputModal = ({ onSubmit }) => {
  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Chào mừng!</h2>
        <p>Vui lòng nhập tên của bạn để tiếp tục:</p>
        <input type="text" id="usernameInput" placeholder="Tên người dùng..." />
        <button
          onClick={() =>
            onSubmit(document.getElementById("usernameInput").value)
          }
        >
          Bắt đầu
        </button>
      </div>
    </div>
  );
};

export default NameInputModal;
