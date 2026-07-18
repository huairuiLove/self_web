from __future__ import annotations

import json
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from typing import Callable

import customtkinter as ctk

from function_search.config import AppConfig
from function_search.lm_studio_client import LMStudioError
from function_search.models import FunctionEntry, SearchResult
from function_search.paths import default_db_path, user_data_dir
from function_search.qa_assistant import QAAssistant
from function_search.search_engine import SearchEngine

PROVIDER_LABELS = {
    "all": "全部",
    "pytorch": "PyTorch",
    "python": "Python 常用",
    "backend": "Python 后端",
}


class FunctionSearchApp(ctk.CTk):
    def __init__(self, db_path: Path | None = None) -> None:
        super().__init__()
        self.title("Function Search - API 快速查询")
        self.geometry("1180x760")
        self.minsize(960, 640)

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self._db_path = db_path or default_db_path()
        self._engine = SearchEngine(self._db_path)
        self._engine.connect()

        self._provider_filter = "all"
        self._results: list[SearchResult] = []
        self._selected_index = 0
        self._debounce_id: str | None = None
        self._qa_config = AppConfig.load()
        self._qa_assistant = QAAssistant(self._engine, self._qa_config)
        self._qa_busy = False

        self._build_ui()
        self._run_search("")
        self._refresh_qa_status()

        self.bind("<Command-q>", lambda _e: self.destroy())
        self.bind("<Control-q>", lambda _e: self.destroy())

    def _build_ui(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 8))
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text="Function Search",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w")

        stats = ctk.CTkLabel(
            header,
            text=f"已索引 {self._engine.entry_count} 个 API",
            text_color="gray",
        )
        stats.grid(row=0, column=1, sticky="e")

        search_row = ctk.CTkFrame(self, fg_color="transparent")
        search_row.grid(row=0, column=0, sticky="ew", padx=16, pady=(48, 8))
        search_row.grid_columnconfigure(0, weight=1)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search_changed)

        self.search_entry = ctk.CTkEntry(
            search_row,
            textvariable=self.search_var,
            placeholder_text="输入函数名、模块或关键词，如 torch.nn.Linear / json.dumps / FastAPI",
            height=42,
            font=ctk.CTkFont(size=15),
        )
        self.search_entry.grid(row=0, column=0, sticky="ew")
        self.search_entry.focus_set()

        self.tabs = ctk.CTkTabview(self)
        self.tabs.grid(row=1, column=0, sticky="nsew", padx=16, pady=12)
        self.tabs.add("API 搜索")
        self.tabs.add("AI 问答")

        search_tab = self.tabs.tab("API 搜索")
        search_tab.grid_columnconfigure(0, weight=1)
        search_tab.grid_rowconfigure(1, weight=1)

        filter_row = ctk.CTkFrame(search_tab, fg_color="transparent")
        filter_row.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        self._filter_buttons: dict[str, ctk.CTkButton] = {}
        available = {"all": "全部"}
        for provider in self._engine.providers:
            available[provider] = PROVIDER_LABELS.get(provider, provider)

        col = 0
        for key, label in available.items():
            btn = ctk.CTkButton(
                filter_row,
                text=label,
                width=110,
                command=lambda k=key: self._set_provider_filter(k),
            )
            btn.grid(row=0, column=col, padx=(0, 8))
            self._filter_buttons[key] = btn
            col += 1
        self._highlight_filter_button("all")

        body = ctk.CTkFrame(search_tab)
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_columnconfigure(0, weight=2)
        body.grid_columnconfigure(1, weight=3)
        body.grid_rowconfigure(0, weight=1)

        self._build_qa_tab(self.tabs.tab("AI 问答"))

        left = ctk.CTkFrame(body)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left.grid_rowconfigure(1, weight=1)
        left.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(left, text="搜索结果", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, sticky="w", padx=12, pady=(10, 4)
        )

        self.result_list = tk.Listbox(
            left,
            activestyle="none",
            exportselection=False,
            font=("Menlo", 12),
            bg="#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#f7f7f7",
            fg="#ffffff" if ctk.get_appearance_mode() == "Dark" else "#111111",
            selectbackground="#1f6aa5",
            borderwidth=0,
            highlightthickness=0,
        )
        self.result_list.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.result_list.bind("<<ListboxSelect>>", self._on_result_select)
        self.result_list.bind("<Up>", self._on_list_key)
        self.result_list.bind("<Down>", self._on_list_key)
        self.result_list.bind("<Return>", self._on_copy_example)

        right = ctk.CTkFrame(body)
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_rowconfigure(4, weight=1)
        right.grid_columnconfigure(0, weight=1)

        self.name_label = ctk.CTkLabel(
            right,
            text="选择一个函数查看详情",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w",
        )
        self.name_label.grid(row=0, column=0, sticky="ew", padx=14, pady=(12, 4))

        self.meta_label = ctk.CTkLabel(
            right,
            text="",
            text_color="gray",
            anchor="w",
            justify="left",
        )
        self.meta_label.grid(row=1, column=0, sticky="ew", padx=14)

        ctk.CTkLabel(right, text="函数说明", font=ctk.CTkFont(weight="bold")).grid(
            row=2, column=0, sticky="w", padx=14, pady=(10, 4)
        )
        self.desc_box = ctk.CTkTextbox(right, height=140, wrap="word")
        self.desc_box.grid(row=3, column=0, sticky="ew", padx=14)
        self.desc_box.configure(state="disabled")

        example_header = ctk.CTkFrame(right, fg_color="transparent")
        example_header.grid(row=4, column=0, sticky="ew", padx=14, pady=(10, 4))
        example_header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(example_header, text="调用示例", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, sticky="w"
        )
        self.copy_btn = ctk.CTkButton(
            example_header,
            text="复制示例",
            width=100,
            command=self._copy_example,
        )
        self.copy_btn.grid(row=0, column=1, sticky="e")

        self.example_box = ctk.CTkTextbox(right, wrap="none", font=ctk.CTkFont(family="Menlo", size=13))
        self.example_box.grid(row=5, column=0, sticky="nsew", padx=14, pady=(0, 12))
        self.example_box.configure(state="disabled")

        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 12))
        ctk.CTkLabel(
            footer,
            text="快捷键: ↑↓ 选择 · Enter 复制示例 · Tab 切换 AI 问答 · 支持模糊搜索与分类过滤",
            text_color="gray",
        ).pack(side="left")

    def _build_qa_tab(self, parent: ctk.CTkFrame) -> None:
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(2, weight=1)

        status_row = ctk.CTkFrame(parent, fg_color="transparent")
        status_row.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        status_row.grid_columnconfigure(0, weight=1)

        self.qa_status_label = ctk.CTkLabel(
            status_row,
            text="正在检测 LM Studio...",
            text_color="gray",
            anchor="w",
        )
        self.qa_status_label.grid(row=0, column=0, sticky="w")

        self.qa_refresh_btn = ctk.CTkButton(
            status_row,
            text="刷新连接",
            width=90,
            command=self._refresh_qa_status,
        )
        self.qa_refresh_btn.grid(row=0, column=1, padx=(8, 0))

        ask_row = ctk.CTkFrame(parent, fg_color="transparent")
        ask_row.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        ask_row.grid_columnconfigure(0, weight=1)

        self.qa_question_var = tk.StringVar()
        self.qa_question_entry = ctk.CTkEntry(
            ask_row,
            textvariable=self.qa_question_var,
            placeholder_text="提问，如：如何用 torch 定义两层全连接网络？json 和 orjson 怎么选？",
            height=42,
            font=ctk.CTkFont(size=15),
        )
        self.qa_question_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.qa_question_entry.bind("<Return>", self._on_ask_question)

        self.qa_ask_btn = ctk.CTkButton(
            ask_row,
            text="提问",
            width=90,
            command=self._on_ask_question,
        )
        self.qa_ask_btn.grid(row=0, column=1)

        qa_body = ctk.CTkFrame(parent)
        qa_body.grid(row=2, column=0, sticky="nsew")
        qa_body.grid_columnconfigure(0, weight=1)
        qa_body.grid_columnconfigure(1, weight=2)
        qa_body.grid_rowconfigure(0, weight=1)

        context_panel = ctk.CTkFrame(qa_body)
        context_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        context_panel.grid_rowconfigure(1, weight=1)
        context_panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            context_panel,
            text="检索上下文",
            font=ctk.CTkFont(weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=12, pady=(10, 4))

        self.qa_context_box = ctk.CTkTextbox(
            context_panel,
            wrap="word",
            font=ctk.CTkFont(family="Menlo", size=12),
        )
        self.qa_context_box.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.qa_context_box.configure(state="disabled")

        answer_panel = ctk.CTkFrame(qa_body)
        answer_panel.grid(row=0, column=1, sticky="nsew")
        answer_panel.grid_rowconfigure(1, weight=1)
        answer_panel.grid_columnconfigure(0, weight=1)

        answer_header = ctk.CTkFrame(answer_panel, fg_color="transparent")
        answer_header.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 4))
        answer_header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            answer_header,
            text="AI 回答",
            font=ctk.CTkFont(weight="bold"),
        ).grid(row=0, column=0, sticky="w")

        self.qa_copy_btn = ctk.CTkButton(
            answer_header,
            text="复制回答",
            width=90,
            command=self._copy_qa_answer,
        )
        self.qa_copy_btn.grid(row=0, column=1, sticky="e")

        self.qa_answer_box = ctk.CTkTextbox(
            answer_panel,
            wrap="word",
            font=ctk.CTkFont(size=14),
        )
        self.qa_answer_box.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.qa_answer_box.configure(state="disabled")

    def _refresh_qa_status(self) -> None:
        def check() -> None:
            available = self._qa_assistant.is_available()
            model = self._qa_config.model or "（使用 LM Studio 当前加载模型）"
            if available:
                text = f"LM Studio 已连接 · 模型: {model}"
                color = "#2fa572"
            else:
                text = (
                    "LM Studio 未连接 · 请启动本地服务器并加载 GLM-4-32B 模型 "
                    f"({self._qa_config.lm_studio_url})"
                )
                color = "#c0392b"
            self.after(0, lambda: self.qa_status_label.configure(text=text, text_color=color))

        threading.Thread(target=check, daemon=True).start()

    def _on_ask_question(self, _event=None) -> None:
        if self._qa_busy:
            return
        question = self.qa_question_var.get().strip()
        if not question:
            messagebox.showinfo("提示", "请输入问题")
            return

        self._qa_busy = True
        self.qa_ask_btn.configure(state="disabled", text="思考中...")
        self._set_text(self.qa_answer_box, "正在检索相关 API 并请求 LM Studio...")
        self._set_text(self.qa_context_box, "")

        provider = None if self._provider_filter == "all" else self._provider_filter

        def worker() -> None:
            try:
                context_text, _results = self._qa_assistant.build_context(
                    question,
                    provider=provider,
                )
                self.after(0, lambda: self._set_text(self.qa_context_box, context_text))
                result = self._qa_assistant.answer(question, provider=provider)
                self.after(0, lambda: self._finish_qa_answer(result.answer))
            except LMStudioError as exc:
                self.after(0, lambda: self._finish_qa_error(str(exc)))
            except Exception as exc:  # noqa: BLE001
                self.after(0, lambda: self._finish_qa_error(f"问答失败: {exc}"))

        threading.Thread(target=worker, daemon=True).start()

    def _finish_qa_answer(self, answer: str) -> None:
        self._set_text(self.qa_answer_box, answer)
        self._qa_busy = False
        self.qa_ask_btn.configure(state="normal", text="提问")

    def _finish_qa_error(self, message: str) -> None:
        self._set_text(self.qa_answer_box, message)
        self._qa_busy = False
        self.qa_ask_btn.configure(state="normal", text="提问")
        self._refresh_qa_status()

    def _copy_qa_answer(self) -> None:
        content = self.qa_answer_box.get("1.0", tk.END).strip()
        if not content:
            messagebox.showinfo("提示", "当前没有可复制内容")
            return
        self.clipboard_clear()
        self.clipboard_append(content)
        self.qa_status_label.configure(text="已复制 AI 回答", text_color="#2fa572")
        self.after(1500, self._refresh_qa_status)

    def _set_provider_filter(self, provider_key: str) -> None:
        self._provider_filter = provider_key
        self._highlight_filter_button(provider_key)
        self._run_search(self.search_var.get())

    def _highlight_filter_button(self, active: str) -> None:
        for key, btn in self._filter_buttons.items():
            if key == active:
                btn.configure(fg_color="#1f6aa5")
            else:
                btn.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])

    def _on_search_changed(self, *_args) -> None:
        if self._debounce_id is not None:
            self.after_cancel(self._debounce_id)
        self._debounce_id = self.after(80, self._debounced_search)

    def _debounced_search(self) -> None:
        self._debounce_id = None
        self._run_search(self.search_var.get())

    def _run_search(self, query: str) -> None:
        provider = None if self._provider_filter == "all" else self._provider_filter
        self._results = self._engine.search(query, provider=provider, limit=80)
        self._render_results()
        if self._results:
            self._select_result(0)
        else:
            self._clear_detail()

    def _render_results(self) -> None:
        self.result_list.delete(0, tk.END)
        for result in self._results:
            entry = result.entry
            provider = PROVIDER_LABELS.get(entry.provider, entry.provider)
            score_hint = "" if result.score < 1 else f"  ·  {int(result.score)}"
            line = f"[{provider}] {entry.full_name}{score_hint}"
            self.result_list.insert(tk.END, line)

    def _on_result_select(self, _event=None) -> None:
        selection = self.result_list.curselection()
        if selection:
            self._select_result(selection[0])

    def _on_list_key(self, event) -> str | None:
        self.after(10, self._sync_selection_from_list)
        return None

    def _sync_selection_from_list(self) -> None:
        selection = self.result_list.curselection()
        if selection:
            self._select_result(selection[0], update_list=False)

    def _select_result(self, index: int, *, update_list: bool = True) -> None:
        if index < 0 or index >= len(self._results):
            return
        self._selected_index = index
        if update_list:
            self.result_list.selection_clear(0, tk.END)
            self.result_list.selection_set(index)
            self.result_list.see(index)
        self._show_detail(self._results[index].entry)

    def _show_detail(self, entry: FunctionEntry) -> None:
        self.name_label.configure(text=entry.full_name)
        provider = PROVIDER_LABELS.get(entry.provider, entry.provider)
        tags = ", ".join(entry.tags) if entry.tags else "-"
        meta = f"来源: {provider}  ·  分类: {entry.category}  ·  模块: {entry.module or '-'}\n签名: {entry.signature}\n标签: {tags}"
        self.meta_label.configure(text=meta)

        self._set_text(self.desc_box, entry.description or "（暂无文档说明）")
        self._set_text(self.example_box, entry.example or "# 暂无示例")

    def _clear_detail(self) -> None:
        self.name_label.configure(text="未找到匹配结果")
        self.meta_label.configure(text="尝试更短关键词、拼音缩写或模块名")
        self._set_text(self.desc_box, "")
        self._set_text(self.example_box, "")

    @staticmethod
    def _set_text(widget: ctk.CTkTextbox, content: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert("1.0", content)
        widget.configure(state="disabled")

    def _copy_example(self) -> None:
        if not self._results:
            return
        entry = self._results[self._selected_index].entry
        text = entry.example.strip()
        if not text:
            messagebox.showinfo("提示", "当前条目没有可复制示例")
            return
        self.clipboard_clear()
        self.clipboard_append(text)
        self._flash_status(f"已复制: {entry.full_name}")

    def _on_copy_example(self, _event=None) -> None:
        self._copy_example()

    def _flash_status(self, message: str) -> None:
        original = self.meta_label.cget("text")
        self.meta_label.configure(text=message)
        self.after(1500, lambda: self.meta_label.configure(text=original))


def load_extension_providers(extensions_dir: Path) -> list:
    from function_search.extensions_loader import load_extension_providers as _load

    return _load(extensions_dir)


def run_app(db_path: Path | None = None) -> None:
    try:
        import tkinter as tk  # noqa: F401
    except ModuleNotFoundError as exc:
        print(
            "GUI requires tkinter. On macOS: brew install python-tk@3.14",
            file=__import__("sys").stderr,
        )
        raise SystemExit(1) from exc

    from tkinter import messagebox

    if db_path is None:
        db_path = default_db_path()
    if not db_path.exists():
        messagebox.showerror(
            "索引缺失",
            f"未找到搜索索引:\n{db_path}\n\n请先运行: python -m function_search.build_index",
        )
        return

    app = FunctionSearchApp(db_path=db_path)
    app.mainloop()
