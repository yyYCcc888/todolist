import streamlit as st
import datetime
import json
import os
import pandas as pd

st.set_page_config(page_title="YC & PP's To-Do List", page_icon="💗", layout="wide")

CATEGORY_LIST = ["美食", "娱乐", "旅游", "学习", "其他"]
DATA_FILE = "todo_data.json"

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def add_task(tasks, content, category):
    task = {
        "content": content,
        "category": category,
        "date": datetime.date.today().isoformat(),
        "completed": False
    }
    tasks.append(task)
    save_tasks(tasks)

def delete_task(tasks, idx):
    tasks.pop(idx)
    save_tasks(tasks)

def toggle_complete(tasks, idx):
    tasks[idx]["completed"] = not tasks[idx]["completed"]
    save_tasks(tasks)

def get_stats(tasks):
    total = len(tasks)
    completed = sum(1 for t in tasks if t["completed"])
    return total, completed, total - completed

def main():
    tasks = load_tasks()
    total, completed, incomplete = get_stats(tasks)
    st.markdown(f"**总任务数：** {total}  ")
    st.progress(completed / total if total else 0, text=f"已完成 {completed} / {total}")
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
        body {
            background: #ffe6f2 !important;
        }
        .pixel-title {
            font-family: 'Press Start 2P', cursive;
            color: #ff69b4;
            text-shadow: 2px 2px 0 #fff, 4px 4px 0 #b7e0fc;
            font-size: 2.2rem;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        .add-row {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.2rem;
        }
        .add-row .stTextInput, .add-row .stSelectbox, .add-row .stFormSubmitButton {
            margin-bottom: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<div class='pixel-title'>YC & PP's To-Do List</div>", unsafe_allow_html=True)
    # 导出为xlsx
    df = pd.DataFrame(tasks)
    import io
    output = io.BytesIO()
    df.to_excel(output, index=False, engine="openpyxl")
    output.seek(0)
    st.download_button(
        label="导出清单",
        data=output,
        file_name="todo_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="export_btn",
        help="导出所有任务为XLSX",
        use_container_width=False,
        disabled=False,
        on_click=None,
        args=None,
        kwargs=None,
        type="primary"
    )
    with st.form("add_task_form", clear_on_submit=True):
        cols = st.columns([2,4,1])
        with cols[0]:
            category = st.selectbox("分类", CATEGORY_LIST, key="task_category")
        with cols[1]:
            content = st.text_input("任务内容", key="task_content")
        with cols[2]:
            submitted = st.form_submit_button("添加", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        if submitted and content.strip():
            add_task(tasks, content.strip(), category)
            st.rerun()
    st.divider()
    columns = st.columns(len(CATEGORY_LIST))
    for i, cat in enumerate(CATEGORY_LIST):
        with columns[i]:
            st.markdown(f"### {cat}")
            for idx, task in enumerate([t for t in tasks if t["category"] == cat]):
                t_idx = tasks.index(task)
                checked = st.checkbox(f"{task['content']} ({task['date']})", value=task["completed"], key=f"{cat}_{t_idx}", on_change=toggle_complete, args=(tasks, t_idx))
                st.button("删除", key=f"del_{cat}_{t_idx}", on_click=delete_task, args=(tasks, t_idx))
    st.markdown(
        """
        <style>
        body {
            background: #ffe4ec !important;
        }
        .stApp {
            background: #ffe4ec !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # 统计任务完成进度
    if not isinstance(tasks, dict) or tasks is None:
        total_tasks = 0
        completed_tasks = 0
        percent = 0
    else:
        total_tasks = sum(len(ts) for ts in tasks.values() if isinstance(ts, list))
        completed_tasks = sum(task["completed"] for ts in tasks.values() if isinstance(ts, list) for task in ts)
        percent = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

if __name__ == "__main__":
    main()
