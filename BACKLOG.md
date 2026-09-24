# Backlog — knm-audio

## T-01 — Редизайн под конвенции аудиокниг
Текущий UI (dark + JetBrains Mono + study-ring) выглядит как дашборд, не как
аудиокнига. Переверстать по референсам реальных audiobook-приложений
(Audible, Spotify Audiobooks, Libro.fm, Storytel): чистая обложка/hero текущей
главы, вертикальный список глав вместо горизонтальной обрезающейся полки,
консистентные брейкпоинты для десктопа и мобилки. CSS сейчас захламлён
несколькими наслоившимися патчами — почистить при переверстке.
Status: **done** — единая тёмная/светлая тема, вертикальный список глав с
обложками вместо горизонтальной полки, карточка "Verder luisteren", убрана
мёртвая rail/sidebar-вёрстка и study-ring.

## T-02 — Проверить, что вся озвучка на ElevenLabs
README и коммиты показывают: только главы 1-2 + H5T5 (11 из 36 треков)
переозвучены через ElevenLabs Flash, остальные 25 — всё ещё edge-tts
(Microsoft neural, `nl-NL-MaartenNeural`/`en-US-GuyNeural`). Нет
ElevenLabs API-ключа в системе → перегенерация остальных 25 треков требует
ключа и стоит денег (ElevenLabs тарифицирует по символам).
Status: **investigated, blocked on decision** — см. отчёт в сессии.

## T-03 — Перенести деплой с GitHub Pages на Netlify
По аналогии с hdash.netlify.app / knm-quiz.netlify.app: отдельный Netlify-сайт,
репозиторий остаётся на GitHub, деплой — `netlify deploy --prod`.
Status: **done**

## T-04 — Пуш + деплой после каждого существенного изменения
Зафиксировать как рабочий процесс: любое значимое изменение → git commit +
push на GitHub → `netlify deploy --prod`.
Status: **ongoing convention**, применяется начиная с этой сессии.
