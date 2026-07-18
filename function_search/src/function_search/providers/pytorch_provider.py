from __future__ import annotations

import importlib
import inspect
import pkgutil
import re
from typing import Any

from function_search.models import FunctionEntry
from function_search.providers.base import Provider

# Top-level torch submodules to index (keeps index focused and build time reasonable)
TORCH_ROOT_MODULES = (
    "torch",
    "torch.nn",
    "torch.nn.functional",
    "torch.optim",
    "torch.utils.data",
    "torch.autograd",
    "torch.distributions",
    "torch.fft",
    "torch.linalg",
    "torch.special",
    "torch.cuda",
    "torch.backends",
    "torch.jit",
    "torch.onnx",
    "torch.hub",
    "torch.serialization",
    "torch.random",
    "torch.sparse",
    "torch.testing",
)

SKIP_NAME_PREFIXES = ("_", "test_", "TEST_")
SKIP_MODULES = {
    "torch.utils.bottleneck",
    "torch.utils.benchmark",
    "torch.utils.mobile_optimizer",
}


def _is_public(name: str) -> bool:
    return not any(name.startswith(p) for p in SKIP_NAME_PREFIXES)


def _clean_doc(doc: str | None, max_len: int = 600) -> str:
    if doc is None:
        return ""
    if not isinstance(doc, str):
        return ""
    text = inspect.cleandoc(doc)
    text = re.sub(r"\n{3,}", "\n\n", text)
    if len(text) > max_len:
        text = text[: max_len - 3].rstrip() + "..."
    return text


def _format_signature(obj: Any, full_name: str) -> str:
    try:
        sig = inspect.signature(obj)
        return f"{full_name}{sig}"
    except (TypeError, ValueError):
        return full_name


def _make_example(full_name: str, signature: str, category: str) -> str:
    if category == "class":
        short = full_name.split(".")[-1]
        return f"model = {full_name}()\n# or\ninstance = {short}()"
    if "(" in signature:
        args = signature[signature.index("(") :]
        return f"result = {full_name}{args}"
    return f"result = {full_name}()"


def _entry_id(provider: str, full_name: str) -> str:
    return f"{provider}:{full_name}"


def _category_for(obj: Any) -> str:
    if inspect.isclass(obj):
        return "class"
    if inspect.isfunction(obj) or inspect.isbuiltin(obj):
        return "function"
    if isinstance(obj, type):
        return "class"
    return "api"


class PyTorchProvider(Provider):
    """Extracts public PyTorch APIs via runtime introspection."""

    @property
    def id(self) -> str:
        return "pytorch"

    @property
    def display_name(self) -> str:
        return "PyTorch"

    def collect(self) -> list[FunctionEntry]:
        try:
            import torch  # noqa: F401
        except ImportError as exc:
            raise RuntimeError(
                "PyTorch is required to build the PyTorch index. "
                "Install with: pip install torch"
            ) from exc

        entries: list[FunctionEntry] = []
        seen: set[str] = set()

        for module_name in TORCH_ROOT_MODULES:
            if module_name in SKIP_MODULES:
                continue
            try:
                module = importlib.import_module(module_name)
            except Exception:
                continue
            self._walk_module(module, module_name, entries, seen)
            for sub in self._iter_public_submodules(module, module_name):
                if sub in SKIP_MODULES:
                    continue
                try:
                    sub_mod = importlib.import_module(sub)
                except Exception:
                    continue
                self._walk_module(sub_mod, sub, entries, seen)

        entries.sort(key=lambda e: e.full_name)
        return entries

    def _iter_public_submodules(self, module: Any, root: str) -> list[str]:
        if not hasattr(module, "__path__"):
            return []
        names: list[str] = []
        prefix = root + "."
        for info in pkgutil.iter_modules(module.__path__, prefix):
            if info.ispkg or info.name.count(".") - root.count(".") <= 2:
                names.append(info.name)
        return names

    def _walk_module(
        self,
        module: Any,
        module_name: str,
        entries: list[FunctionEntry],
        seen: set[str],
    ) -> None:
        for name, obj in inspect.getmembers(module):
            if not _is_public(name):
                continue
            if getattr(obj, "__module__", None) and not str(
                getattr(obj, "__module__", "")
            ).startswith("torch"):
                continue

            if inspect.ismodule(obj):
                continue

            if not (inspect.isfunction(obj) or inspect.isclass(obj) or inspect.isbuiltin(obj)):
                if not (callable(obj) and hasattr(obj, "__name__")):
                    continue
                # Skip descriptors/properties that are not plain callables
                if isinstance(obj, (property, classmethod, staticmethod)):
                    continue

            full_name = f"{module_name}.{name}"
            if full_name in seen:
                continue
            seen.add(full_name)

            category = _category_for(obj)
            signature = _format_signature(obj, full_name)
            try:
                raw_doc = getattr(obj, "__doc__", None)
            except Exception:
                raw_doc = None
            description = _clean_doc(raw_doc)
            example = _make_example(full_name, signature, category)
            tags = self._infer_tags(module_name, name, category)

            entries.append(
                FunctionEntry(
                    id=_entry_id(self.id, full_name),
                    provider=self.id,
                    category=category,
                    name=name,
                    full_name=full_name,
                    signature=signature,
                    description=description,
                    example=example,
                    module=module_name,
                    tags=tags,
                )
            )

    @staticmethod
    def _infer_tags(module_name: str, name: str, category: str) -> list[str]:
        tags = [category, "pytorch"]
        parts = module_name.split(".")
        if len(parts) >= 2:
            tags.append(parts[1])
        if "functional" in module_name:
            tags.append("functional")
        if "optim" in module_name:
            tags.append("optimizer")
        if "cuda" in module_name:
            tags.append("gpu")
        if name.endswith("Loss"):
            tags.append("loss")
        if name.endswith("Dataset") or name.endswith("DataLoader"):
            tags.append("data")
        return tags
