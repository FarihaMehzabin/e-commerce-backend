// Add category
document
  .getElementById("add-category-form")
  .addEventListener("submit", async (event) => {
    event.preventDefault();

    let categoryNameInput = document.getElementById("add-category");
    let categoryName = categoryNameInput.value.trim();

    if (categoryName) {
      try {
        let response = await fetch(
          "http://127.0.0.1:1234/product/manage-category/create",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ category_name: categoryName }),
          }
        );

        let data = await response.json();
        alert(data.message);
        location.reload();
      } catch (error) {
        console.error("Error:", error);
      }
    } else {
      alert("Category name cannot be empty.");
    }
  });

  
// Edit category
document.querySelectorAll(".edit-category").forEach((button) => {
  button.addEventListener("click", async () => {
    let categoryName = button.getAttribute("data-name");

    console.log(categoryName);

    let newCategoryName = prompt(
      "Enter the new name for the category:",
      categoryName
    );

    console.log(newCategoryName);

    if (newCategoryName) {
      try {
        let response = await fetch(
          "http://127.0.0.1:1234/product/manage-category/edit",
          {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              category_name: categoryName,
              new_category: newCategoryName,
            }),
          }
        );

        let data = await response.json();
        alert(data.message);
        location.reload();
      } catch (error) {
        console.error("Error:", error);
      }
    }
  });
});

// Delete category
document.querySelectorAll(".delete-category").forEach((button) => {
  button.addEventListener("click", async () => {
    let categoryName = button.getAttribute("data-name");

    if (
      confirm(`Are you sure you want to delete the ${categoryName} category?`)
    ) {
      try {
        let response = await fetch(
          "http://127.0.0.1:1234/product/manage-category/delete",
          {
            method: "DELETE",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ category_name: categoryName }),
          }
        );

        let data = await response.json();
        alert(data.message);
        location.reload();
      } catch (error) {
        console.error("Error:", error);
      }
    }
  });
});
