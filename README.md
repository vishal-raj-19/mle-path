# MLE Path — 6-month ML Engineer planner

A local website that plans your 26-week path to ML Engineer and re-plans itself when you miss days.

## Run it
You need Python 3 (no packages).

- **Windows:** double-click `start-windows.bat`
- **macOS:** double-click `start-mac.command` (first time: right-click → Open)
- **Linux:** `./start.sh`

Your browser opens at http://127.0.0.1:8765. Keep the terminal window open while you use it.
Progress is saved to `progress.json` in this folder, with one backup per day in `backups/`.

You can also just open `index.html` directly. It works the same way, but progress is then saved only in that browser.

## How the auto-adjust works
- The plan is a queue of 182 tasks (415.5 h). Each day takes as many hours as you set (default Mon–Fri 2 h, Sat–Sun 3.5 h).
- Anything you don't finish rolls forward. The calendar is rebuilt from today every time you open the site.
- If the projected finish passes your target date, **stretch** tasks move to a backlog (latest first). They come back when you catch up.
- **I know this** skips a task and pulls everything forward. **Can't study today** frees today. **Plan → Calendar** lets you set hours for any day (0 = day off).
- After missed days you'll see a banner with a one-click option to add 3 weeks of catch-up hours.
- To see what the plan would look like on another date, open `http://127.0.0.1:8765/?today=2026-12-01`. Nothing real changes.
