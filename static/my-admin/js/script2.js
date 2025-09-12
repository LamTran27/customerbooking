document.addEventListener('DOMContentLoaded', function () {
    // Khai báo biến
    const urls = JSON.parse(document.getElementById('django-urls').textContent);
    const createUrl = urls.create;
    const deleteUrl = urls.delete;
    const groupName = urls.group;

    function getCustomerUrl(customerId) {
    return `${urls.get}${customerId}/`;
    }
    function updateCustomerUrl(customerId) {
    return `${urls.update}${customerId}/`;
    }


   // Lấy CSRF token từ cookie
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

      // Tạo khách hàng mới
      document.getElementById('customerForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const form = this;
        const formData = new FormData(form);
        const customerId = form.dataset.editingId;
        //console.log("Cutsomer update: ", customerId);
        const url = customerId
          ? updateCustomerUrl(customerId)
          : createUrl;

        fetch(url, {
          method: 'POST',
          headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
          },
          body: formData
        })
        .then(response => response.json())
        .then(data => {
          if (data.success && data.customer) {
            if (customerId) {
              updateCustomerRow(data.customer); // ✅ hoặc updateCustomerRow(data.customer)
            } else {
              addCustomerRow(data.customer);
            }

            form.reset();
            delete form.dataset.editingId; // ✅ xóa trạng thái sửa
          } else {
            alert("Lỗi: " + data.error);
          }
        });
      });
      // End Tạo khách hàng mới

      //Lưu dữ liệu vào danh sách
      function addCustomerRow(customer) {
        const table = document.getElementById('customerTable');
        const row = document.createElement('tr');
        row.classList.add('customer-item');
        row.dataset.id = customer.id; // Gán ID để dùng cho xóa/sửa

        const noDataRow = document.getElementById('no-data-row');
        if (noDataRow) {
          noDataRow.remove();
        }

        let extraColumns = '';
        if (groupName === "Toyota") {
          extraColumns = `
            <td>${customer.KHDV || ''}</td>
            <td>${customer.CVDV || ''}</td>
          `;
        }

        row.innerHTML = `
          <td>${formatDate(customer.adddate)}</td>
          <td>${formatTime(customer.adddate)}</td>
          <td>${customer.name}</td>
          <td>${customer.plate}</td>
          <td>${customer.note}</td>
           ${extraColumns}
          <td>
            <button class="btn btn-sm btn-warning edit-btn" data-id="${customer.id}">Sửa</button>
            <button class="btn btn-sm btn-danger delete-btn" data-id="${customer.id}">Xóa</button>
          </td>
        `;

        table.appendChild(row);
        //attachRowEvents(row);
      }
      //End lưu dữ liệu vào danh sÁCH

      //Cập nhật dữ liệu chỉnh sửa
      function updateCustomerRow(customer) {
        const row = document.querySelector(`tr.customer-item[data-id="${customer.id}"]`);
        if (!row) {
          console.warn("Không tìm thấy dòng khách hàng để cập nhật:", customer.id);
          return;
        }

        let extraColumns = '';
        if (typeof groupName !== 'undefined' && groupName === "Toyota") {
          extraColumns = `
            <td>${customer.KHDV || ''}</td>
            <td>${customer.CVDV || ''}</td>
          `;
        }

        row.innerHTML = `
          <td>${formatDate(customer.adddate)}</td>
          <td>${formatTime(customer.adddate)}</td>
          <td>${customer.name}</td>
          <td>${customer.plate}</td>
          <td>${customer.note}</td>
          ${extraColumns}
          <td>
            <button class="btn btn-sm btn-warning edit-btn" data-id="${customer.id}">Sửa</button>
            <button class="btn btn-sm btn-danger delete-btn" data-id="${customer.id}">Xóa</button>
          </td>
        `;

        //attachRowEvents(row); // ✅ nếu bạn gắn sự kiện thủ công
      }
      //End cập nhật dữ liệu chỉnh sửa
      
      // Gắn sự kiện xóa và sửa cho dòng mới
      function attachRowEvents(row) {
        const editBtn = row.querySelector('.edit-btn');
        if (editBtn) {
          editBtn.addEventListener('click', function (e) {
            const customerId = editBtn.dataset.id;
            handleEdit(customerId); // ✅ Truyền đúng ID
          });
        }
      }

        // Xử lý xóa khách hàng
         document.getElementById('customerTable').addEventListener('click', function (e) {
          if (e.target.classList.contains('delete-btn')) {
            const row = e.target.closest('.customer-item');
            const customerId = row.dataset.id;

            const confirmed = confirm("Bạn có chắc chắn muốn xóa khách hàng này?");
            if (!confirmed) return;

            fetch(deleteUrl, {
              method: 'POST',
              headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded'
              },
              body: `id=${customerId}`
            })
            .then(res => res.json())
            .then(data => {
              if (data.success) {
                row.remove();
              } else {
                alert("Lỗi: " + data.error);
              }
            })
            .catch(err => {
              console.error("Lỗi khi gửi request xóa:", err);
              alert("Đã xảy ra lỗi khi xóa khách hàng.");
            });
          }
        });
      // End Xử lý xóa khách hàng

        // Xử lý sửa khách hàng (placeholder)
        document.getElementById('customerTable').addEventListener('click', function (e) {
          const editBtn = e.target.closest('.edit-btn');
          if (editBtn) {
            const customerId = editBtn.dataset.id;
            handleEdit(customerId); // ✅ Truyền đúng ID
          }
        });

       function handleEdit(customerId) {
            //console.log("customerId:", customerId)
            fetch(getCustomerUrl(customerId))
              .then(res => {
                if (!res.ok) {
                  throw new Error(`HTTP error ${res.status}`);
                }
                return res.json();
              })
              .then(data => {
                if (data.success && data.customer) {
                  const customer = data.customer;

                  document.getElementById('id_name').value = customer.name || '';
                  document.getElementById('id_plate').value = customer.plate || '';
                  document.getElementById('id_note').value = customer.note || '';
                  document.getElementById('id_adddate').value = toLocalDatetimeString(customer.adddate) || '';
                  document.getElementById('id_KHDV').value = customer.KHDV || '';
                  document.getElementById('id_CVDV').value = customer.CVDV || '';

                  // Gán ID để biết đang sửa ai
                  document.getElementById('customerForm').dataset.editingId = customerId;

                  // Cuộn đến form
                  document.getElementById('customerForm').scrollIntoView({ behavior: 'smooth' });
                } else {
                  alert("Không tìm thấy khách hàng.");
                }
              })
              .catch(err => {
                console.error("Lỗi khi lấy dữ liệu khách hàng:", err);
                alert("Đã xảy ra lỗi khi lấy dữ liệu.");
              });
          }
  
        function toLocalDatetimeString(isoString) {
          const date = new Date(isoString);
          const pad = n => n.toString().padStart(2, '0');
          return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`;
        }
        // Format ngày và giờ từ chuỗi ISO
        function formatDate(isoString) {
        const date = new Date(isoString);
        return date.toLocaleDateString('vi-VN');
        }

        function formatTime(isoString) {
          const date = new Date(isoString);
          return date.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });
        }

        // Gắn sự kiện xóa/sửa cho các dòng đã render sẵn
        document.querySelectorAll('.customer-item').forEach(row => attachRowEvents(row));
       
   // End upload picture
});