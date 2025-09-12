//get getCookie csrftoken
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

//update pics
document.addEventListener('DOMContentLoaded', function () {
  const input = document.querySelector('input[type="file"]');
  const preview = document.getElementById('preview');

  if (input && preview) {
    input.addEventListener('change', function () {
      const file = this.files[0];
      if (file) {
        preview.src = URL.createObjectURL(file);
        preview.style.display = 'block';
      } else {
        preview.style.display = 'none';
      }
    });
  }

  document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', function () {
      const card = this.closest('[data-id]');
      const picId = card.getAttribute('data-id');

      fetch(`/pictures/delete/${picId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
        }
      })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            card.remove();
          } else {
            alert("Không thể xóa ảnh.");
          }
        });
    });
  });
});
// end update pics


