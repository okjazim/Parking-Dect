let lastDistance = -999;

document.addEventListener('DOMContentLoaded', () => {
  // Theme switching functionality
  const themeToggle = document.getElementById('themeToggle');
  const sunIcon = document.getElementById('sunIcon');
  const moonIcon = document.getElementById('moonIcon');
  const html = document.documentElement;

  function updateThemeIcon(theme) {
    if (!sunIcon || !moonIcon) return;

    if (theme === 'dark') {
      sunIcon.classList.add('hidden');
      moonIcon.classList.remove('hidden');
    } else {
      sunIcon.classList.remove('hidden');
      moonIcon.classList.add('hidden');
    }
  }

  // Load saved theme preference - defaults to light mode
  const savedTheme = localStorage.getItem('theme') || 'light';

  // Apply the saved theme
  if (savedTheme === 'dark') {
    html.classList.add('dark');
    updateThemeIcon('dark');
  } else {
    html.classList.remove('dark');
    updateThemeIcon('light');
  }

  // Toggle theme on button click
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const isDark = html.classList.contains('dark');

      if (isDark) {
        html.classList.remove('dark');
        localStorage.setItem('theme', 'light');
        updateThemeIcon('light');
      } else {
        html.classList.add('dark');
        localStorage.setItem('theme', 'dark');
        updateThemeIcon('dark');
      }
    });

    // Double-click to force reset to light mode (in case of issues)
    themeToggle.addEventListener('dblclick', (e) => {
      e.preventDefault();
      html.classList.remove('dark');
      localStorage.setItem('theme', 'light');
      updateThemeIcon('light');
    });
  }

  function update(distance) {
    if (distance === lastDistance) return;
    lastDistance = distance;

    const distEl = document.getElementById('distance');
    const statusEl = document.getElementById('status');
    const r = document.getElementById('lampRed');
    const y = document.getElementById('lampYellow');
    const g = document.getElementById('lampGreen');
    const meter = document.getElementById('meterFill');

    // If any element is missing, don't crash.
    if (!distEl || !statusEl || !r || !y || !g || !meter) return;

    distEl.textContent = distance > 0 ? distance.toFixed(1) + ' cm' : '-- cm';

    // Turn everything off first
    r.classList.remove('active');
    y.classList.remove('active');
    g.classList.remove('active');

    // Meter: closer = more filled (0cm -> 100%, 60cm+ -> 0%)
    if (distance > 0) {
      const clamped = Math.max(0, Math.min(distance, 60));
      meter.style.width = (100 - (clamped / 60) * 100).toFixed(0) + '%';
    } else {
      meter.style.width = '0%';
    }

    let state = 'NO SIGNAL';
    distEl.style.color = 'var(--text-primary)';

    if (distance > 0) {
      if (distance <= 15) {
        r.classList.add('active');
        state = 'STOP - Too close!';
        distEl.style.color = 'var(--danger)';
      } else if (distance <= 25) {
        y.classList.add('active');
        state = 'SLOW - Careful approach';
        distEl.style.color = 'var(--warning)';
      } else if (distance <= 45) {
        g.classList.add('active');
        state = 'GO - Safe distance';
        distEl.style.color = 'var(--success)';
      } else {
        g.classList.add('active');
        state = 'CLEAR - Optimal spacing';
        distEl.style.color = 'var(--text-primary)';
      }
    }

    statusEl.textContent = state;
  }

  function getData() {
    fetch('/data')
      .then(r => r.json())
      .then(d => update(d.distance))
      .catch(() => update(-1));
  }

  setInterval(getData, 300);
  getData();
});
