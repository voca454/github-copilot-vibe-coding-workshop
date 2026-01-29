import React from "react";

const Search = ({ onSearch }) => {
  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Tìm kiếm sản phẩm..."
        onChange={(e) => onSearch(e.target.value)}
      />
    </div>
  );
};

export default Search;
