// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化所有工具提示
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // 初始化所有弹出框
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // 自动隐藏提示消息
    var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // 搜索框自动聚焦
    var searchInput = document.querySelector('.search-form input[type="search"]');
    if (searchInput) {
        searchInput.focus();
    }

    // 表单验证
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // 密码强度检查
    var passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            var password = this.value;
            var strength = 0;
            
            // 检查长度
            if (password.length >= 8) strength++;
            // 检查是否包含数字
            if (/\d/.test(password)) strength++;
            // 检查是否包含小写字母
            if (/[a-z]/.test(password)) strength++;
            // 检查是否包含大写字母
            if (/[A-Z]/.test(password)) strength++;
            // 检查是否包含特殊字符
            if (/[^A-Za-z0-9]/.test(password)) strength++;

            var strengthBar = this.parentElement.querySelector('.password-strength');
            if (strengthBar) {
                strengthBar.style.width = (strength * 20) + '%';
                
                if (strength <= 2) {
                    strengthBar.className = 'progress-bar bg-danger';
                    strengthBar.textContent = '弱';
                } else if (strength <= 3) {
                    strengthBar.className = 'progress-bar bg-warning';
                    strengthBar.textContent = '中';
                } else {
                    strengthBar.className = 'progress-bar bg-success';
                    strengthBar.textContent = '强';
                }
            }
        });
    });

    // 图片加载失败处理
    var images = document.querySelectorAll('img');
    images.forEach(function(img) {
        img.addEventListener('error', function() {
            this.src = '/static/images/default-city.jpg';
        });
    });
});
