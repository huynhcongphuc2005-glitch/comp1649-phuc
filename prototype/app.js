/**
 * NeuroPulse HE — Interactive Mid-Fidelity Prototype Logic
 * Targets: iPhone 17 Pro Max viewport
 * Implements: Don Norman's Design Principles, Task Decomposition, Visual Focus Timer, Sensory Themes
 */

document.addEventListener('DOMContentLoaded', () => {
  // =========================================================================
  // 1. Clock & Real-time Status Bar
  // =========================================================================
  const clockElement = document.getElementById('live-clock');
  function updateLiveClock() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    if (clockElement) {
      clockElement.textContent = `${hours}:${minutes}`;
    }
  }
  updateLiveClock();
  setInterval(updateLiveClock, 30000);

  // =========================================================================
  // 2. Screen Navigation & Bottom Tab Bar
  // =========================================================================
  const screens = document.querySelectorAll('.screen');
  const navTabs = document.querySelectorAll('.bottom-tab-bar .tab-item');
  const journeyItems = document.querySelectorAll('.journey-list li');

  function navigateToScreen(targetScreenId) {
    screens.forEach(screen => {
      if (screen.id === targetScreenId) {
        screen.classList.add('active');
      } else {
        screen.classList.remove('active');
      }
    });

    navTabs.forEach(tab => {
      if (tab.getAttribute('data-nav') === targetScreenId) {
        tab.classList.add('active');
      } else {
        tab.classList.remove('active');
      }
    });

    journeyItems.forEach(item => {
      if (item.getAttribute('data-target-screen') === targetScreenId) {
        item.classList.add('active-step');
      } else {
        item.classList.remove('active-step');
      }
    });

    // Clear active Norman highlight on screen switch to avoid confusion
    clearPrincipleHighlights();
  }

  navTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.getAttribute('data-nav');
      if (target) navigateToScreen(target);
    });
  });

  journeyItems.forEach(item => {
    item.addEventListener('click', () => {
      const target = item.getAttribute('data-target-screen');
      if (target) navigateToScreen(target);
    });
  });

  // Back buttons
  document.querySelectorAll('[data-navigate-back]').forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.getAttribute('data-navigate-back');
      navigateToScreen(target);
    });
  });

  // In-screen direct navigation shortcuts
  document.getElementById('nav-btn-profile')?.addEventListener('click', () => {
    navigateToScreen('screen-settings');
  });

  document.getElementById('btn-open-breakdown')?.addEventListener('click', () => {
    navigateToScreen('screen-decompose');
  });

  document.getElementById('btn-cw-decompose')?.addEventListener('click', () => {
    navigateToScreen('screen-decompose');
  });

  document.getElementById('btn-start-hero-timer')?.addEventListener('click', () => {
    const heroTaskTitle = document.querySelector('.focus-hero-title')?.textContent || 'Micro-Focus Session';
    setTimerTask(heroTaskTitle);
    navigateToScreen('screen-timer');
    startTimer();
  });

  // =========================================================================
  // 3. Cognitive Overwhelm / Energy Check-in
  // =========================================================================
  const moodChips = document.querySelectorAll('.mood-chip');
  moodChips.forEach(chip => {
    chip.addEventListener('click', () => {
      moodChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      const mood = chip.getAttribute('data-mood');
      
      if (mood === 'overwhelmed') {
        showToast('🛡️ Sensory Shield Activated: Clutter hidden & soft palette applied');
        document.body.classList.add('mode-clutter-shield');
        applyPalette('theme-soft-sage');
        const shieldToggle = document.getElementById('toggle-clutter-shield');
        if (shieldToggle) shieldToggle.checked = true;
      } else {
        showToast(`Cognitive state saved: ${chip.textContent.trim()}`);
      }
    });
  });

  // =========================================================================
  // 4. Smart Task Breakdown & Stepping Stones
  // =========================================================================
  const taskChecklist = document.getElementById('task-checklist');

  function attachTaskEvents() {
    document.querySelectorAll('.stone-item').forEach(item => {
      const checkbox = item.querySelector('.stone-checkbox');
      if (checkbox && !checkbox.hasAttribute('data-bound')) {
        checkbox.setAttribute('data-bound', 'true');
        checkbox.addEventListener('click', (e) => {
          e.stopPropagation();
          item.classList.toggle('completed');
          if (item.classList.contains('completed')) {
            checkbox.textContent = '✓';
            showToast('🎉 Micro-step accomplished! Great momentum.');
          } else {
            checkbox.textContent = '';
          }
        });
      }
    });

    document.querySelectorAll('.btn-quick-play').forEach(btn => {
      if (!btn.hasAttribute('data-bound')) {
        btn.setAttribute('data-bound', 'true');
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          const stoneItem = btn.closest('.stone-item');
          const taskName = stoneItem?.querySelector('h5')?.textContent || 'Active Task';
          setTimerTask(taskName);
          navigateToScreen('screen-timer');
          startTimer();
        });
      }
    });
  }
  attachTaskEvents();

  // AI Magic Deconstruct feature
  const btnMagicChunk = document.getElementById('btn-magic-chunk');
  const inputNewAssignment = document.getElementById('input-new-assignment');

  btnMagicChunk?.addEventListener('click', () => {
    const rawVal = inputNewAssignment.value.trim();
    if (!rawVal) {
      showToast('⚠️ Please enter an assignment or topic first.');
      return;
    }

    btnMagicChunk.textContent = '⏳ Deconstructing...';
    btnMagicChunk.disabled = true;

    setTimeout(() => {
      const newItems = [
        { title: `Read grading criteria for "${rawVal}"`, duration: '10 mins • Planning' },
        { title: `Identify 3 key references for "${rawVal}"`, duration: '15 mins • Research' },
        { title: `Draft preliminary bullet outline`, duration: '15 mins • Structuring' },
        { title: `Write first draft section (150 words)`, duration: '15 mins • Drafting' }
      ];

      taskChecklist.innerHTML = '';
      newItems.forEach((task, idx) => {
        const stone = document.createElement('div');
        stone.className = `stone-item ${idx === 0 ? 'current-step' : ''}`;
        stone.setAttribute('data-task-id', `new-${idx}`);
        stone.innerHTML = `
          <div class="stone-checkbox"></div>
          <div class="stone-content">
            <h5>${task.title}</h5>
            <span class="stone-duration">${task.duration}</span>
          </div>
          <button class="btn-quick-play" title="Launch timer for this task">▶</button>
        `;
        taskChecklist.appendChild(stone);
      });

      attachTaskEvents();
      btnMagicChunk.textContent = '🪄 Break Down';
      btnMagicChunk.disabled = false;
      showToast(`✨ Deconstructed "${rawVal}" into 4 manageable micro-actions!`);
    }, 600);
  });

  // =========================================================================
  // 5. Visual Time-Blindness Timer (Sensory Pomodoro)
  // =========================================================================
  let timerInterval = null;
  let totalSeconds = 15 * 60;
  let remainingSeconds = totalSeconds;
  let isRunning = false;

  const timerDisplay = document.getElementById('timer-display');
  const timerCaption = document.getElementById('timer-status-caption');
  const timerRing = document.getElementById('timer-progress-ring');
  const timerToggleBtn = document.getElementById('btn-timer-toggle');
  const timerResetBtn = document.getElementById('btn-timer-reset');
  const timerTaskLabel = document.getElementById('timer-task-label');
  const timerPresets = document.querySelectorAll('.btn-preset');
  const circumference = 2 * Math.PI * 100; // 628.318

  function setTimerTask(title) {
    if (timerTaskLabel) timerTaskLabel.textContent = title;
  }

  function updateTimerDisplay() {
    const mins = Math.floor(remainingSeconds / 60);
    const secs = remainingSeconds % 60;
    if (timerDisplay) {
      timerDisplay.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }

    if (timerRing) {
      const fraction = remainingSeconds / totalSeconds;
      const offset = circumference * (1 - fraction);
      timerRing.style.strokeDashoffset = offset;
    }
  }

  function startTimer() {
    if (isRunning) return;
    isRunning = true;
    timerToggleBtn.textContent = '⏸ Pause Session';
    timerCaption.textContent = 'Focusing... you are in flow';
    
    timerInterval = setInterval(() => {
      if (remainingSeconds > 0) {
        remainingSeconds--;
        updateTimerDisplay();
      } else {
        clearInterval(timerInterval);
        isRunning = false;
        timerToggleBtn.textContent = '▶ Begin Micro-Focus';
        timerCaption.textContent = 'Session complete! 🍃';
        showToast('🔔 Micro-focus finished! Rest your eyes for 3 minutes.');
      }
    }, 1000);
  }

  function pauseTimer() {
    if (!isRunning) return;
    clearInterval(timerInterval);
    isRunning = false;
    timerToggleBtn.textContent = '▶ Resume Focus';
    timerCaption.textContent = 'Paused (Take a breath)';
  }

  function resetTimer() {
    pauseTimer();
    remainingSeconds = totalSeconds;
    updateTimerDisplay();
    timerToggleBtn.textContent = '▶ Begin Micro-Focus';
    timerCaption.textContent = 'Ready to focus';
    showToast('Timer reset to starting duration.');
  }

  timerToggleBtn?.addEventListener('click', () => {
    if (isRunning) {
      pauseTimer();
    } else {
      startTimer();
    }
  });

  timerResetBtn?.addEventListener('click', resetTimer);

  timerPresets.forEach(presetBtn => {
    presetBtn.addEventListener('click', () => {
      timerPresets.forEach(b => b.classList.remove('active'));
      presetBtn.classList.add('active');
      const minutes = parseInt(presetBtn.getAttribute('data-minutes'), 10) || 15;
      totalSeconds = minutes * 60;
      remainingSeconds = totalSeconds;
      resetTimer();
    });
  });

  document.getElementById('btn-timer-sound')?.addEventListener('click', (e) => {
    const btn = e.currentTarget;
    if (btn.textContent.includes('On')) {
      btn.textContent = '🔇 Sound: Off';
      showToast('Ambient sensory sound muted.');
    } else {
      btn.textContent = '🎧 Sound: On';
      showToast('Calming Brown Noise enabled.');
    }
  });

  // =========================================================================
  // 6. Neuro-Adaptive Sensory Settings
  // =========================================================================
  // Typography toggle
  const toggleDyslexic = document.getElementById('toggle-dyslexic-font');
  toggleDyslexic?.addEventListener('change', (e) => {
    if (e.target.checked) {
      document.body.classList.add('font-dyslexic');
      showToast('📖 Dyslexia-friendly font & weighted spacing enabled.');
    } else {
      document.body.classList.remove('font-dyslexic');
      showToast('Default typography restored.');
    }
  });

  // Bionic reading simulation
  const toggleBionic = document.getElementById('toggle-bionic-reading');
  toggleBionic?.addEventListener('change', (e) => {
    if (e.target.checked) {
      showToast('👁️ Guided fixation reading highlights active.');
    } else {
      showToast('Guided fixation reading disabled.');
    }
  });

  // Clutter shield toggle
  const toggleClutter = document.getElementById('toggle-clutter-shield');
  toggleClutter?.addEventListener('change', (e) => {
    if (e.target.checked) {
      document.body.classList.add('mode-clutter-shield');
      showToast('🛡️ Minimalist mode enabled: Non-essential elements shielded.');
    } else {
      document.body.classList.remove('mode-clutter-shield');
      showToast('Full interface mode restored.');
    }
  });

  // Color Palette Selector
  const paletteCards = document.querySelectorAll('.palette-card');
  function applyPalette(themeClass) {
    document.body.classList.remove('theme-default', 'theme-soft-sage', 'theme-warm-amber', 'theme-dark-focus');
    document.body.classList.add(themeClass);

    paletteCards.forEach(c => {
      if (c.getAttribute('data-palette') === themeClass) {
        c.classList.add('active');
      } else {
        c.classList.remove('active');
      }
    });
  }

  paletteCards.forEach(card => {
    card.addEventListener('click', () => {
      const palette = card.getAttribute('data-palette');
      applyPalette(palette);
      showToast(`Palette switched to: ${card.querySelector('strong')?.textContent}`);
    });
  });

  // =========================================================================
  // 7. Don Norman's Principles Inspector (Examiner Feature)
  // =========================================================================
  const principleButtons = document.querySelectorAll('.btn-principle');
  const principleExplanation = document.getElementById('principle-explanation');

  const principleTheoreticalData = {
    visibility: {
      title: 'Visibility (Norman, 2013)',
      desc: 'The single prioritized micro-step hero card and prominent circular time gauge ensure critical affordances are immediately perceptible without cognitive searching.',
      targetSelector: '[data-principle-target*="visibility"]'
    },
    feedback: {
      title: 'Feedback (Norman, 2013)',
      desc: 'Real-time progress bars, circular countdown updates, and confirmation toasts give instant, non-jarring feedback on user actions and system state.',
      targetSelector: '[data-principle-target*="feedback"]'
    },
    constraints: {
      title: 'Constraints (Norman, 2013)',
      desc: 'Preventing overwhelm by limiting active focus to one single 15-minute subtask, pre-setting chunk intervals, and locking out multi-tasking chaos.',
      targetSelector: '[data-principle-target*="constraints"]'
    },
    consistency: {
      title: 'Consistency (Norman, 2013)',
      desc: 'Standardized persistent bottom navigation, uniform progress ring styles, and consistent card padding adhere to established mental models.',
      targetSelector: '[data-principle-target*="consistency"]'
    },
    affordance: {
      title: 'Affordance (Norman, 2013)',
      desc: 'Raised pill buttons, clear play action triggers, toggle switches, and tactile checkboxes visually invite direct finger tapping.',
      targetSelector: '[data-principle-target*="affordance"]'
    }
  };

  function clearPrincipleHighlights() {
    document.querySelectorAll('.principle-highlighted').forEach(el => {
      el.classList.remove('principle-highlighted');
    });
  }

  principleButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const principleKey = btn.getAttribute('data-principle');
      const isAlreadyActive = btn.classList.contains('active');

      principleButtons.forEach(b => b.classList.remove('active'));
      clearPrincipleHighlights();

      if (isAlreadyActive) {
        principleExplanation.innerHTML = '<em>Select a principle above to view its theoretical justification.</em>';
        return;
      }

      btn.classList.add('active');
      const data = principleTheoreticalData[principleKey];
      if (data) {
        principleExplanation.innerHTML = `<strong>${data.title}</strong><br>${data.desc}`;
        
        // Find all elements on the active screen that match
        const activeScreen = document.querySelector('.screen.active');
        if (activeScreen) {
          const targets = activeScreen.querySelectorAll(data.targetSelector);
          targets.forEach(el => el.classList.add('principle-highlighted'));
          
          if (targets.length === 0) {
            showToast(`Note: Principle applied primarily on other screens. Explore tabs below.`);
          }
        }
      }
    });
  });

  // =========================================================================
  // 8. Toast Feedback Utility
  // =========================================================================
  let toastTimer = null;
  function showToast(message) {
    const toast = document.getElementById('toast-notification');
    if (!toast) return;
    toast.textContent = message;
    toast.classList.remove('toast-hidden');

    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toast.classList.add('toast-hidden');
    }, 3200);
  }
});
