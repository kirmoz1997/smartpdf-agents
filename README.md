<p align="center"><img src="assets/logo.png" width="96" height="96" alt="SmartPDF"></p>

# SmartPDF для ИИ-агентов

24 операции с PDF для Claude Code, Codex CLI, Gemini CLI, Cursor, VS Code и других агентов: конвертация в PDF и из
PDF, сжатие, объединение и разделение, распознавание текста (в том числе русского), страницы, подпись, водяной знак,
пароль. Серверы в Москве, оплата в рублях за запрос.

[Портал для разработчиков](https://dev.smartpdf.ru) · [Документация](https://dev.smartpdf.ru/docs) ·
[llms.txt](https://dev.smartpdf.ru/llms.txt)

| Что | Где |
|---|---|
| Плагин Claude Code: MCP-сервер и навык | `.claude-plugin/` |
| Плагин Cursor: MCP-сервер и навык | `.cursor-plugin/`, `mcp.json` |
| Навык (Agent Skill) для любого агента: инструкция, скрипт для файлов с диска, справочник параметров | [`skills/smartpdf/`](skills/smartpdf) |
| Описание для реестра MCP | [`server.json`](server.json) |

## Ключ

Зарегистрируйтесь на [smartpdf.ru](https://smartpdf.ru/register?from=dev) и подтвердите почту — на баланс API придёт
300 ₽. Ключ `sk_live_…` создаётся в личном кабинете, в разделе [«API и MCP»](https://smartpdf.ru/dashboard/api-keys).
Цена запроса и бонусы при пополнении — на [dev.smartpdf.ru](https://dev.smartpdf.ru/#pricing).

## Claude Code — плагин

```
/plugin marketplace add kirmoz1997/smartpdf-agents
/plugin install smartpdf@smartpdf
```

Claude Code спросит ключ и сохранит его в защищённом хранилище системы. После установки агенту доступны инструменты
SmartPDF для файлов по ссылкам и навык `smartpdf` для файлов с диска — ему нужна ещё переменная окружения
`SMARTPDF_API_KEY` с тем же ключом.

Из терминала: `claude plugin marketplace add kirmoz1997/smartpdf-agents`, затем
`claude plugin install smartpdf@smartpdf --config api_key=sk_live_…`.

## Cursor

Плагин для Cursor (MCP-сервер и навык) — в этом же репозитории (`.cursor-plugin/`, `mcp.json`); ключ задаётся в
**Plugins → Configure**. Только MCP-сервер — одной ссылкой: [Добавить в Cursor](https://cursor.com/install-mcp?name=smartpdf&config=eyJ1cmwiOiJodHRwczovL21jcC5zbWFydHBkZi5ydS9tY3AiLCJoZWFkZXJzIjp7IkF1dGhvcml6YXRpb24iOiJCZWFyZXIgJHtlbnY6U01BUlRQREZfQVBJX0tFWX0ifX0%3D) (ключ — из переменной окружения
`SMARTPDF_API_KEY`).

## Только MCP-сервер

| | |
|---|---|
| Адрес | `https://mcp.smartpdf.ru/mcp` |
| Транспорт | Streamable HTTP |
| Ключ | `Authorization: Bearer sk_live_…` или `X-API-Key: sk_live_…` |

Сервер есть в [официальном реестре MCP](https://registry.modelcontextprotocol.io/v0.1/servers?search=ru.smartpdf/smartpdf)
под именем `ru.smartpdf/smartpdf`.

Готовые конфиги для Claude Desktop, Cursor, VS Code, Codex CLI, Gemini CLI, Windsurf, Cline, n8n и Make —
в [документации](https://dev.smartpdf.ru/docs/mcp). Инструменты принимают публичные ссылки на файлы до 100 МБ и
возвращают ссылку на результат.

## Навык в других агентах

Навык работает и с MCP-инструментами, и без них: файлы с диска он обрабатывает скриптом
[`scripts/smartpdf.py`](skills/smartpdf/scripts/smartpdf.py) через REST API (нужен Python 3, ключ — в
`SMARTPDF_API_KEY`). Скопируйте папку `skills/smartpdf` туда, где агент ищет навыки:

```bash
git clone https://github.com/kirmoz1997/smartpdf-agents
cp -R smartpdf-agents/skills/smartpdf ~/.agents/skills/
```

| Агент | Папка навыков |
|---|---|
| Codex CLI | `~/.agents/skills/` или `.agents/skills/` в проекте |
| Gemini CLI | `.gemini/skills/` или `.agents/skills/` в проекте |
| Cursor | `.cursor/skills/` или `.agents/skills/` в проекте |
| VS Code (Copilot) | `.github/skills/` или `.agents/skills/` в проекте |
| Claude Code без плагина | `~/.claude/skills/` или `.claude/skills/` в проекте |

Скрипт можно запускать и самому:

```bash
export SMARTPDF_API_KEY=sk_live_…
python3 skills/smartpdf/scripts/smartpdf.py compress report.pdf -p level=high
python3 skills/smartpdf/scripts/smartpdf.py operations
```

## English

SmartPDF is a Russian PDF service (servers in Moscow, billing in rubles per request). This repository contains a
Claude Code plugin (remote MCP server + agent skill), a standalone Agent Skill with a stdlib-only Python script for
local files, and `server.json` for the official MCP Registry.

- MCP: `https://mcp.smartpdf.ru/mcp`, Streamable HTTP, `Authorization: Bearer <API key>`; 24 tools that take public file
  URLs and return a download link, plus `get_balance`. Official MCP Registry: `ru.smartpdf/smartpdf`.
- Claude Code: `/plugin marketplace add kirmoz1997/smartpdf-agents`, then `/plugin install smartpdf@smartpdf`.
- Cursor: plugin in `.cursor-plugin/` + `mcp.json` (key in Plugins → Configure), or [Add to Cursor](https://cursor.com/install-mcp?name=smartpdf&config=eyJ1cmwiOiJodHRwczovL21jcC5zbWFydHBkZi5ydS9tY3AiLCJoZWFkZXJzIjp7IkF1dGhvcml6YXRpb24iOiJCZWFyZXIgJHtlbnY6U01BUlRQREZfQVBJX0tFWX0ifX0%3D).
- API keys: [smartpdf.ru](https://smartpdf.ru/register?from=dev) — 300 ₽ of free balance after email confirmation.
- Documentation (in Russian): [dev.smartpdf.ru/docs](https://dev.smartpdf.ru/docs),
  [llms.txt](https://dev.smartpdf.ru/llms.txt). Contact: smartpdf@yandex.ru.

## Лицензия

Файлы этого репозитория — [MIT](LICENSE). Работа сервиса — по [оферте](https://smartpdf.ru/terms).
