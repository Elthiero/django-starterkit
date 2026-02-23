/* ============================================================
   STARTER KIT — public.js
   ============================================================ */
(function () {
  'use strict';

  /* ── Navbar scroll effect ─────────────────────────────── */
  function initNavScroll() {
    const nav = document.getElementById('pub-nav');
    if (!nav) return;
    function onScroll() {
      nav.classList.toggle('scrolled', window.scrollY > 20);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ── Password strength meter ──────────────────────────── */
  function initPasswordStrength() {
    const pw = document.getElementById('id_password1') || document.getElementById('id_new_password1');
    const bars = document.querySelectorAll('.pub-pw-bar');
    if (!pw || !bars.length) return;

    function getStrength(val) {
      let score = 0;
      if (val.length >= 8)  score++;
      if (val.length >= 12) score++;
      if (/[A-Z]/.test(val)) score++;
      if (/[0-9]/.test(val)) score++;
      if (/[^A-Za-z0-9]/.test(val)) score++;
      return score;
    }

    pw.addEventListener('input', function () {
      const score = getStrength(this.value);
      bars.forEach(function (b, i) {
        b.className = 'pub-pw-bar';
        if (this.value.length === 0) return;
        if (score <= 2 && i === 0) b.classList.add('weak');
        if (score === 3 && i <= 1) b.classList.add('medium');
        if (score >= 4 && i <= 2) b.classList.add('strong');
      }, pw);
    });
  }

  /* ── Prose TOC active link ────────────────────────────── */
  function initTOC() {
    const tocLinks = document.querySelectorAll('.pub-prose-toc a');
    if (!tocLinks.length) return;
    const headings = Array.from(tocLinks)
      .map(a => document.querySelector(a.getAttribute('href')))
      .filter(Boolean);

    function onScroll() {
      const offset = 100;
      let active = headings[0];
      headings.forEach(function (h) {
        if (h.getBoundingClientRect().top < offset) active = h;
      });
      tocLinks.forEach(function (a) {
        const target = document.querySelector(a.getAttribute('href'));
        a.classList.toggle('active', target === active);
      });
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ── FAQ anchor smooth scroll ─────────────────────────── */
  function initSmoothAnchors() {
    var nav = document.getElementById('pub-nav');
    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var href = this.getAttribute('href');
        var target = document.querySelector(href);
        if (!target) return;
        e.preventDefault();
        var navH = nav ? nav.getBoundingClientRect().height : 64;
        var top = target.getBoundingClientRect().top + window.scrollY - navH - 20;
        window.scrollTo({ top: top, behavior: 'smooth' });
        history.pushState(null, '', href);
      });
    });
  }

  /* ── Auto dismiss alerts ──────────────────────────────── */
  function initAlerts() {
    document.querySelectorAll('.alert-dismissible').forEach(function (el) {
      setTimeout(function () {
        const inst = bootstrap && bootstrap.Alert.getOrCreateInstance(el);
        if (inst) inst.close();
      }, 5000);
    });
  }

  /* ── Init ─────────────────────────────────────────────── */
  document.addEventListener('DOMContentLoaded', function () {
    initNavScroll();
    initPasswordStrength();
    initTOC();
    initSmoothAnchors();
    initAlerts();
  });
})();