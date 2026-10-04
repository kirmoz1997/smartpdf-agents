#!/usr/bin/env python3
"""SmartPDF из командной строки: загрузка → операция → ожидание → скачивание (REST API).

  python3 smartpdf.py compress report.pdf -p level=high
  python3 smartpdf.py merge a.pdf b.pdf c.pdf -o out/
  python3 smartpdf.py ocr scan.pdf -p 'languages=["rus","eng"]'
  python3 smartpdf.py watermark doc.pdf --upload image_file_id=logo.png -p opacity=0.3
  python3 smartpdf.py sign doc.pdf --data-uri signature_data=signature.png -p page=2
  python3 smartpdf.py compress report.pdf --link     # ссылка на результат вместо скачивания
  python3 smartpdf.py balance                         # баланс API и цена запроса
  python3 smartpdf.py operations                      # операции и их параметры

Ключ — переменная окружения SMARTPDF_API_KEY (личный кабинет: https://smartpdf.ru/dashboard/api-keys).
Каждая операция — платный запрос с баланса API. Документация: https://dev.smartpdf.ru/docs

Только стандартная библиотека Python 3.8+. В stdout — путь к сохранённому файлу (или ссылка с --link),
ход работы и ошибки — в stderr. Коды выхода: 0 — готово, 1 — ошибка API или сети, 2 — неверный вызов,
3 — файл не удалось обработать (оплата вернулась на баланс).
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

API_URL = os.environ.get("SMARTPDF_API_URL", "https://api.smartpdf.ru").rstrip("/")
DASHBOARD_URL = "https://smartpdf.ru/dashboard/api-keys"
USER_AGENT = "smartpdf-skill/1.0 (+https://dev.smartpdf.ru)"
POLL_SECONDS = 2
STATUS_TEXT = {"pending": "в очереди", "processing": "обрабатывается"}
WAIT_LIMIT_SECONDS = 20 * 60

# --- operations: генерирует frontend/scripts/build-agents.ts из operations.json — не править вручную ---
OPERATIONS: dict[str, dict] = {
    "word-to-pdf": {"title":"Word в PDF","endpoint":"/pdf/word-to-pdf","mcp":"word_to_pdf","files":"one","params":{"webhook_url":"string"},"required":[]},
    "jpg-to-pdf": {"title":"JPG в PDF","endpoint":"/pdf/jpg-to-pdf","mcp":"jpg_to_pdf","files":"many","params":{"order":"integer[]","fit":"string","webhook_url":"string"},"required":[]},
    "xlsx-to-pdf": {"title":"Excel в PDF","endpoint":"/pdf/xlsx-to-pdf","mcp":"xlsx_to_pdf","files":"one","params":{"webhook_url":"string"},"required":[]},
    "pptx-to-pdf": {"title":"PowerPoint в PDF","endpoint":"/pdf/pptx-to-pdf","mcp":"pptx_to_pdf","files":"one","params":{"webhook_url":"string"},"required":[]},
    "html-to-pdf": {"title":"HTML в PDF","endpoint":"/pdf/html-to-pdf","mcp":"html_to_pdf","files":"one","params":{"page_size":"string","orientation":"string","margin":"string","webhook_url":"string"},"required":[]},
    "pdf-to-word": {"title":"PDF в Word","endpoint":"/pdf/to-word","mcp":"pdf_to_word","files":"one","params":{"webhook_url":"string"},"required":[]},
    "pdf-to-jpg": {"title":"PDF в JPG","endpoint":"/pdf/to-jpg","mcp":"pdf_to_jpg","files":"one","params":{"dpi":"integer","pages":"integer[]","webhook_url":"string"},"required":[]},
    "pdf-to-excel": {"title":"PDF в Excel","endpoint":"/pdf/to-excel","mcp":"pdf_to_excel","files":"one","params":{"layout":"string","webhook_url":"string"},"required":[]},
    "pdf-to-pptx": {"title":"PDF в PowerPoint","endpoint":"/pdf/to-pptx","mcp":"pdf_to_pptx","files":"one","params":{"webhook_url":"string"},"required":[]},
    "pdf-to-txt": {"title":"PDF в текст","endpoint":"/pdf/to-txt","mcp":"pdf_to_txt","files":"one","params":{"mode":"string","webhook_url":"string"},"required":[]},
    "compress": {"title":"Сжать PDF","endpoint":"/pdf/compress","mcp":"compress_pdf","files":"one","params":{"level":"string","webhook_url":"string"},"required":[]},
    "merge": {"title":"Объединить PDF","endpoint":"/pdf/merge","mcp":"merge_pdfs","files":"many","params":{"order":"integer[]","webhook_url":"string"},"required":[]},
    "split": {"title":"Разделить PDF","endpoint":"/pdf/split","mcp":"split_pdf","files":"one","params":{"mode":"string","ranges":"[integer, integer][]","webhook_url":"string"},"required":[]},
    "ocr": {"title":"Распознать текст","endpoint":"/pdf/ocr","mcp":"ocr_pdf","files":"one","params":{"languages":"string[]","webhook_url":"string"},"required":[]},
    "flatten": {"title":"Сгладить PDF","endpoint":"/pdf/flatten","mcp":"flatten_pdf","files":"one","params":{"webhook_url":"string"},"required":[]},
    "delete-pages": {"title":"Удалить страницы","endpoint":"/pdf/delete-pages","mcp":"delete_pages","files":"one","params":{"pages":"integer[]","webhook_url":"string"},"required":["pages"]},
    "extract-pages": {"title":"Извлечь страницы","endpoint":"/pdf/extract-pages","mcp":"extract_pages","files":"one","params":{"pages":"integer[]","webhook_url":"string"},"required":["pages"]},
    "rotate": {"title":"Повернуть страницы","endpoint":"/pdf/rotate","mcp":"rotate_pdf","files":"one","params":{"pages":"integer[] | \"all\"","angle":"integer","webhook_url":"string"},"required":[]},
    "reorder-pages": {"title":"Порядок страниц","endpoint":"/pdf/reorder-pages","mcp":"reorder_pages","files":"one","params":{"new_order":"integer[]","webhook_url":"string"},"required":["new_order"]},
    "add-page-numbers": {"title":"Нумерация страниц","endpoint":"/pdf/add-page-numbers","mcp":"add_page_numbers","files":"one","params":{"position":"string","start_from":"integer","prefix":"string","font_size":"integer","pages":"integer[] | \"all\"","webhook_url":"string"},"required":[]},
    "sign": {"title":"Подписать PDF","endpoint":"/pdf/sign","mcp":"sign_pdf","files":"one","params":{"signature_data":"string","page":"integer","x":"number","y":"number","width":"number","height":"number","webhook_url":"string"},"required":["signature_data"]},
    "protect": {"title":"Защитить паролем","endpoint":"/pdf/protect","mcp":"protect_pdf","files":"one","params":{"user_password":"string","owner_password":"string","webhook_url":"string"},"required":["user_password"]},
    "unlock": {"title":"Снять пароль","endpoint":"/pdf/unlock","mcp":"unlock_pdf","files":"one","params":{"password":"string","webhook_url":"string"},"required":["password"]},
    "watermark": {"title":"Водяной знак","endpoint":"/pdf/watermark","mcp":"watermark_pdf","files":"one","params":{"text":"string","image_file_id":"string","font_size":"integer","color":"string","opacity":"number","angle":"number","position":"string","pages":"integer[] | \"all\"","scale":"number","webhook_url":"string"},"required":[]},
}
# --- end operations ---


class ApiError(Exception):
    """Ответ API с ошибкой (status 0 — нет связи)."""

    def __init__(self, status: int, detail: str):
        super().__init__(detail)
        self.status = status
        self.detail = detail


class ProcessingFailed(Exception):
    """Файл принят, но обработать его не удалось: задача в статусе failed."""


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def _detail(body: bytes) -> str:
    try:
        data = json.loads(body)
    except ValueError:
        return body.decode("utf-8", "replace").strip()[:300] or "без описания"
    detail = data.get("detail") if isinstance(data, dict) else None
    if isinstance(detail, list):  # 422: ошибки по полям
        parts = []
        for item in detail:
            loc = ".".join(str(x) for x in item.get("loc", [])[1:])
            parts.append(f"{loc}: {item.get('msg')}" if loc else str(item.get("msg")))
        return "; ".join(parts)
    return str(detail if detail is not None else data)


class _MultipartFile:
    """Тело multipart/form-data с одним файлом: читается кусками, файл целиком в память не грузится."""

    def __init__(self, path: Path):
        self.boundary = uuid.uuid4().hex
        name = path.name.replace("\\", "_").replace('"', "_")
        ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self._head = (
            f"--{self.boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{name}"\r\n'
            f"Content-Type: {ctype}\r\n\r\n"
        ).encode("utf-8")
        self._tail = f"\r\n--{self.boundary}--\r\n".encode()
        self.length = len(self._head) + path.stat().st_size + len(self._tail)
        self._parts = [self._head, path, self._tail]
        self._file = None

    def read(self, size: int = -1) -> bytes:
        while self._parts:
            part = self._parts[0]
            if isinstance(part, bytes):
                self._parts.pop(0)
                return part
            if self._file is None:
                self._file = open(part, "rb")
            chunk = self._file.read(size if size and size > 0 else 1 << 20)
            if chunk:
                return chunk
            self._file.close()
            self._file = None
            self._parts.pop(0)
        return b""


def _api_key() -> str:
    key = os.environ.get("SMARTPDF_API_KEY", "").strip()
    if not key:
        raise SystemExit(
            "Нет ключа: задайте переменную окружения SMARTPDF_API_KEY (export SMARTPDF_API_KEY=sk_live_…).\n"
            f"Ключ создаётся в личном кабинете: {DASHBOARD_URL}. Не вставляйте ключ в чат и в файлы проекта."
        )
    return key


def request(method: str, path: str, *, body=None, upload: Path | None = None, timeout: int = 60):
    """Запрос к API с ключом. 429 — ждём Retry-After и повторяем; обрыв связи у GET — повторяем."""
    url = f"{API_URL}/v1{path}"
    for attempt in range(4):
        headers = {"X-API-Key": _api_key(), "User-Agent": USER_AGENT, "X-SmartPDF-Client": "skill", "Accept": "application/json"}
        data = None
        if upload is not None:
            data = _MultipartFile(upload)
            headers["Content-Type"] = f"multipart/form-data; boundary={data.boundary}"
            headers["Content-Length"] = str(data.length)
        elif body is not None:
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                return json.loads(raw) if raw else None
        except urllib.error.HTTPError as err:
            raw = err.read()
            if err.code == 429 and attempt < 3:
                wait = err.headers.get("Retry-After")
                wait = int(wait) if wait and wait.isdigit() else 5
                log(f"Слишком много запросов — ждём {wait} с и повторяем")
                time.sleep(min(wait, 60))
                continue
            raise ApiError(err.code, _detail(raw)) from None
        except (urllib.error.URLError, TimeoutError, ConnectionError) as err:
            if method == "GET" and attempt < 3:
                time.sleep(POLL_SECONDS)
                continue
            reason = getattr(err, "reason", err)
            raise ApiError(0, f"Нет связи с API ({API_URL}): {reason}") from None
    raise ApiError(429, "Слишком много запросов — попробуйте позже")


def explain(err: ApiError) -> str:
    hints = {
        401: f"Ключ не принят: проверьте SMARTPDF_API_KEY — ключ могли перевыпустить или удалить ({DASHBOARD_URL}).",
        402: f"Ничего не списано. Пополнить баланс или поднять лимит ключа: {DASHBOARD_URL}",
        404: "file_id живёт час, task_id — только с тем же ключом: загрузите файл заново.",
        410: "Результат уже удалён или ссылку на бесплатном тарифе уже выдавали — запустите операцию заново.",
        413: "Файл больше лимита тарифа: сожмите или разделите его (split).",
        415: "Формат не поддерживается или расширение не совпадает с содержимым.",
    }
    head = f"Ошибка {err.status}: {err.detail}" if err.status else err.detail
    hint = hints.get(err.status)
    return f"{head}\n{hint}" if hint else head


def parse_value(op: dict, name: str, raw: str):
    """Строковые параметры — как есть (пароль 0123 не станет числом), остальные — JSON."""
    kind = op["params"].get(name)
    if kind == "string":
        return raw
    try:
        return json.loads(raw)
    except ValueError:
        return raw


def resolve_operation(name: str) -> tuple[str, dict]:
    key = name.strip().lower().replace("_", "-")
    if key in OPERATIONS:
        return key, OPERATIONS[key]
    for slug, op in OPERATIONS.items():  # имя инструмента MCP: compress_pdf, merge_pdfs…
        if op["mcp"] == name:
            return slug, op
    raise SystemExit(f"Нет операции «{name}». Список: python3 {Path(__file__).name} operations")


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    for i in range(2, 1000):
        candidate = path.with_name(f"{path.stem} ({i}){path.suffix}")
        if not candidate.exists():
            return candidate
    return path


def upload(path: Path) -> str:
    size = path.stat().st_size
    log(f"Загрузка {path.name} ({size / 1048576:.1f} МБ)…")
    return request("POST", "/upload", upload=path, timeout=900)["file_id"]


def wait(task_id: str) -> dict:
    deadline = time.monotonic() + WAIT_LIMIT_SECONDS
    shown = None
    while True:
        task = request("GET", f"/tasks/{task_id}")
        status = task.get("status")
        if status == "done":
            return task
        if status == "failed":
            raise ProcessingFailed(task.get("error") or "Файл не удалось обработать.")
        note = task.get("stage") or (f"{task.get('progress')} %" if task.get("progress") else STATUS_TEXT.get(status, status))
        if note != shown:
            log(f"Обработка: {note}")
            shown = note
        if time.monotonic() > deadline:
            raise ApiError(0, f"Операция не завершилась за {WAIT_LIMIT_SECONDS // 60} минут. task_id: {task_id}")
        time.sleep(POLL_SECONDS)


def run_operation(args: argparse.Namespace) -> int:
    slug, op = resolve_operation(args.operation)
    files = [Path(f).expanduser() for f in args.files]
    if not files:
        raise SystemExit(f"Укажите файл: python3 {Path(__file__).name} {slug} document.pdf")
    if op["files"] == "one" and len(files) > 1:
        raise SystemExit(f"«{op['title']}» обрабатывает один файл за запрос — запустите скрипт для каждого файла.")
    for f in files:
        if not f.is_file():
            raise SystemExit(f"Файл не найден: {f}")

    params: dict = {}
    for item in args.param:
        name, sep, raw = item.partition("=")
        if not sep:
            raise SystemExit(f"Параметр — в виде имя=значение: {item}")
        params[name] = parse_value(op, name, raw)
    for item in args.data_uri:
        name, sep, raw = item.partition("=")
        image = Path(raw).expanduser()
        if not image.is_file():
            raise SystemExit(f"Файл не найден: {raw}")
        ctype = mimetypes.guess_type(image.name)[0] or "image/png"
        params[name] = f"data:{ctype};base64,{base64.b64encode(image.read_bytes()).decode()}"
    for item in args.upload:
        name, sep, raw = item.partition("=")
        if not Path(raw).expanduser().is_file():
            raise SystemExit(f"Файл не найден: {raw}")
        params[name] = None  # загрузим после проверки параметров
    missing = [name for name in op["required"] if name not in params]
    if missing:
        raise SystemExit(f"Не хватает обязательного параметра: {', '.join(missing)} (-p имя=значение). "
                         f"Справка: python3 {Path(__file__).name} operations")
    for item in args.upload:
        name, sep, raw = item.partition("=")
        params[name] = upload(Path(raw).expanduser())

    ids = [upload(f) for f in files]
    body = {"file_ids": ids} if op["files"] == "many" else {"file_id": ids[0]}
    body.update(params)
    log(f"Операция «{op['title']}»…")
    task_id = request("POST", op["endpoint"], body=body)["task_id"]
    task = wait(task_id)

    result = request("GET", f"/tasks/{task_id}/download")
    if args.link:
        print(result["download_url"])
        log(f"Ссылка действует до {result.get('expires_at')}: {result.get('filename')}")
        return 0
    out_dir = Path(args.out).expanduser() if args.out else files[0].parent
    out_dir.mkdir(parents=True, exist_ok=True)
    target = unique_path(out_dir / Path(result.get("filename") or f"result_{task_id}").name)
    req = urllib.request.Request(result["download_url"], headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=900) as resp, open(target, "wb") as fh:
        while chunk := resp.read(1 << 20):
            fh.write(chunk)
    before, after = task.get("input_file_size"), task.get("output_file_size")
    sizes = f" ({before / 1048576:.2f} → {after / 1048576:.2f} МБ)" if before and after else ""
    log(f"Готово{sizes}")
    print(target.resolve())
    return 0


def show_operations() -> int:
    for slug, op in OPERATIONS.items():
        params = ", ".join(f"{name} ({kind})" for name, kind in op["params"].items()) or "—"
        files = "несколько файлов" if op["files"] == "many" else "один файл"
        print(f"{slug:18} {op['title']} — {files}; MCP: {op['mcp']}; параметры: {params}")
    print("\nОписание параметров: reference/operations.md рядом со скриптом или https://dev.smartpdf.ru/docs/operations")
    return 0


def show_balance() -> int:
    print(json.dumps(request("GET", "/api-keys/balance"), ensure_ascii=False, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(
        prog="smartpdf.py",
        description="SmartPDF REST API: операция над файлами с диска. Ключ — SMARTPDF_API_KEY.",
        epilog="Примеры — в начале файла скрипта; документация — https://dev.smartpdf.ru/docs",
    )
    parser.add_argument("operation", help="операция (compress, merge, pdf-to-word…), balance или operations")
    parser.add_argument("files", nargs="*", help="файлы; у merge и jpg-to-pdf — в нужном порядке")
    parser.add_argument("-p", "--param", action="append", default=[], metavar="ИМЯ=ЗНАЧЕНИЕ",
                        help="параметр операции; массивы и числа — JSON: pages=[1,3]")
    parser.add_argument("--upload", action="append", default=[], metavar="ИМЯ=ФАЙЛ",
                        help="загрузить файл и передать его file_id (watermark: image_file_id=logo.png)")
    parser.add_argument("--data-uri", action="append", default=[], metavar="ИМЯ=КАРТИНКА",
                        help="передать картинку как data: URI (sign: signature_data=signature.png)")
    parser.add_argument("-o", "--out", help="папка для результата (по умолчанию — рядом с первым файлом)")
    parser.add_argument("--link", action="store_true", help="не скачивать, напечатать ссылку на результат (действует час)")
    args = parser.parse_args(argv)
    try:
        if args.operation == "operations":
            return show_operations()
        if args.operation == "balance":
            return show_balance()
        return run_operation(args)
    except ApiError as err:
        log(explain(err))
        return 1
    except ProcessingFailed as err:
        log(f"Файл не обработан: {err}\nОплата за операцию вернулась на баланс.")
        return 3
    except SystemExit as exc:
        if isinstance(exc.code, str):
            log(exc.code)
            return 2
        raise


if __name__ == "__main__":
    sys.exit(main())
