/* ============================================================
   STARTER KIT — main.js
   ============================================================ */

(function () {
    'use strict';

    /* ── Sidebar Toggle (desktop) ─────────────────────────── */
    const STORAGE_KEY = 'sk-sidebar-collapsed';

    function initSidebar() {
        const toggle = document.getElementById('sk-sidebar-toggle');
        if (!toggle) return;

        // Restore saved state
        if (localStorage.getItem(STORAGE_KEY) === '1') {
            document.body.classList.add('sidebar-collapsed');
        }

        toggle.addEventListener('click', function () {
            const collapsed = document.body.classList.toggle('sidebar-collapsed');
            localStorage.setItem(STORAGE_KEY, collapsed ? '1' : '0');
        });
    }

    /* ── HTMX Progress Bar ────────────────────────────────── */
    function initProgress() {
        const bar = document.getElementById('sk-progress');
        if (!bar) return;

        let timer = null;

        document.body.addEventListener('htmx:beforeRequest', function () {
            bar.style.width = '0%';
            bar.style.opacity = '1';
            let w = 0;
            clearInterval(timer);
            timer = setInterval(function () {
                w = Math.min(w + Math.random() * 15, 85);
                bar.style.width = w + '%';
            }, 200);
        });

        document.body.addEventListener('htmx:afterRequest', function () {
            clearInterval(timer);
            bar.style.width = '100%';
            setTimeout(function () { bar.style.opacity = '0'; bar.style.width = '0%'; }, 350);
        });
    }

    /* ── Auto-dismiss Django messages ────────────────────── */
    function initMessages() {
        document.querySelectorAll('.alert.alert-dismissible').forEach(function (el) {
            setTimeout(function () {
                const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
                bsAlert.close();
            }, 5000);
        });
    }

    /* ── Active nav link highlight ───────────────────────── */
    function initActiveNav() {
        const path = window.location.pathname;
        document.querySelectorAll('.sk-nav-link').forEach(function (link) {
            const href = link.getAttribute('href');
            if (href && href !== '/' && path.startsWith(href)) {
                link.classList.add('active');
                // Open parent collapse if inside submenu
                const collapse = link.closest('.collapse');
                if (collapse) {
                    collapse.classList.add('show');
                    const trigger = document.querySelector('[data-bs-target="#' + collapse.id + '"]');
                    if (trigger) trigger.setAttribute('aria-expanded', 'true');
                }
            }
        });
    }

    /* ── Bootstrap collapse chevron sync ─────────────────── */
    function initChevrons() {
        document.querySelectorAll('[data-bs-toggle="collapse"]').forEach(function (trigger) {
            const targetId = trigger.getAttribute('href') || trigger.getAttribute('data-bs-target');
            const target = document.querySelector(targetId);
            if (!target) return;

            target.addEventListener('show.bs.collapse', function () { trigger.setAttribute('aria-expanded', 'true'); });
            target.addEventListener('hide.bs.collapse', function () { trigger.setAttribute('aria-expanded', 'false'); });
        });
    }

    /* ── Init ─────────────────────────────────────────────── */
    document.addEventListener('DOMContentLoaded', function () {
        initSidebar();
        initProgress();
        initMessages();
        initActiveNav();
        initChevrons();
    });
})();