document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('todo-form');
  const input = document.getElementById('todo-input');
  const typeSelect = document.getElementById('todo-type');
  const columns = document.getElementById('todo-columns');
  const stats = document.getElementById('todo-stats');

  // 分类列表
  const categories = ['美食', '娱乐', '旅游地点', '学习', '其他'];

  // 加载本地存储任务
  let todos = JSON.parse(localStorage.getItem('todos') || '[]');
  renderTodos();

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    const value = input.value.trim();
    const type = typeSelect.value;
    if (value && type) {
      const todo = {
        text: value,
        type: type,
        created: new Date().toLocaleDateString(),
        completed: false
      };
      todos.push(todo);
      localStorage.setItem('todos', JSON.stringify(todos));
      renderTodos();
      input.value = '';
      typeSelect.value = '';
    }
  });

  function renderTodos() {
    columns.innerHTML = '';
    let completedCount = 0;
    let totalCount = todos.length;
    let uncompletedCount = 0;
    // 进度条
    const progressBar = document.getElementById('todo-progress-bar');
    const progressInner = document.getElementById('todo-progress-inner');
    // 按分类分组
    categories.forEach(cat => {
      const catTodos = todos.map((todo, idx) => ({...todo, idx})).filter(todo => todo.type === cat);
      const col = document.createElement('div');
      col.className = 'todo-column';
      const colTitle = document.createElement('div');
      colTitle.className = 'todo-column-title';
      colTitle.textContent = cat;
      col.appendChild(colTitle);
      const ul = document.createElement('ul');
      ul.className = 'todo-list';
      catTodos.forEach(todo => {
        const li = document.createElement('li');
        li.className = todo.completed ? 'completed' : '';
        // 内容
        const info = document.createElement('span');
        info.innerHTML = `${todo.text} <small style='color:#888;'>${todo.created}</small>`;
        li.appendChild(info);
        // 勾选框
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = !!todo.completed;
        checkbox.style.margin = '0 8px 0 16px';
        checkbox.onchange = function() {
          todos[todo.idx].completed = checkbox.checked;
          localStorage.setItem('todos', JSON.stringify(todos));
          renderTodos();
        };
        li.appendChild(checkbox);
        // 删除按钮
        const delBtn = document.createElement('button');
        delBtn.textContent = '删除';
        delBtn.className = 'delete-btn';
        delBtn.onclick = function() {
          todos.splice(todo.idx, 1);
          localStorage.setItem('todos', JSON.stringify(todos));
          renderTodos();
        };
        li.appendChild(delBtn);
        ul.appendChild(li);
        if (todo.completed) completedCount++;
      });
      col.appendChild(ul);
      columns.appendChild(col);
    });
    uncompletedCount = totalCount - completedCount;
    // 进度条显示
    let percent = totalCount === 0 ? 0 : Math.round((completedCount / totalCount) * 100);
    progressInner.style.width = percent + '%';
    progressInner.textContent = percent + '%';
    stats.innerHTML = `总数：${totalCount}，已完成：${completedCount}，未完成：${uncompletedCount}`;
  }
});